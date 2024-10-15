from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from . models import Room, Topic, Message
from . forms import CreateRoom, CreateMessage

# Create your views here.
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else '';
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        );
    topics = Topic.objects.all();
    room_count = rooms.count();
    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
    }
    return render(request, 'home.html', context);


# Display Room
def room(request, id):
    sng_room = get_object_or_404(Room, id=id);
    message = Message.objects.filter(room=sng_room);
    context = {
        'sng_room': sng_room,
        'message': message,
    }
    return render(request, 'room.html', context);


# Display Topic
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


# Create Room
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


# Edit Room
def editroom(request, id):
    room = get_object_or_404(Room, id=id)
    if request.method == "POST":
        form = CreateRoom(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('room', id=room.id)
    else:
        form = CreateRoom(instance=room)
    context = {
        'form': form
    }
    return render(request, 'room_form.html', context)
    

# Delete room
def deleteroom(request, id):
    room = get_object_or_404(Room, id=id)
    
    if request.method == "POST":
        room.delete()
        return redirect('home')
    
    return render(request, 'room_delete.html', {'room':room})


#Message 
def message(request, id):
    room = get_object_or_404(Room, id=id)
    form = CreateMessage()
    if request.method == "POST":
        form = CreateMessage(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.room = room
            msg.user = request.user
            msg.save()
            return redirect('room', id=room.id)
    context = {
        'form': form,
    }

    return render(request, 'room_form.html', context)