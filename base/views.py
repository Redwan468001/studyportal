from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from . models import Room, Topic, Message
from . forms import CreateRoom, CreateMessage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

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
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'room_messages': room_messages,
    }
    return render(request, 'home.html', context);


# Display Room
def room(request, id):
    sng_room = get_object_or_404(Room, id=id);
    room_messages = Message.objects.filter(room=sng_room)
    participants = sng_room.participants.all();

    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=sng_room,
            body=request.POST.get('body'),
        )
        sng_room.participants.add(request.user)
        return redirect(room, id=sng_room.id);

    context = {
        'sng_room': sng_room,
        'room_messages': room_messages,
        'participants': participants,
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
@login_required(login_url='login')
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
@login_required(login_url='login')
def editroom(request, id):
    room = get_object_or_404(Room, id=id)

    if request.user != room.host:
        return HttpResponse('You are not allowed to update the room')

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
@login_required(login_url='login')
def deleteroom(request, id):
    room = get_object_or_404(Room, id=id)

    if request.user != room.host:
        return HttpResponse("You are not allowed to delete this room! ")
    
    if request.method == "POST":
        room.delete()
        return redirect('home')
    
    return render(request, 'room_delete.html', {'room':room})


#Message 
@login_required(login_url='login')
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



# Delete Message
def deletemessage(request, id):
    del_message = get_object_or_404(Message, id=id)

    if request.user != del_message.user:
        return HttpResponse('You are not allowed to delete the message!')
    
    if request.method == "POST":
        del_message.delete()
        return redirect('home');

    context = {
        'del_message': del_message
    }

    return render(request, 'delete_msg.html', context)


# Edit message
def editmessage(request, id):
    edit_msg = get_object_or_404(Message, id=id)
    pass


# Log in
def loginPage(request):

    page = '';

    if request.method == "POST":
        username = request.POST.get('username');
        password = request.POST.get('password');

        try:
            user = User.objects.get(username=username);
        except:
            messages.error(request, "User not found");

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user);
            return redirect('home')
        else:
            messages.error(request, "Username or Password does not match!")


    context = {

    }
    
    return render(request, 'login_page.html', context)


# Log out
def logoutview(request):
    logout(request)
    return redirect('login');

# Registration page
def registrationpage(request):

    forms = UserCreationForm()

    if request.method == "POST":
        forms = UserCreationForm(request.POST)
        if forms.is_valid():
            user = forms.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occur during registeration')


    context = {
        'forms': forms,
    }

    return render(request, 'registration_page.html', context)









