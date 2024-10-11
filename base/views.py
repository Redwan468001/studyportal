from django.shortcuts import render, get_object_or_404, redirect
from . models import Room, Topic
from . forms import CreateRoom

# Create your views here.
def home(request):
    rooms = Room.objects.all();
    topics = Topic.objects.all();
    context = {
        'rooms': rooms,
        'topics': topics,
    }
    return render(request, 'home.html', context);


def room(request, id):
    sng_room = get_object_or_404(Room, id=id)
    context = {
        'sng_room': sng_room,
    }
    return render(request, 'room.html', context);


def topic(request, id):
    topics = Topic.objects.all()
    sng_topic = get_object_or_404(Topic, id=id)
    sng_rooms = Room.objects.filter(topic=sng_topic)
    context = {
        'sng_topic': sng_topic,
        'sng_rooms': sng_rooms,
        'topics': topics,
    }
    return render(request, 'topics.html', context);


def createroom(request):
    form = CreateRoom()
    if request.method == "POST":
        form = CreateRoom(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home')
    context = {
        'form': form,
    }
    return render(request, 'room_form.html', context)


def editroom(request, id):
    room = get_object_or_404(Room, id=id)
    if request.method == "POST":
        form = CreateRoom(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CreateRoom(instance=room)
    context = {
        'form': form
    }
    return render(request, 'room_form.html', context)
    
