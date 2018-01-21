from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import Boards, Topic, Post


def home(request):
    boards = Boards.objects.all()
    return render(request, 'home.html', {'boards': boards})


def board_topics(request, board_primary_key):
    board = get_object_or_404(Boards, pk=board_primary_key)
    return render(request, 'topics.html', {'board': board})


def new_topic(request, board_primary_key):
    board = get_object_or_404(Boards, pk=board_primary_key)

    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']

        user = User.objects.first()

        topic = Topic.objects.create(
            subjects=subject,
            board=board,
            starter=user
        )

        post = Post.objects.create(
            message=message,
            topic=topic,
            created_by=user
        )

        return redirect('board_topics', board_primary_key=board.pk)

    return render(request, 'new_topic.html', {'board': board})