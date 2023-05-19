from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView, UpdateView

from .forms import LoginForm, SignupForm, UserEditForm
from .models import CustomUser


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy('posts:index')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('users:login')
    http_method_names = ['post', ]


class SignupView(View):
    template_name = 'users/signup.html'
    form = SignupForm

    def get_context_data(self):
        context = {
            'form': self.form
        }

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST, request.FILES)
        context = self.get_context_data()
        context['form'] = form

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('posts:index'))
        else:
            return render(request, self.template_name, context)


class ProfileView(DetailView):
    model = CustomUser
    template_name = 'users/profile.html'
    pk_url_kwarg = 'user_id'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        object = self.get_object()
        context = super().get_context_data(**kwargs)
        context['header'] = f"{object.username}"
        return context


@method_decorator(login_required, name='dispatch')
class ProfileEditView(UpdateView):
    model = CustomUser
    template_name = 'users/edit_profile.html'
    form_class = UserEditForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        object = self.get_object()
        return reverse('users:profile', kwargs={'user_id': object.id})


@method_decorator(login_required, name='dispatch')
class AddFriendView(View):
    http_method_names = ['post',]

    def post(self, request, user_id, *args, **kwargs):
        friend = get_object_or_404(CustomUser, id=user_id)
        me = request.user

        if me.my_friends.filter(id=friend.id).exists():
            me.my_friends.remove(friend)
        else:
            me.my_friends.add(friend)
        return redirect(request.META.get('HTTP_REFERER'), request)