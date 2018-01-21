from django.shortcuts import render
from .models import Boards


def home(request):
    boards = Boards.objects.all()
    return render(request, 'home.html', {'boards': boards})
