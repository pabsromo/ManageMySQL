from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError

from typing import Tuple

import os
import paramiko
import re

import logging

from .models import Users
from .models import Images
from .models import Containers

from .forms import UsersForm
from .forms import ImagesForm
from .forms import ServersForm

# Instance of logger
logger = logging.getLogger(__name__)


# USEFUL METHODS
def run_ssh_command(command: str) -> Tuple[str, str]:
    hostname = "172.21.169.35"  # Replace with your WSL2 host IP address
    port = 22
    username = "pabromo"  # Replace with your WSL2 username
    key_filename = "/root/.ssh/id_rsa"

    # Load the private key
    private_key = paramiko.RSAKey.from_private_key_file(key_filename)

    # Create an SSH client instance
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the SSH server using key-based authentication
        ssh.connect(hostname, port, username, pkey=private_key)

        # Execute the command
        stdin, stdout, stderr = ssh.exec_command(command)
        out = stdout.read().decode()
        err = stderr.read().decode()

        return out, err

    finally:
        # Ensure the SSH connection is closed
        ssh.close()


# ABSTRACTED METHODS
def update_images():
    # Call subprocess to list images and put into list
    image_output = run_ssh_command("docker images")
    image_lines = image_output[0].split("\n")
    image_lines = image_lines[1:-1]

    # Gather SSH output to List of Images Objects
    image_list = []
    for row in image_lines:
        row_list = re.split(r"\s{2,}", row)
        temp_image = Images(
            image_name=row_list[0], tag=row_list[1], image_hash=row_list[2]
        )
        image_list.append(temp_image)

    # Pare down images to only new ones
    new_images = []
    existing_images = set(Images.objects.values_list("image_name", flat=True))
    for image in image_list:
        if image.image_name not in existing_images:
            new_images.append(image)

    # Insert new images only
    try:
        Images.objects.bulk_create(new_images)
    except IntegrityError as e:
        print(f"IntegrityError: {e}")
        pass


def update_servers():
    # Call subprocess to list images and put into list
    container_output = run_ssh_command("docker ps -a")
    container_lines = container_output[0].split("\n")
    container_lines = container_lines[1:-1]

    # Gather SSH output to List of Images Objects
    container_list = []
    for row in container_lines:
        row_list = re.split(r"\s{2,}", row)
        temp_container = Containers(
            container_hash=row_list[0],
            image=Images.objects.get(image_name=row_list[1].split(":")[0]),
            created=row_list[3],
            status=row_list[4],
            port=row_list[5].split("->")[0][-4:],
            container_name=row_list[6],
        )
        container_list.append(temp_container)

    # Pare down images to only new ones
    new_containers = []
    existing_containers = set(
        Containers.objects.values_list("container_name", flat=True)
    )
    for container in container_list:
        if container.container_name not in existing_containers:
            new_containers.append(container)

    # Insert new images only
    try:
        Containers.objects.bulk_create(new_containers)
    except IntegrityError as e:
        print(f"IntegrityError: {e}")
        pass


# HOME PAGE
def home(request):
    users = Users.objects.all()
    images = Images.objects.all()
    servers = Containers.objects.all()

    # First, let's print the current working directory
    print("Current Working Directory", os.getcwd())
    return render(
        request,
        "home.html",
        {
            "users": users,
            "servers": servers,
            "images": images,
            "hostname": run_ssh_command("hostname"),
        },
    )


# CREATE VIEWS # TODO: Condense these into one common method and their html files too
def user_create(request):
    if request.method == "POST":
        form = UsersForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = UsersForm()
    return render(request, "user_create.html", {"form": form})


def image_create(request):
    if request.method == "POST":
        form = ImagesForm(request.POST)
        if form.is_valid():
            # form.save()

            # Get info for docker pull
            image_name = form.cleaned_data.get("image_name")
            tag = form.cleaned_data.get("tag")

            # Build command
            command: str = ""
            if tag == "none":
                command = "docker pull " + image_name
            else:
                command = "docker pull " + image_name + ":" + tag

            logger.info(command)

            # Execute docker pull
            run_ssh_command(command)
            update_images()
            return redirect("home")
    else:
        form = ImagesForm()
    return render(request, "image_create.html", {"form": form})


def server_create(request):
    if request.method == "POST":
        form = ServersForm(request.POST)
        if form.is_valid():
            # form.save()

            # Get data
            logger.info("container_name: " + form.cleaned_data.get("container_name"))
            logger.info("image: " + form.cleaned_data.get("image").image_name)
            logger.info("port: " + str(form.cleaned_data.get("port")))
            logger.info("database_name: " + form.cleaned_data.get("database_name"))

            container_name = form.cleaned_data.get("container_name")
            image = form.cleaned_data.get("image")
            image_name = image.image_name
            image_tag = image.tag
            database_name = form.cleaned_data.get("database_name")
            password = form.cleaned_data.get("password")
            port = form.cleaned_data.get("port")

            # Build command #TODO: customize per type of DBMS
            command: str = f"docker run -d --name {container_name} -e MYSQL_DATABASE={database_name} -e MYSQL_ROOT_PASSWORD={password} -v {container_name}-data:/var/lib/{image_name} -p {port}:3306 {image_name}:{image_tag} --default-authentication-plugin=mysql_native_password"

            logger.info("BUILT COMMAND TO BUILD DATABASE:\n" + command)

            run_ssh_command(command)
            return redirect("home")
    else:
        form = ServersForm()
    return render(request, "server_create.html", {"form": form})


# DELETE VIEWS
def user_delete(request, user_id):
    user = get_object_or_404(Users, id=user_id)
    user.delete()
    return redirect("home")


def image_delete(request, image_id):
    image = get_object_or_404(Images, id=image_id)
    logger.info("DELETING IMAGE")
    logger.info("docker rmi " + image.image_hash)
    run_ssh_command("docker rmi " + image.image_hash)
    image.delete()
    return redirect("home")


def server_delete(request, server_id):
    container = get_object_or_404(Containers, id=server_id)
    logger.info("DELETING SERVER")
    logger.info("docker rm " + container.container_hash)
    run_ssh_command("docker stop " + container.container_hash)
    run_ssh_command("docker rm " + container.container_hash)
    container.delete()
    return redirect("home")


# UPDATE VIEWS
def image_update_list(request):
    update_images()
    return redirect("home")


def server_update_list(request):
    update_servers()
    return redirect("home")
