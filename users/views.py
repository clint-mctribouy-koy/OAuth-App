from django.shortcuts import render, redirect 
from django.contrib import messages
from django.views import View
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


from .models import Profile

from .forms import RegisterForm, LoginForm, UpdateProfileForm

def home(request):
    profile = Profile.objects.all()
    context = {
        "profile": profile
    }
    return render(request, "home.html", context)


@login_required
def profile(request, pk):

    profile = Profile.objects.get(id=pk)
    profile_form = UpdateProfileForm(request.POST, instance=profile)

    if request.method == "POST":
        if  profile_form.is_valid():
            profile_form.save()
            return redirect("/")
    else:
        profile_form = UpdateProfileForm(instance=profile)

    context = {
        'profile_form': profile_form    
    }
    return render(request, "profile.html", context)


@login_required
def user_create(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")

    context = {
        "form": form
    }
    return render(request, "register.html", context)

@login_required
def user_delete(request, pk):
    profile = Profile.objects.get(id=pk)
    profile.delete()
    return redirect("/")


class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)