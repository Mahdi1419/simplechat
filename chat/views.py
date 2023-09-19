from django.shortcuts import render, redirect
from .models import Topic
# Create your views here.


def index(request):
    user = request.user
    print(user)
    if not user.is_authenticated:
        return redirect(to='/admin')
    topics = Topic.objects.filter(users=user)

    context = {"topics": topics}

    return render(request, 'chat/index.html', context=context)


def room(request, room_name):
    user = request.user
    print(user)
    if not user.is_authenticated:
        return redirect(to='/admin')
    return render(request, 'chat/room.html', context={"room_name":room_name})


