import json

from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from django.db import IntegrityError

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, GroupMember, Group, Message, Like
from .permissions import IsAdminPermission, IsNormalPermission
from .serializers import UserSerializer, GroupSerializer, GroupResponseSerializer, UserResponseSerializer, \
    GroupMemberSerializer, MessageSerializer, LikeMessageSerializer


class UserAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminPermission]

    def post(self, request):
        """
        API to create user. Only Admin(is_admin=True) users can create users.
        """
        try:
            data = dict()
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                account = serializer.save()
                account.is_active = True
                account.save()
                token = Token.objects.get_or_create(user=account)[0].key
                data["message"] = "User registered successfully."
                data["email"] = account.email
                data["username"] = account.username
                data["token"] = token
            else:
                data = serializer.errors
            return Response(data)

        except IntegrityError as e:
            account = User.objects.get(username='')
            account.delete()
            raise ValidationError({"400": f'{str(e)}'})

        except KeyError as e:
            raise ValidationError({"400": f'Field {str(e)} missing'})

    def put(self, request, pk):
        """
        API to update user. Only Admin(is_admin=True) users can update users.
        """
        account = User.objects.get(id=pk)
        serializer = UserSerializer(data=request.data, instance=account, partial=True)
        if serializer.is_valid():
            _ = serializer.save()
            response = Response(
                serializer.data, status=status.HTTP_201_CREATED)
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Login API which returns a token, which can be used across all the APIs as authentication.
        """
        data = {}
        username = request.data['username']
        password = request.data['password']
        try:
            account = User.objects.get(username=username)
        except BaseException as e:
            raise ValidationError({"400": f'{str(e)}'})

        token = Token.objects.get_or_create(user=account)[0].key
        if not check_password(password, account.password):
            raise ValidationError({"message": "Incorrect Login credentials"})

        if account:
            if account.is_active:
                login(request, account)
                data["message"] = "User logged in"
                data["username"] = account.username

                response = {"data": data, "token": token}

                return Response(response)

            else:
                raise ValidationError({"400": f'Account not active'})
        else:
            raise ValidationError({"400": f'Account doesnt exist'})


class UserLogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Logout API which on call deletes the generated token for the user.
        """
        request.user.auth_token.delete()

        logout(request)
        return Response('User Logged out successfully')


def get_serializer_errors_list(errors):
    return {'errors': [{key: val} for key, val in errors.items()]}


class GroupAPIView(APIView):
    permission_classes = [IsAuthenticated, IsNormalPermission]

    def get(self, request):
        """
        API for fetching the details of the Group.
        """
        groups = Group.objects.all()
        serializer = GroupResponseSerializer(groups, many=True)
        response = dict()
        response['groups'] = serializer.data
        response['success'] = True
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        """
        API for creating the Group.
        """
        request.data["created_by"] = request.user.id
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            group = serializer.save()
            GroupMember.objects.create(group=group, member=request.user)
            response = Response(
                serializer.data, status=status.HTTP_201_CREATED)
            return response
        response = get_serializer_errors_list(serializer.errors)
        response = Response(response,
                            status=status.HTTP_400_BAD_REQUEST)
        response.data.update({"success": False})
        return response

    def delete(self, request, pk, format=None):
        """
        API for deleting a Group.
        """
        group = Group.objects.filter(id=pk)
        if not group:
            return Response(data={"error": f"Group with {pk} id does not exist."},
                            status=status.HTTP_400_BAD_REQUEST)
        group.delete()
        return Response(status=status.HTTP_200_OK)


class SearchMemberAPIView(APIView):
    permission_classes = [IsAuthenticated, IsNormalPermission]

    def get(self, request):
        """
        API for searching all the Normal users. It has 2 filters username and first_name.
        """
        users = User.objects.exclude(is_admin=True)
        if request.query_params.get("username"):
            users = users.filter(username__startswith=request.query_params.get("username"))
        if request.query_params.get("first_name"):
            users = users.filter(first_name__startswith=request.query_params.get("first_name"))
        serializer = UserResponseSerializer(users, many=True)
        response = dict()
        response['users'] = serializer.data
        response['success'] = True
        return Response(response, status=status.HTTP_200_OK)


