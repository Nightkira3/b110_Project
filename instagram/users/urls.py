from django.urls import path

from .views import (
    CustomLoginView, CustomLogoutView, SignupView,
    ProfileView, ProfileEditView, AddFriendView
)


app_name = 'users'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),

    path('profile/<int:user_id>/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileEditView.as_view(), name='edit_profile'),
    path('profile/<int:user_id>/add-remove-friend/',
         AddFriendView.as_view(),
         name='add_remove_friend'
         )
]
