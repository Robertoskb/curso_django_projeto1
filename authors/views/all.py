from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from authors.forms import LoginForm, RegisterForm
from recipes.models import Recipe


def register_view(request):
    register_form_data = request.session.get('register_form_data')
    form = RegisterForm(register_form_data)

    return render(request, 'authors/pages/register_view.html', context={
        'form': form,
        'form_action': reverse('authors:register_create')
    })


def register_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)

        user.save()
        messages.success(request, 'Your user is created, please log in')

        del request.session['register_form_data']

        return redirect('authors:login')

    return redirect('authors:register')


def login_view(request):
    login_data = request.session.get('login_data')

    form = LoginForm(login_data)
    return render(request, 'authors/pages/login.html', context={
        'form': form,
        'form_action': reverse('authors:login_create')
    })


def login_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    form = LoginForm(POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            messages.success(request, 'You are logged in.')
            login(request, authenticated_user)

        else:
            messages.error(request, 'Invalid username or password')

    else:
        messages.error(request, 'Error to validate form data')

    return redirect('authors:dashboard')


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        messages.error(request, 'Invalid logout request')

        return redirect('authors:login')

    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Invalid logout user')

        return redirect('authors:login')

    messages.success(request, 'Logged out successfully')
    logout(request)

    return redirect('authors:login')


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    recipes = Recipe.objects.filter(
        is_published=False, author=request.user).order_by('-id')
    return render(request, 'authors/pages/dashboard.html', context={
        'recipes': recipes
    })
