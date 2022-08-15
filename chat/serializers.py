from rest_framework import serializers
from .models import User, Group, GroupMember, Message, Like


class UserSerializer(serializers.ModelSerializer):
    """
    User Serializer for create and update user.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'is_admin', 'username', 'password']

    def create(self, validated_data):
        account = super(UserSerializer, self).create(validated_data)
        account.set_password(validated_data["password"])
        account.save()
        return account

    def update(self, instance, validated_data):
        first_name = validated_data.get("first_name", None)
        last_name = validated_data.get("last_name", None)
        email = validated_data.get("email", None)
        is_admin = validated_data.get("is_admin", None)
        username = validated_data.get("username", None)

        instance.first_name = first_name if first_name else instance.first_name
        instance.last_name = last_name if last_name else instance.last_name
        instance.email = email if email else instance.email
        instance.is_admin = is_admin if is_admin is not None else instance.is_admin
        instance.username = username if username else instance.username

        if validated_data.get("password"):
            instance.set_password(validated_data["password"])
        instance.save()
        return instance


class UserResponseSerializer(serializers.ModelSerializer):
    """
    User model serializer to fetch all the fields of user on get request.
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'email', 'is_admin']


class GroupSerializer(serializers.ModelSerializer):
    """
    Group model serializer for Create operation.
    """

    class Meta:
        model = Group
        fields = ['name', 'about', 'created_by']

    def create(self, validated_data):
        account = super(GroupSerializer, self).create(validated_data)
        account.save()
        return account


class GroupResponseSerializer(serializers.ModelSerializer):
    """
    Group model serializer for fetching all the details on get request.
    """

    class Meta:
        model = Group
        fields = "__all__"


class GroupMemberSerializer(serializers.ModelSerializer):
    """
    GroupMember serializer to Add, Get and Delete Members to Group.
    """
    group_name = serializers.ReadOnlyField(source='group.name')
    member_name = serializers.ReadOnlyField(source='member.username')

    class Meta:
        model = GroupMember
        fields = "__all__"

    def create(self, validated_data):
        group_member = super(GroupMemberSerializer, self).create(validated_data)
        group_member.save()
        return group_member


class MessageSerializer(serializers.ModelSerializer):
    """
    Message model Serializer to support Create and Get Message objects.
    """
    sender_name = serializers.ReadOnlyField(source='sender.member.username')

    class Meta:
        model = Message
        fields = "__all__"

    def create(self, validated_data):
        message = super(MessageSerializer, self).create(validated_data)
        message.save()
        return message


class LikeMessageSerializer(serializers.ModelSerializer):
    """
    Like model serializer to Create and Get details of liked message objects.
    """
    member_name = serializers.ReadOnlyField(source='member.member.username')
    message_text = serializers.ReadOnlyField(source='message.message')

    class Meta:
        model = Like
        fields = "__all__"

    def create(self, validated_data):
        like_message = super(LikeMessageSerializer, self).create(validated_data)
        like_message.save()
        return like_message
