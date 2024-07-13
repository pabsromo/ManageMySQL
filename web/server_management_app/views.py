from django.shortcuts import render, redirect

from .models import Users
from .models import Servers

from .forms import UsersForm
from .forms import ServersForm


# Todo List View
def home(request):
    users = Users.objects.all()
    servers = Servers.objects.all()
    return render(request, "home.html", {"users": users, "servers": servers})


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
