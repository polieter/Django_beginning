from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import Boards, Topic, Post
from .forms import NewTopicForm


def home(request):
    boards = Boards.objects.all()
    return render(request, 'home.html', {'boards': boards})


def board_topics(request, board_primary_key):
    board = get_object_or_404(Boards, pk=board_primary_key)
    return render(request, 'topics.html', {'board': board})


@login_required
def new_topic(request, board_primary_key):
    board = get_object_or_404(Boards, pk=board_primary_key)
    user = User.objects.first()

    if request.method == 'POST':
        form = NewTopicForm(request.POST)

        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()

            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
            return redirect('board_topics', board_primary_key=board.pk)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})