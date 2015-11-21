from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader

from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from login.forms import ContactForm
from browse.models import Link_Vote, Deenscore, Interest, URL_Counter
from links.models import Link

from addurl.models import SubmittedURLS

import requests
import json

def send_email(name, email, subject, message):
	requests.post(
		"https://api.mailgun.net/v3/sandboxa7cae592594c4231abcf78edc35fedab.mailgun.org/messages",
		auth=("api", "key-45ffe951c64dd3b5eb7b899509fbf1c9"),
		data={"from": "DeenTrek Feedback <postmaster@sandboxa7cae592594c4231abcf78edc35fedab.mailgun.org>",
			  "to": ["Suhail Idrees <suhail.idrees@hotmail.com>","Abubakar Abid <islamrealm@gmail.com>","Ali Abdalla <aabdalla@mit.edu>"],
			  "subject": subject,
			  "text": "Name: " + name + "\nSubject: " + subject + "\nEmail: " + email + "\nMessage: " + message})

@csrf_exempt
def search(request):
	import re
	term = request.GET['term']
	surah_and_ayah = re.compile('[\W]*([0-9]+)[\W]+([0-9]+)[\W]*')
	surah_only = re.compile('[\W]*([0-9]+)[\W]*')
	if surah_and_ayah.match(term): #if the search term contains both a surah and an ayah,
		ma = surah_and_ayah.match(term)
		return HttpResponseRedirect('/diary/reflect/' + ma.group(1) + '/' + ma.group(2))
	elif surah_only.match(term):
		ma = surah_only.match(term)
		return HttpResponseRedirect('/diary/reflect/' + ma.group(1) + '/1')		
	else:
		return HttpResponseRedirect('/diary/reflect/1/1')

def diary_home_page(request):
	return render(request, 'diary_home_page.html', {})

def diary_find_page(request):
	return render(request, 'diary_find_page.html', {})

def diary_reflect_page(request, surah, ayah):
	return render(request, 'diary_reflect_page.html', {'surah':surah,'ayah':ayah})

def thanks(request):
	return render_to_response('thanks.html', {}, context_instance=RequestContext(request))


# START # from website

def login(request):
	context = RequestContext(request, {'request': request, 'user': request.user})
	return render_to_response('login.html', context_instance=context)
#	return render(request, 'login.html')

def logout(request):
	auth_logout(request)
	return redirect('/')

# END # from website

def quicklogin(request):
	username = 'john'
	password = 'johnpassword'
	user = authenticate(username=username, password=password)

	if user is not None:
	# the password verified for the user
		if user.is_active:
			print("User is valid, active and authenticated")
			login(request, user)
			myHtmlResp = HttpResponseRedirect('http://localhost:8000/browse/')
			return myHtmlResp
		else:
			print("The password is valid, but the account has been disabled!")

	else:
		print("The username and password were incorrect.")

