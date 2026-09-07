from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import RoomForm, ChannelForm
from .models import Room, Message, Channel, Topic
from django.db.models import Q

@login_required(login_url='login')
def create_room_view(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room = Room.objects.create(
            topic= topic,
            host = request.user,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
        room.participants.add(request.user)
        return redirect('home')
    context = {'form': form, 'topics': topics}
    return render(request, 'create_room.html', context)

@login_required(login_url='login')
def update_room_view(request, pk):
    room = get_object_or_404(Room, id=pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'update_room.html', context)

@login_required(login_url='login')
def delete_room_view(request, pk):
    room = get_object_or_404(Room, id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj': room}
    return render(request, 'delete.html', context)
    

def home_page(request):
    query = request.GET.get('query', '')
    topic_id = request.GET.get('topic', '')
    topics = Topic.objects.all()
    rooms = Room.objects.filter(Q(name__icontains=query) | Q(description__icontains=query) |
                                Q(topic__name__icontains=query) |
                                Q(host__username__icontains=query))
    if topic_id:
        rooms = Room.objects.filter(topic__id=topic_id)
    context = {'rooms': rooms, 'topics': topics}
    return render(request, 'home.html', context)

@login_required(login_url='login')
def room_page(request, pk):
    room = get_object_or_404(Room, id=pk)
    channels = room.channels.all()
    joined = Room.objects.filter(id=room.id).filter(participants__in=[request.user.id])
    if not joined:
        return HttpResponse('You have to join to this room.')
    context = {'room': room, 'channels': channels}
    return render(request, 'room.html', context)

@login_required(login_url='login')
def join_room(request, pk):
    room = get_object_or_404(Room, id=pk)
    room.participants.add(request.user)
    return redirect('room', pk)

@login_required(login_url='login')
def leave_room(request, pk):
    room = get_object_or_404(Room, id=pk)
    if (request.user in room.participants.all()):
        room.participants.remove(request.user)
    return redirect('home')

@login_required(login_url='login')
def channel_page(request, pk):
    channel = Channel.objects.get(id=pk)
    room = Room.objects.get(channels__id=channel.id)
    if (request.method == 'GET' and request.GET.get('body')):
        Message.objects.create(
            channel = channel,
            owner = request.user,
            body = request.GET.get('body'),
        )
        return redirect('channel', pk)
    messages = channel.message_set.all()
    context = {'room':room, 'messages': messages, 'channel': channel}
    return render(request, 'channel.html', context)

@login_required(login_url='login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)
    channel = message.channel
    message.delete()
    return redirect('channel', channel.id)    

@login_required(login_url='login')
def create_channel(request, pk):
    form = ChannelForm()
    room = get_object_or_404(Room, id=pk)
    if request.method == 'POST':
        form = ChannelForm(request.POST)
        if form.is_valid():
            channel = form.save()
            room.channels.add(channel)
            return redirect('room', pk)

    context = {'form': form}
    return render(request, 'create.html', context)

@login_required(login_url='login')
def delete_channel(request, pk):
    channel = Channel.objects.get(id=pk)
    room = Room.objects.get(channels__id=pk)
    if request.method == 'POST':
        channel.delete()
        return redirect('room', room.id)
    return redirect('room', room.id)

@login_required(login_url='login')
def update_channel(request, pk):
    channel = Channel.objects.get(id=pk)
    room = Room.objects.get(channels__id=pk)
    form = ChannelForm(instance=channel)

    if request.method == 'POST':
        form = ChannelForm(request.POST, instance=channel)
        if form.is_valid():
            form.save()
            return redirect('room', room.id)

    context = {'form': form, 'room': room}
    return render(request, 'update_channel.html', context)
