from django.urls import path, include
from . import views


urlpatterns = [
    # path('login/', user_login, name="login"),
    path("login/", views.NewLoginView.as_view(), name="login"),
    path("logout/", views.NewLogoutView.as_view(), name="logout"),
    path('password_change/', views.NewPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', views.NewPasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', views.NewPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.NewPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.NewPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done', views.NewPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/edit', views.edit_profile, name='profile_edit'),
    path('registration/', views.registration, name='registration'),
    path('profile/', views.home, name='home'),
    path('', views.home, name='home'),
    path('people/', views.people, name='people'),
    path("api/v1/follow", views.FollowAPIView.as_view())
]
