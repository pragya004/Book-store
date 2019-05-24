from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json

def chat_index_direct(request):
    #to render the initial page
    if request.user.pk == None:
        return redirect('login')
    
    context = {"user_details": request.user}
    
    return render(request,"chat/chat_index_direct.html", context)

def chat_index_group(request):
    #to render the initial page
    if request.user.pk == None:
        return redirect('login')
    
    context = {"user_details": request.user}

    return render(request,"chat/chat_index_group.html", context)


def chat_create_group(request):
    #creates a group
    if request.method == "GET":
        return render(request,"chat/create_group.html")
    elif request.method == "POST":
        user              = User.objects.get(pk=request.user.pk)
        group_name        = request.POST["group-name"]
        group_description = request.POST["group-description"]
        group = Group(name=group_name, description=group_description, creator=user)
        group.save()
        group.member.add(user) 
        group.save()

        return redirect("chat_index_group_url")

def get_users(request):
    #shows all users in the side panel
    users = User.objects.exclude(id=request.user.pk) 
    data = {"user_names": [{"username": user.username, "id": user.id} for user in users]}
    data_json = json.dumps(data)
    return HttpResponse(data_json, content_type="application/json")


def get_groups(request):
    #shows all groups in the side panel
    groups = Group.objects.all()
    data = {"group_details": [{"name": group.name, "description": group.description, "id": group.id} for group in groups]}
    data_json = json.dumps(data)
    return HttpResponse(data_json, content_type="application/json")



def get_direct_conversation(request):
    # checks is direct chat exists or not between user1 and user 2
    
    idx = request.GET["id"]
    
    user1 = User.objects.get(pk=request.user.pk)
    user2 = User.objects.get(pk=idx)

    conv1 = DirectChat.objects.filter(sender=user1).filter(receiver=user2)#returns number of items in
    conv2 = DirectChat.objects.filter(sender=user2).filter(receiver=user1) #the list

    
    if conv1.count() and not conv2.count():
        data = {"conv_id": conv1[0].id}
    elif not conv1.count() and conv2.count():
        data = {"conv_id": conv2[0].id}
    else:
        conv = DirectChat(sender=user1,receiver=user2)
        conv.save()
        data = {"conv_id": conv.id}


    data_json = json.dumps(data)

    return HttpResponse(data_json, content_type="application/json")


def adduser_to_group(request):

    group = Group.objects.get(pk=int(request.GET["id"]))
    #checks in terminal
    if request.user not in group.member.all():
        print("Not Present")
    else:
        print("present")

    data = {"status": "successfully added to to group"}

    data_json = json.dumps(data)

    return HttpResponse(data_json, content_type="application/json")

@csrf_exempt
def messages(request):
#gets the convo id and shows all the messages corresponding it.
    if request.method == "GET":
        if request.GET["type"] == "1":

            conv     = DirectChat.objects.get(pk=int(request.GET["conv_id"]))
            messages = DirectMessage.objects.filter(direct_chat=conv)

        else:
            conv     = Group.objects.get(pk=int(request.GET["conv_id"]))
            messages = GroupMessage.objects.filter(group_chat=conv)

        data      = {   "logged_in_user": request.user.id, 
                        "messages": [{  "user_id": m.sender.id, 
                                        "user_name": m.sender.username, 
                                        "message": m.message} for m in messages]
                    }

        data_json = json.dumps(data)

        return HttpResponse(data_json, content_type="application/json")
#saves the messages that users send to the database
    elif request.method == "POST":
        
        sender = User.objects.get(pk=request.user.id)  
        data = json.loads(request.body)

        if data["type"] == "1":

            direct_chat = DirectChat.objects.get(pk=int(data["conversation"]))
            message     = DirectMessage(sender=sender, direct_chat=direct_chat, message=data["body"])
            message.save()

        else:

            group_chat  = Group.objects.get(pk=int(data["conversation"]))
            message     = GroupMessage(sender=sender, group_chat=group_chat, message=data["body"])
            message.save()
    
        data      = {"status": "message created successfully"}
        data_json = json.dumps(data)

        return HttpResponse(data_json, content_type="application/json")

