from django.shortcuts import render, redirect

from typing import Tuple

import os
import subprocess
import paramiko

from .models import Users
from .models import Servers

from .forms import UsersForm
from .forms import ServersForm


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


# Todo List View
def home(request):
    users = Users.objects.all()
    servers = Servers.objects.all()

    # First, let's print the current working directory
    print("Current Working Directory", os.getcwd())
    return render(
        request,
        "home.html",
        {"users": users, "servers": servers, "hostname": run_ssh_command("hostname")},
    )


# Create Views
def user_create(request):
    if request.method == "POST":
        form = UsersForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = UsersForm()
    return render(request, "user_create.html", {"form": form})


def server_create(request):
    if request.method == "POST":
        form = ServersForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = ServersForm()
    return render(request, "server_create.html", {"form": form})
