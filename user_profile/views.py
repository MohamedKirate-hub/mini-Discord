from django.shortcuts import render, redirect
from accounts.models import User
from core.models import Topic
from django.db.models import Q
from core.models import Room
from .forms import UserForm

def profile_view(request, pk):
    query = request.GET.get('query', '')
    topic_id = request.GET.get('topic', '')
    user = User.objects.get(id=pk)
    topics = Topic.objects.all()
    created_rooms = Room.objects.filter(host = user).filter(Q(name__icontains=query) |
                                                            Q(description__icontains=query) |
                                                            Q(topic__name__icontains=query) |
                                                            Q(host__username__icontains=query))

    joined_rooms = Room.objects.filter(participants__in=[request.user.id])
    joined_rooms = joined_rooms.exclude(host__id=user.id).filter(Q(name__icontains=query) |
                                                            Q(description__icontains=query) |
                                                            Q(topic__name__icontains=query) |
                                                            Q(host__username__icontains=query))
    if topic_id:
        created_rooms = created_rooms.filter(topic__id=topic_id)
        joined_rooms = joined_rooms.filter(topic__id=topic_id)

    context = {'user': user, 'rooms': created_rooms,
                'joined_rooms': joined_rooms,
                'topics': topics}
    return render(request, 'profile.html', context)

def update_profile_view(request, pk):
    user = User.objects.get(id=pk)
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk)
    context = {'form': form}
    return render(request, 'edite.html', context)