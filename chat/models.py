from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField(_('first name'), max_length=150, null=False, blank=False)

    def __str__(self):
        return self.username


class Group(models.Model):
    name = models.CharField(max_length=300, unique=True)
    about = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(to=User, related_name="chat_groups", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class GroupMember(models.Model):
    group = models.ForeignKey(to=Group, related_name="group_members", on_delete=models.CASCADE)
    member = models.ForeignKey(to=User, related_name="group_members", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('group', 'member')

    def __str__(self):
        return f"{self.group.name} - {self.member.username}"


class Message(models.Model):
    message = models.TextField()
    sender = models.ForeignKey(to=GroupMember, related_name="messages", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.member.username} - {self.message}"


class Like(models.Model):
    message = models.ForeignKey(to=Message, related_name="likes", on_delete=models.CASCADE)
    member = models.ForeignKey(to=GroupMember, related_name="liked_messages", on_delete=models.CASCADE)
    like = models.BooleanField(default=True)

    class Meta:
        unique_together = ('message', 'member')

    def __str__(self):
        return f"{self.message.message} - {self.like}"