class GroupMemberAPIView(APIView):
    permission_classes = [IsAuthenticated, IsNormalPermission]

    def get(self, request):
        """
        API to fetch details of the Members of Group.
        """
        response = dict()
        groups = Group.objects.all()
        if request.query_params.get("group_id"):
            groups = groups.filter(id=int(request.query_params.get("group_id")))
        response["group_details"] = []
        for group in groups:
            group_members = GroupMember.objects.filter(group=group)
            serializer = GroupMemberSerializer(group_members, many=True)
            response["group_details"].append({"group_id": group.id,
                                              "member_details": serializer.data})
        response['success'] = True
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        """
        API for adding member to a group.
        """
        serializer = GroupMemberSerializer(data=request.data)
        if serializer.is_valid():
            group_member = serializer.save()
            data = {"details": {"id": group_member.id, "group": group_member.group.name,
                                "member": group_member.member.username},
                    "success": True
                    }
            response = Response(
                data, status=status.HTTP_201_CREATED)
            return response
        response = get_serializer_errors_list(serializer.errors)
        response = Response(response,
                            status=status.HTTP_400_BAD_REQUEST)
        response.data.update({"success": False})
        return response

    def delete(self, request):
        """
        API for removing a member from the Group.
        """
        group_member = GroupMember.objects.filter(group=request.data.get('group'), member=request.data.get("member"))
        if not group_member:
            return Response(data={"error": f"Either member does not exist or member is not in Group."},
                            status=status.HTTP_400_BAD_REQUEST)
        group_member.delete()
        return Response(status=status.HTTP_200_OK)


class MessageAPIView(APIView):
    permission_classes = [IsAuthenticated, IsNormalPermission]

    def get(self, request):
        """
        API for fetching the messages sent to the Group.
        """
        response = dict()
        groups = Group.objects.all()
        if request.query_params.get("group_id"):
            groups = groups.filter(id=int(request.query_params.get("group_id")))
        response["group_details"] = []
        for group in groups:
            group_members = GroupMember.objects.filter(group=group)
            messages = Message.objects.filter(sender__in=group_members).order_by("-timestamp")
            serializer = MessageSerializer(messages, many=True)
            response["group_details"].append({"group_id": group.id,
                                              "group_name": group.name,
                                              "message_details": serializer.data})
        response['success'] = True
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        """
        API to send message to the Group.
        """
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.save()
            data = {
                "details": {"id": message.id, "sender": message.sender.member.username, "timestamp": message.timestamp},
                "success": True
            }
            response = Response(
                data, status=status.HTTP_201_CREATED)
            return response
        response = get_serializer_errors_list(serializer.errors)
        response = Response(response,
                            status=status.HTTP_400_BAD_REQUEST)
        response.data.update({"success": False})
        return response


class LikeMessageAPIView(APIView):
    permission_classes = [IsAuthenticated, IsNormalPermission]

    def get(self, request):
        """
        API to fetch the details of members who liked the message.
        """
        response = dict()
        messages = Message.objects.all()
        if request.query_params.get("message_id"):
            messages = messages.filter(id=int(request.query_params.get("message_id")))
        response["like_details"] = []
        for message in messages:
            liked_messages = Like.objects.filter(message=message, like=True)
            serializer = LikeMessageSerializer(liked_messages, many=True)
            response["like_details"].append({"message_id": message.id,
                                             "message": message.message,
                                             "like_members": serializer.data})

        response['success'] = True
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        """
        API to like a message in the Group.
        """
        message = Message.objects.filter(id=request.data.get("message")).first()
        member = GroupMember.objects.filter(id=request.data.get("member")).first()
        if (not message) or (not member):
            return Response(data={"error": f"Either member or message does not exist for the Group."},
                            status=status.HTTP_400_BAD_REQUEST)
        like, created = Like.objects.get_or_create(message=message, member=member)
        if not created:
            like.like = not like.like
            like.save()
        serializer = LikeMessageSerializer(like)
        response = Response(
            serializer.data, status=status.HTTP_201_CREATED)
        return response
