from django.urls import path
from .views import UserAPIView, UserLoginAPIView, UserLogoutAPIView, GroupAPIView, SearchMemberAPIView, \
    GroupMemberAPIView, MessageAPIView, LikeMessageAPIView

urlpatterns = [
    # User Operations APIs.
    path('user-create', UserAPIView.as_view(), name='user-create'),
    path("user-update/<int:pk>/", UserAPIView.as_view(), name="user-update"),
    path('user-login', UserLoginAPIView.as_view(), name='user-login'),
    path('user-logout', UserLogoutAPIView.as_view(), name='user-logout'),

    # Group operations APIs.
    path('group-create', GroupAPIView.as_view(), name='group-create'),
    path("group-delete/<int:pk>/", GroupAPIView.as_view(), name="group-delete"),
    path("group-list", GroupAPIView.as_view(), name="group-list"),

    # Group Members operations APIs.
    path("search-member", SearchMemberAPIView.as_view(), name="search-member"),
    path("add-group-member", GroupMemberAPIView.as_view(), name="add-group-member"),
    path("view-group-member", GroupMemberAPIView.as_view(), name="view-group-member"),
    path("remove-group-member", GroupMemberAPIView.as_view(), name="remove-group-member"),

    # Group Message APIs.
    path("send-message", MessageAPIView.as_view(), name="send-message"),
    path("view-messages", MessageAPIView.as_view(), name="view-messages"),

    # Like Message APIs.
    path("like-message", LikeMessageAPIView.as_view(), name="like-message"),
    path("view-message-likes", LikeMessageAPIView.as_view(), name="view-message-likes")
]
