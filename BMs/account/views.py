from django.http import HttpResponse
from django.shortcuts import render
from .forms import LoginForm, NewAuthenticationForm, \
    NewPasswordChangeForm, NewPasswordResetForm, \
    UserRegistrationForm, ProfileEditForm, \
    UserEditForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from .models import Profile, Following

from rest_framework.decorators import APIView
from django.http import JsonResponse

from .serializators import FollowersSerializator

from actions.utils import create_action
from actions.models import Action

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username = cd['username'],
                                password = cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Авторизован")
                return HttpResponse("Учетная запись неактивна")
            return HttpResponse("Пользователь не найден")
        return HttpResponse("Ошибка в заполнении формы")
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {"form": form,
                                                  "page_name": "Авторизация"})

class NewLoginView(auth_views.LoginView):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(request.user.profile.get_absolute_uri())
        return super().dispatch(request, *args, **kwargs)
    extra_context = {"page_name": "Авторизация"}
    authentication_form = NewAuthenticationForm

class NewLogoutView(auth_views.LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        return super().dispatch(request, *args, **kwargs)
    extra_context = {"page_name": "Выход"}

class NewPasswordChangeView(auth_views.PasswordChangeView):
    extra_context = {"page_name": "Изменение пароля"}
    form_class = NewPasswordChangeForm

class NewPasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    extra_context = {"page_name": "Изменение пароля завершено"}
    
class NewPasswordResetView(auth_views.PasswordResetView):
    extra_context = {"page_name": "Сброс пароля"}

class NewPasswordResetDoneView(auth_views.PasswordResetDoneView):
    extra_context = {"page_name": "Сброс пароля"}

class NewPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    extra_context = {"page_name": "Сброс пароля"}
    form_class = NewPasswordResetForm

class NewPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    extra_context = {"page_name": "Сброс пароля завершен"}

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    user_profile = Profile.objects.select_related('user').prefetch_related('user__followers').get(user=user)
    return render(request, "account/profile/profile.html", {"page_name": "Профиль",
                                                            "page_type": "Профиль",
                                                            "user_profile": user_profile})

@login_required
def home(request):
    return redirect(request.user.profile.get_absolute_uri())

@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "GET":
        profile_form = ProfileEditForm(instance=profile)
        user_form = UserEditForm(instance=request.user)
        return render(request, 'account/profile/edit.html', {"page_name": "Редактирование профиля",
                                                             "page_type": "Профиль",
                                                            "profile_form": profile_form,
                                                             "user_form": user_form})
    if request.method == "POST":
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        user_form = UserEditForm(request.POST, instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            return redirect(request.user.profile.get_absolute_uri())

def registration(request):
    if request.user.is_authenticated:
        return redirect(request.user.profile.get_absolute_uri())
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_user = form.save(commit=False)
            new_user.set_password(cd['password'])
            new_user.save()
            new_user_profile = Profile(user=new_user)
            new_user_profile.save()
            return render(request, "account/registration_done.html", {"page_name": "Регистрация завершена"})
    else:
        form = UserRegistrationForm()
    return render(request, "account/registration.html", {"page_name": "Регистрация",
                                                         "form": form})

def people(request):
    users = User.objects.select_related('profile').filter(is_active=True)
    followings_to = Following.objects.filter(user_from = request.user).values_list('user_to', flat=True)
    actions = Action.objects.select_related('user').filter(user__in=followings_to)[:30]

    return render(request, 'people/people.html', {"page_name": "Сообщество",
                                                  "page_type": "Сообщество",
                                                  "users": users,
                                                  "actions": actions})

class FollowAPIView(APIView):
    def post(self, request):
        data = request.data
        action = data['action']
        follow_to = data['username']
        follower = request.user

        if action and follow_to:
            try:
                follow_to = User.objects.get(username=follow_to)
                if action == 'follow':
                    following = Following.objects.get_or_create(user_from = follower, user_to=follow_to)
                    create_action(request.user, 'подписался на', follow_to)
                else:
                    try:
                        following = Following.objects.get(user_from = follower, user_to = follow_to)
                        following.delete()
                        create_action(request.user, 'отписался от', follow_to)
                    except Following.DoesNotExist:
                        return JsonResponse({"status": "error"})
                serializator = FollowersSerializator(follow_to)
                return JsonResponse(serializator.data, status=200)
            except User.DoesNotExist:
                return JsonResponse({"status": "error"})
        return JsonResponse({"status": "error"})

    def get(self, request):
        data = request.query_params
        username = data['username']
        purpose = data['purpose']
        if username and purpose:
            try:
                user = User.objects.get(username=username)
                if purpose == "is_following":
                    response = request.user in user.followers.all()
                    return JsonResponse({"is_following": response})
                return JsonResponse({"status": "error"})
            except User.DoesNotExist:
                return JsonResponse({"status": "error"})
        return JsonResponse({"status": "error"})

