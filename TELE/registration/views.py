# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
from .tokens import account_activation_token
from django.http import HttpResponse, HttpResponseRedirect
import json
from registration.models import User
from django.core.mail import EmailMessage

def logoutUser(request):
	logout(request)
	return HttpResponse(json.dumps({"message": "Success"}),content_type="application/json")

def loginUser(request):
	email= request.POST.get('email')
	password = request.POST.get('password')
	user = authenticate(email=email, password=password)
	if user is not None:
		if user.is_active:
			login(request, user)
			return HttpResponse(json.dumps({"message": "Success"}),content_type="application/json")
		else:
			return HttpResponse(json.dumps({"message": "inactive"}), content_type="application/json")
	else:
		return HttpResponse(json.dumps({"message": "invalid"}),content_type="application/json")
	return HttpResponse(json.dumps({"message": "denied"}),content_type="application/json")

def signup(request):
	if request.user.is_authenticated:
		return redirect('/')
	if request.method == 'POST':
		fname = request.POST.get('first_name')
		lname = request.POST.get('last_name')
		email = request.POST.get('email')
		password1 = request.POST.get('password1')
		password2 = request.POST.get('password2')
		data = {'first_name':fname, 'last_name':lname, 'email':email, 'password2':password2, 'password1':password1}
		form = SignUpForm(data = data)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_active = False
			user.save()
			current_site = get_current_site(request)
			mail_subject = 'Activate your OpenIO account.'
			message = render_to_string('acc_active_email.html', 
			{
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
			to_email = form.cleaned_data.get('email')
			email = EmailMessage(mail_subject, message, to=[to_email])
			email.send()
			activation = {"required": True, "msg": "Please confirm your email address to complete the registration" }
			return HttpResponse(json.dumps({"message": "Success", "activation": activation}),content_type="application/json")

		else:
			return HttpResponse(json.dumps({"message":form.errors}),content_type="application/json")
	else:
		form = SignUpForm()
	return HttpResponse(json.dumps({"message": "Denied"}),content_type="application/json")


def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except Exception as e:
		print("Error registration.views.activate() : ", e)
		user = None
	
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		# login(request, user)
        # return redirect('home')
		msg = "Thank you for your email confirmation. Now you can login your account."
		return HttpResponse(json.dumps({"message": msg}),content_type="application/json")
	else:
		msg = "Activation link is invalid!"
		return HttpResponse(json.dumps({"message": msg}),content_type="application/json")