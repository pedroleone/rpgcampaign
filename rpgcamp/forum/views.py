from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from campaign.models import *
from forum.models import *
from forum.forms import *
from forum.models import *
from campaign.views import get_campaigns, get_permission


@login_required(login_url='/login/')
def view_forum(request, slug):
    context = { 'campaign_list': get_campaigns(request) }
    campaign = get_object_or_404(Campaign, slug=slug)
    context['permission'] = get_permission(request, campaign)
    context['campaign'] = campaign
    topics_sessions = Topic.objects.filter(campaign=campaign, linked_session__isnull=False)
    topics = Topic.objects.filter(campaign=campaign, linked_session__isnull=True)
    context['topics'] = topics
    context['topics_sessions'] = topics_sessions
    return render(request, 'forum/view_forum.html', context=context)

@login_required(login_url='/login/')
def view_topic(request, slug, topic_id):
    context = { 'campaign_list': get_campaigns(request) }
    campaign = get_object_or_404(Campaign, slug=slug)
    context['permission'] = get_permission(request, campaign)
    context['campaign'] = campaign
    topic = get_object_or_404(Topic, id=topic_id)
    context['topic'] = topic
    form = AddMessageForm(request.POST or None)
    context['form'] = form
    if request.method == "POST":
        if form.is_valid():
            message = TopicMessage(topic=topic, author=request.user,text=form.cleaned_data['message'])
            message.save()
            if request.POST.get('redirect') == 'main':
                return HttpResponseRedirect(reverse('view_campaign', args=[campaign.slug]))    
            else:
                return HttpResponseRedirect(reverse('view_topic', args=[campaign.slug, topic.id]))
    return render(request, 'forum/view_topic.html', context=context)

@login_required(login_url='/login/')
def new_topic(request, slug):
    context = { 'campaign_list': get_campaigns(request) }
    campaign = get_object_or_404(Campaign, slug=slug)
    context['permission'] = get_permission(request, campaign)
    user = get_object_or_404(User, username=request.user)
    context['campaign'] = campaign

    if request.method == "POST":
        form = AddTopicForm(request.POST)
        if form.is_valid():
            topic = Topic(author=user,campaign=campaign,title=form.cleaned_data['title'])
            topic.save()
            message = TopicMessage(topic=topic, author=user,text=form.cleaned_data['message'])
            message.save()
            return HttpResponseRedirect(reverse('view_forum', args=[campaign.slug])) 
    else:
        form = AddTopicForm()
    context['form'] = form
    return render(request, 'forum/add_topic.html', context=context)


def edit_topic(request, slug, topic_id):
    pass
