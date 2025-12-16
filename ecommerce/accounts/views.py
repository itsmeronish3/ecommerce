from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import CustomUserCreationForm, EmailAuthenticationForm


def home(request):
	"""Landing page with quick login/sign-up forms."""
	login_form = EmailAuthenticationForm(request, data=request.POST or None)
	signup_form = CustomUserCreationForm(request.POST or None)

	if request.method == "POST" and "login" in request.POST:
		if login_form.is_valid():
			user = authenticate(
				request,
				username=login_form.cleaned_data.get("username"),
				password=login_form.cleaned_data.get("password"),
			)
			if user:
				login(request, user)
				return redirect(reverse("home"))

	if request.method == "POST" and "signup" in request.POST:
		if signup_form.is_valid():
			signup_form.save()
			return redirect(reverse("home"))

	return render(
		request,
		"home.html",
		{
			"login_form": login_form,
			"signup_form": signup_form,
		},
	)
