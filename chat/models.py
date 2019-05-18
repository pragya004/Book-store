from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# we do the work related to databases here

class DirectChat(models.Model):
    
    sender     = models.ForeignKey(User, related_name='chat_sender', on_delete=models.CASCADE)
    receiver   = models.ForeignKey(User, related_name='chat_receiver', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Conversation: sender: {} receiver: {}".format(self.sender.username, self.receiver.username)

class Group(models.Model):
    
    name        = models.CharField(max_length=200)
    description = models.TextField(default="Group Description")
    creator     = models.ForeignKey(User, related_name='group_creator', on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    member      = models.ManyToManyField(User, related_name='group_member')

    def __str__(self):
        return "Group name: {}, creator: {}".format(self.name, self.creator.username)


class DirectMessage(models.Model):

    direct_chat = models.ForeignKey(DirectChat, on_delete=models.CASCADE)
    message     = models.TextField()
    sender      = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

class GroupMessage(models.Model):
    
    group_chat  = models.ForeignKey(Group, on_delete=models.CASCADE)
    message     = models.TextField()
    sender      = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

