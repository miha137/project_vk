from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
import vk
from django.contrib.auth.models import User

def home(request):
    if request.user in User.objects.all():
        user = request.user
        usr_name = " ".join([user.first_name, user.last_name])
        token = user.social_auth.first().extra_data['access_token']
        uid = user.social_auth.first().uid

        session = vk.Session(access_token=token)
        vkapi = vk.API(session)
        friends_ids = vkapi.friends.get(user_id=uid, v=2, count=5)
        friends = []
        for friend_id in friends_ids:
            person = vkapi.users.get(user_id=friend_id, v=2)
            name = " ".join([person[0]['first_name'], person[0]['last_name']])
            friends.append(name)
        context = {'friends': friends, 'name': usr_name}
    else:
        context = {}
    return render(request, 'home.html', context)

def logout(request):
    auth_logout(request)
    return redirect('/')
