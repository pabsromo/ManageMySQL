from django.shortcuts import render


# Todo List View
def home(request):
    # todos = Todo.objects.all()
    return render(request, "home.html")
