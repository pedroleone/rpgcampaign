from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from campaign.models import *
from forum.models import *
from forum.forms import *
from forum.models import *
from campaign.views import get_campaigns, get_permission, user_in_campaign


@login_required(login_url='/login/')
@user_in_campaign
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
@user_in_campaign
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
            elif request.POST.get('redirect') == 'session':
                return HttpResponseRedirect(reverse('view_session', args=[campaign.slug, topic.linked_session.id]))    
            else:
                return HttpResponseRedirect(reverse('view_topic', args=[campaign.slug, topic.id]))
    return render(request, 'forum/view_topic.html', context=context)

@login_required(login_url='/login/')
@user_in_campaign
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

@login_required(login_url='/login/')
@user_in_campaign
def edit_message(request, slug, topic_id, message_id):
    context = { 'campaign_list': get_campaigns(request) }
    campaign = get_object_or_404(Campaign, slug=slug)
    permission = get_permission(request, campaign)
    context['permission'] = permission
    user = get_object_or_404(User, username=request.user)
    context['campaign'] = campaign
    topic = get_object_or_404(Topic, id=topic_id)
    message = get_object_or_404(TopicMessage, id=message_id)
    if (message.author != request.user) and permission == 2:
         return render(request, 'denied.html', context=context)

    first_message=TopicMessage.objects.filter(topic=topic).first()
    if message == first_message:
        data = {
            'title': topic.title,
            'message': message.text
        }
        form = AddTopicForm(request.POST or data)
        if request.method == "POST":
            if form.is_valid():
                topic.title = form.cleaned_data['title']
                message.text = form.cleaned_data['message']
                message.edited = True 
                message.save()
                topic.save()
                print(topic, message)
            if request.POST.get('redirect') == 'main':
                return HttpResponseRedirect(reverse('view_campaign', args=[campaign.slug]))    
            elif request.POST.get('redirect') == 'session':
                return HttpResponseRedirect(reverse('view_session', args=[campaign.slug, topic.linked_session.id]))    
            else:
                return HttpResponseRedirect(reverse('view_topic', args=[campaign.slug, topic.id]))        
        else:
            context['form'] = form
            return render(request, 'forum/edit_topic.html', context)
    else:
        form = AddMessageForm(request.POST or {'message': message.text})
        if request.method == "POST":
            if form.is_valid():
                message.text = form.cleaned_data['message']
                message.edited = True 
                message.save()
            if request.POST.get('redirect') == 'main':
                return HttpResponseRedirect(reverse('view_campaign', args=[campaign.slug]))    
            elif request.POST.get('redirect') == 'session':
                return HttpResponseRedirect(reverse('view_session', args=[campaign.slug, topic.linked_session.id]))    
            else:
                return HttpResponseRedirect(reverse('view_topic', args=[campaign.slug, topic.id]))        
        else:
            context['form'] = form
            return render(request, 'forum/edit_topic.html', context)

@login_required(login_url='/login/')
@user_in_campaign
def new_topic_from_session(request, slug, session_id):
    session = get_object_or_404(Session, id=session_id)
    campaign = get_object_or_404(Campaign, slug=slug)
    form = AddMessageSmallForm(request.POST or None)
    if request.method=="POST":
        if form.is_valid():
            topic=Topic(author=request.user, campaign=campaign, title="Sessão "+str(session.date), linked_session=session)
            topic.save()
            message = TopicMessage(topic=topic, author=request.user,text=form.cleaned_data['message'])
            message.save()
            if request.POST.get('redirect') == 'main':
                return HttpResponseRedirect(reverse('view_campaign', args=[campaign.slug]))    
            elif request.POST.get('redirect') == 'session':
                return HttpResponseRedirect(reverse('view_session', args=[campaign.slug, session.id]))    
            else:
                return HttpResponseRedirect(reverse('view_topic', args=[campaign.slug, topic.id]))
    else:
        context = { 'campaign_list': get_campaigns(request) }
        campaign = get_object_or_404(Campaign, slug=slug)
        context['permission'] = get_permission(request, campaign)
        user = get_object_or_404(User, username=request.user)
        context['campaign'] = campaign
        context['form'] = form
        context['session'] = session
        return render(request, 'forum/new_topic_from_session.html', context)
