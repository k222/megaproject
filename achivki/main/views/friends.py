# -*- coding: utf-8 -*-
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from achivki.main.models import UserFriends
from django.shortcuts import  render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from smtplib import SMTPException
from django.http import Http404
from django.contrib.auth.decorators import login_required

@login_required()
def show_friends(request, username):
    search_friends = request.POST.get('search_friends',"")
    friends=[]
    if request.user.is_authenticated():
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404
        #user = User.objects.get(id=request.user.id)

        friendsList = UserFriends.objects.filter(user=user)

        #isfriends = UserFriends.objects.all()
        if (friendsList):
            for friendEl in friendsList:
                try:
                    friend = User.objects.get(id=friendEl.friends.id, username__contains=search_friends)
                    already_friend = False
                    my_profile = False
                    if request.user.is_authenticated():
                        already_friend =  is_friend(request.user, friend)
                        my_profile = (friend.username == request.user.username)
                    friend_hash = {'is_authenticated' : friend.is_authenticated(),
                                   'name' : friend.username,
                                   'gravatar_url' : friend.get_profile().get_gravatar_url(),
                                   'already_friend' : already_friend,
                                   'my_profile':my_profile
                    }
                    friend_hash.update(csrf(request))
                    friends.append (friend_hash)
                except User.DoesNotExist:
                    pass


    context = {
        'is_authenticated' : request.user.is_authenticated(),
        'friends' : friends,
        'search_friends' : search_friends,
        'profile_name' : user.username,
        'gravatar_url' : user.get_profile().get_gravatar_url(),
        'empty_text': _(u"Друзей по Вашему запросу не найдено") if(search_friends)
                     else _(u"У %(name)s пока нет друзей" % {'name':user.username}),
        'search_word': request.POST.get('search_word',""),
        'show_friends_filter': True,
        'actfriends':True,
        'my_username':request.user.username
    }
    return render_to_response("friends.html", context)

@login_required()
def search_friends(request):

    users=[]
    search_word = request.POST.get('search_word',"")
    search_word = "" if(search_word == _(u'Поиск людей')) else search_word
    #user_id= request.user.id if request.user.is_authenticated() else 0
    userList = User.objects.filter(username__contains=search_word)
    if(request.user.is_authenticated()):
        userList =userList.exclude(id=request.user.id)
    for userEl in userList:
        already_friend = False
        if request.user.is_authenticated():
            already_friend =  is_friend(request.user, userEl)
        user_hash = {'is_authenticated' : userEl.is_authenticated(),
                     'name' : userEl.username,
                     'gravatar_url' : userEl.get_profile().get_gravatar_url(),
                     'already_friend' : already_friend

                    }
        user_hash.update(csrf(request))
        users.append (user_hash)

    context = {
        'is_authenticated' : True,
        'friends' : users,
        'search_word' : search_word,
        'profile_name' : request.user.username if request.user.is_authenticated() else "",
        'gravatar_url' : request.user.get_profile().get_gravatar_url() if request.user.is_authenticated() else "",
        'empty_text': _(u"По вашему запросу ничего не найдено"),
        'show_friends_filter': False,
        'my_username':request.user.username
    }
    context.update(csrf(request))
    return render_to_response("friends.html", context)

@login_required()
def add_friends(request):
    profilename = request.POST.get('profile_name',"")
    error = u"success"
    if (profilename):
        if request.user.is_authenticated():
            user = User.objects.get(id=request.user.id)
            friend = User.objects.get(username=profilename)
            is_friend_vr  = is_friend(user, friend)

            if (not is_friend_vr):
                uf = UserFriends(user=user,friends=friend)
                msg = _(u" Пользователь %(name)s  добавил Вас в друзья на сайте TickIt," \
                        u" Вы можете добавить его в друзья, воспользовавшись поиском, или на" \
                        u" странице его профиля: http://host6640.hnt.ru/%(name)s " % {'name':user.username})
                topic = _(u" Вас добавили в друзья TickIt")
                try:
                    send_mail(topic, msg, 'tickit@bk.ru', [friend.email])
                    #send_mail(topic, msg, 'tickit@bk.ru', ['Ann1137@ya.ru'])
                    uf.save()
                except SMTPException:
                   error = _(u"Не удаётся отправить письмо-оповещение. Пожалуйста, попробуйте позже.")
            else:
                error=u"Пользователь уже у Вас в друзьях"
        else:
            error=u"Вы не авторизованы"
    else:
        error=u"Имя друга не задано"
    if(request.method == "POST"):
        return HttpResponse(error)
    else:
        return HttpResponseRedirect(request.user.username+"/friends")
    #return render_to_response('friends.html', error)
    #show_friends(request)

@login_required()
def delete_friends(request):
    profilename = request.POST.get('profile_name',"")
    error = "success"
    if (profilename):
        if request.user.is_authenticated():
            user = User.objects.get(id=request.user.id)
            friend = User.objects.get(username=profilename)
            is_friend_vr = is_friend(user, friend)

            if (is_friend_vr):
                uf = UserFriends.objects.get(user=user,friends=friend)
                uf.delete()
                if(is_friend(friend, user)):
                    fu = UserFriends.objects.get(user=friend,friends=user)
                    fu.delete()
            else:
                error="Пользователь уже удален из друзей"
        else:
            error="Вы не авторизованы"
    else:
        error="Имя друга не задано"
    if(request.method == "POST"):
        return HttpResponse(error)
    else:
        return HttpResponseRedirect(request.user.username+"/friends")

def is_friend(user_obj, friend_obj):
    is_friend = False
    try:
        is_friend = UserFriends.objects.get(user=user_obj, friends=friend_obj)
    except UserFriends.DoesNotExist:
        is_friend = False
    already_friend = True if is_friend else False
    return already_friend

