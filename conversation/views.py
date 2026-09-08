from django.shortcuts import render, get_object_or_404, redirect
from .models import ConversationRoom, ConversationMessage
from accounts.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required(login_url='login')
def create_conversation(request, pk):
    other_user = User.objects.get(id=pk)
    user = request.user
    room = ConversationRoom.objects.filter(participants__id=request.user.id
                                           ).filter(participants__id=pk).first()
    if room is None:
        room = ConversationRoom.objects.create(
            created_by=user
        )
        room.participants.add(user, other_user)
    return redirect('conversation', room.id)

@login_required(login_url='login')
def delete_conversation(request, pk):
    conversation_room = get_object_or_404(ConversationRoom, id=pk)
    if request.method == 'POST':
        conversation_room.delete()
        return redirect('home')
    context = {'obj': conversation_room}
    return render(request, 'delete.html', context)

@login_required(login_url='login')
def delete_conversation_message(request, pk):
    conversation_message = get_object_or_404(ConversationMessage, id=pk)
    if request.method == 'POST':
        conversation_message.delete()
        return redirect('conversation', conversation_message.room.id)
    context = {'obj': conversation_message}
    return render(request, 'delete.html', context)

@login_required(login_url='login')
def conversation_page(request, pk):
    room = ConversationRoom.objects.get(id=pk)
    if request.method == 'POST' and request.POST.get('body', None):
        ConversationMessage.objects.create(
            owner = request.user,
            room = room,
            body = request.POST.get('body')
        )
        return redirect('conversation', pk=pk)
    messages = room.message.all()
    context = {'messages': messages, 'conversation_room': room}
    return render(request, 'chat.html', context)

@login_required(login_url='login')
def all_messages(request, pk):

    user = get_object_or_404(User, id=pk)
    query = request.GET.get('query', '')
    conversation_rooms = ConversationRoom.objects.filter(
        participants=user
    )
    conversation_rooms = conversation_rooms.filter(
        Q(participants__username__icontains=query) |
        Q(participants__first_name__icontains=query) |
        Q(participants__last_name__icontains=query)
    ).distinct()

    context = {'conversations': conversation_rooms}
    print(conversation_rooms)
    return render(request, 'conversations.html', context)