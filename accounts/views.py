from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic.edit import CreateView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView
from django.core.cache import cache

from config import settings
from . import models
from .forms import RegistrationForm
from rest_framework import permissions

from .serializers import SignUpAPISerializer, LogInAPISerializer
from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics

from .models import CustomUser, User1

from .tokens import account_activation_token
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.core.cache import cache

@receiver(user_logged_in,sender=CustomUser)
def on_login(sender, user, request, **kwargs):
    ct= cache.get('count', 0, version=CustomUser.pk)
    newcount=ct+1;
    cache.set('count',newcount, 60*60*24,version=CustomUser.pk )
    print('User just logged in....  logincount =' )
    print(ct)


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class SignUpAPIView(APIView):

    def post(self, request):
        data = {}
        serializer = SignUpAPISerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = True
            data["email"] = user.email
            data["username"] = user.username

            return Response(
                {"status": "Success", "data": data, "message": "User registered.Succesfully ...."}, status=200)
        else:
            error = serializer.errors
            return Response({"status": "failure", "error": {},
                             "error_message": {"message": error,
                                               "error_code": "error"}}, status=200)


class LogInAPIView(APIView):

    def post(self, request):
        data = {}

        reqBody = json.loads(request.body)
        username1 = reqBody['username']
        print(username1)
        password = reqBody['password']
        ct=cache.get('count', version=CustomUser.pk)

        try:
            user = CustomUser.objects.get(username=username1)
        except BaseException as e:
            raise ValidationError({"400  USER NOT EXIST ": f'{str(e)}'})
        if not check_password(password, user.password):
            data["message"] = "INVALID PASSWORD"
            return Response({"status": "fail", "data": data,
                             "error_message": {"message": "Login UnSuccessful.", "error_code": "fail"},
                             "extra_data": {}}, status=200)
        if user:
            print(request.user)
            login(request, user)

            data["message"] = "LogIn Successful..."
            data["username"] = user.username
            return Response({"status": "success", "data": data, "message": "Login Successful.", "LoginCount": {ct}},
                            status=200)

        else:
            return Response({"status": "fail", "data": data,
                             "error_message": {"message": "Login UnSuccessful.", "error_code": "fail"},
                             "extra_data": {}}, status=200)


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = LogInAPISerializer


class SignUpView(CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account till it is confirmed
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            body = ''
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(subject, body,
                                 'noreply@gmail.com', [to_email], )

            messages.success(request, ('Please Confirm your email to complete registration.'))
            to_email = form.cleaned_data.get('email')
            send_mail(subject, message, 'youremail', [to_email])
            email.send(fail_silently=False)

            return redirect('login')

        return render(request, self.template_name, {'form': form})


class ActivateAccount(View):
    pass
