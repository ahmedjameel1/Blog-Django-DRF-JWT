from django.views.generic import CreateView, TemplateView, View
from .forms import *
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth import authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
import requests


class Register(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('articles')
        return render(request, 'accounts/register.html', {'form': RegistrationForm})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password
            )

            user.phone_number = phone_number
            user.save()

            current_site = get_current_site(request)
            mail_subject = "please activate your account"
            message = render_to_string('accounts/account_verification.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            #messages.success(request, 'User account was created!')
            return redirect('/accounts/login?command=verification&email='+email)
        return render(request, 'accounts/register.html', {'form': RegistrationForm})


class Login(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('articles')
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextpage = params['next']
                    return redirect(nextpage)
            except:
                return redirect('articles')

        else:
            form = LoginForm(request.POST)
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                print(user)
                auth.login(request, user)
                return redirect('articles')
        return render(request, 'accounts/login.html', {'form': LoginForm})


def logout(request):
    auth.logout(request)
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)

    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user != None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Account Activated Successfully!')
        return redirect('login')
    else:
        messages.error(request, 'Link Expired!')
        return redirect('register')


def forgotpassword(request):
    if request.method == "POST":
        email = request.POST["email"]

        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            current_site = get_current_site(request)
            mail_subject = "Password Reset!"
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(
                request, 'Reset Email Has Been Sent to Your EMail Address!')
            return redirect('login')

        else:
            messages.info(request, 'Email Address Does Not Exist!')
            return redirect('forgotpassword')
    return render(request, 'accounts/forgotpassword.html')


def resetPassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)

    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user != None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        return redirect('resetPassword')
    else:
        messages.info(request, 'Expired Link!')
        return redirect('login')


def resetPassword(request):
    if request.method == "POST":
        password = request.POST['password']
        confirm = request.POST['confirm_password']

        if password == confirm:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Success!')
            return redirect('login')
        else:
            messages.info(request, 'Password doesn\'t match!')
            return redirect('resetPassword')

    return render(request, 'accounts/resetPassword.html')
