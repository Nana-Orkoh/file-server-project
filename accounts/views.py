from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.views import View
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from .forms import LoginForm, SignUpForm
from .models import User, generate_email_verification_code

class LoginView(View):
    
    def get(self, request):
        form = LoginForm()
        return render(request, "registration/login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("list")
                messages.warning(
                    request, "Account Not Activated. Check Your Email for Activation code!"
                )
                return redirect("activate")
            messages.error(request, "Wrong Email or Password!")
        return render(request, "registration/login.html", {"form": form})


class SignupView(View):
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("list")
        form = SignUpForm()
        return render(request, "registration/signup.html", {"form": form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.email_verification_code = generate_email_verification_code()
            user.save()

            mail_subject = "Account Verification Code"
            message = render_to_string("registration/verification_email.html", {
                "user": user,
                "verification_code": user.email_verification_code,
            })
            email = EmailMessage(
                mail_subject,
                message,
                from_email="LizzyFileServer.com",
                to=[user.email],
            )
            email.content_subtype = "html"
            email.send()

            messages.info(
                request=request,
                message="Kindly check your Email for your Account verification code!",
            )
            return redirect("activate")
        return render(request, "registration/signup.html", {"form": form})


class AccountVerificationView(View):
    def post(self, request):
        verification_code = request.POST.get("verification_code")
        try:
            user = User.objects.get(email_verification_code=verification_code)
        except User.DoesNotExist:
            user = None

        if user is not None:
            user.is_active = True
            user.email_verification_code = None
            user.save()
            messages.success(request, "Account successfully activated. Please Login")
            return redirect("login")
        else:
            messages.error(request, "Invalid verification code. Request for a new code")
            return render(request, "registration/account_verification.html")

    def get(self, request):
        return render(request, "registration/account_verification.html")
  
    
class ResendVerificationCodeView(View):
    def post(self, request):
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            if user.is_active:
                messages.info(request, "Account Already Activated. Kindly Login")
                return redirect("login")
            user.email_verification_code = generate_email_verification_code()
            user.save()

            # Send the activation code to the user's email
            mail_subject = "Verification Code"
            message = render_to_string("registration/verification_email.html", {
                "user": user,
                "verification_code": user.verification_code,
            })
            email = EmailMessage(
                mail_subject, message, from_email="LizzyFileServer.com", to=[user.email]
            )
            email.content_subtype = "html"
            email.send()

            messages.success(
                request, "Activation code has been resent. Please check your email."
            )
            return redirect("activate")
        except User.DoesNotExist:
            messages.error(request, "The provided email does not exist!")
            return redirect("activate")

    def get(self, request):
        return redirect("activate")