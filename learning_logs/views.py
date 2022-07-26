from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Entry, Topic
from .forms import TopicForm, EntryForm

def index(request):
    '''Домашняя страница приложения Learning Log'''
    return render(request, 'learning_logs/index.html')


@login_required
def topics(request):
    '''Страница с темами'''
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    public_topics = Topic.objects.filter(public=True).order_by('date_added')
    context = {'topics': topics, 
        'public_topics': public_topics
        }
    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    '''Выводит одну тему и все ее записи'''
    topic = get_object_or_404(Topic, id=topic_id)
    # Проверка того, что тема принадлежит текущему пользователю
    if topic.owner != request.user and topic.public == False:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 
        'entries': entries
        }
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    '''Определяет новую тему'''
    if request.method !=  'POST':
        # Данные не отправлялись, создается пустая форма
        form = TopicForm()
    else:
        # Отправлены данные POST; обработать данные
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('topics'))
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def delete_topic(request, topic_id):
    '''Удаляет тему'''
    topic = get_object_or_404(Topic, id=topic_id)
    if topic.owner != request.user:
        raise Http404
    else:
        topic.delete()
    return HttpResponseRedirect(reverse('topics'))


@login_required
def new_entry(request, topic_id):
    '''Определяет новую запись по конкретной теме'''
    topic = get_object_or_404(Topic, id=topic_id)
    if topic.owner != request.user:
        raise Http404
    if request.method !=  'POST':
        # Данные не отправлялись, создается пустая форма
        form = EntryForm()
    else:
        # Отправлены данные POST; обработать данные
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('topic', args=[topic_id]))
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    '''Редактирует существующую запись'''
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic
    # Проверка того, что запись принадлежит текущему пользователю
    if topic.owner != request.user:
        raise Http404
    if request.method !=  'POST':
        # Исходный запрос, форма заполняется данными текущей записи
        form = EntryForm(instance=entry)
    else:
        # Отправлены данные POST; обработать данные
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topic', args=[topic.id]))
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
