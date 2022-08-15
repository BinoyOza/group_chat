from django.contrib import admin

from chat.models import User, Group, GroupMember, Message, Like


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'is_admin',)
    ordering = ('-id',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'about', 'created_by', 'created_at',)
    ordering = ('-id',)


@admin.register(GroupMember)
class GroupMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'group', 'member',)
    ordering = ('-id',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'sender', 'timestamp')
    ordering = ('-timestamp',)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'member', 'like')
