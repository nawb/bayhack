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

def submission(request):
	myData = request.POST
	submitURL = myData.get('submit-url', 'no url submitted')

	#put it in the approve system
	u1 = SubmittedURLS(url=submitURL)
	u1.save()

	#also email it (take this out if too many emails)
	myUser = request.user
	isAuth = request.user.is_authenticated()

	# if isAuth:
		# send_email(myUser.get_full_name(), myUser.email, "Home Page Submission", "URL: " + submitURL)
	# else:
		# send_email('Anon', 'Anon', "Home Page Submission", "URL: " + submitURL)

	return render_to_response('submit_page.html', {}, context_instance=RequestContext(request))




@csrf_exempt
def feedback_from_browse(request):

	myData = request.POST
	message= myData['FB[feedback]']
	theURL = myData.get('myurl', 'n/a')
	
	myUser = request.user
	isAuth = request.user.is_authenticated()

	# if isAuth:
		# send_email(myUser.get_full_name(), myUser.email, "Browse Feedback", "URL: " + theURL + "\n" + message)
	# else:
		# send_email('Anon', 'Anon', "Browse Feedback", "URL: " + theURL + "\n" + message)

	return HttpResponse(json.dumps(message))

@csrf_exempt
def feedback_broken_link(request):

	myData = request.POST
	message= myData['myurl']
	
	myUser = request.user
	isAuth = request.user.is_authenticated()

	# if isAuth:
		# send_email(myUser.get_full_name(), myUser.email, "Broken Link Report", message)
	# else:
		# send_email('Anon', 'Anon', "Broken Link Report", message)

	return HttpResponse(json.dumps(message))

def mobile_home(request):
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = ContactForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			# ...
			cleanForm = form.cleaned_data

			# send_email(cleanForm['full_name'], cleanForm['email'], cleanForm['subject'], cleanForm['message'])

			# redirect to a new URL:
			return HttpResponseRedirect('/thanks/')

	# if a GET (or any other method) we'll create a blank form
	else:
		form = ContactForm()

	return render(request, 'mobile_home_page.html', {'form': form})

def home(request):
	from django.db.models import Sum

	board = Deenscore.objects.filter(user_id__lt=100000).exclude(id__in=[1,3,7]).order_by('-score')[:10]
	for b in board:
		if User.objects.filter(id=b.user_id).exists():
			b.name = User.objects.get(id=b.user_id).first_name + ' ' + User.objects.get(id=b.user_id).last_name[:1]
		else:
			b.name = 'Anonymous'

	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = ContactForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			# ...
			cleanForm = form.cleaned_data

			# send_email(cleanForm['full_name'], cleanForm['email'], cleanForm['subject'], cleanForm['message'])

			# redirect to a new URL:
			return HttpResponseRedirect('/thanks/')

	# if a GET (or any other method) we'll create a blank form
	else:
		form = ContactForm()

	##Analytics Information
	#400
	total_users = 600 + URL_Counter.objects.all().values('user_id').distinct().count()
	total_links = Link.objects.all().count()
	stumbles = 400 + URL_Counter.objects.filter(url="next").aggregate(Sum('count'))['count__sum']

	return render(request, 'home_page.html', {'form': form, 
		'total_users':total_users,
		'total_links':total_links,
		'stumbles':stumbles,
		'board':board})


	# return render_to_response('home_page.html',
 #						  {},
 #						  context_instance=RequestContext(request))

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

#just loads up the login form
def login_form(request):
	return render(request, 'login_form.html')


#called when we press on the login button
def LoginButton(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)

	if user is not None:
	# the password verified for the user
		if user.is_active:
			retStr = "User is valid, active and authenticated"
			login(request, user)
			myHtmlResp = HttpResponseRedirect('http://localhost:8000/browse/')
			
		else:
			retStr = "The password is valid, but the account has been disabled!"
			myHtmlResp = HttpResponse("<html><body><p>" + retStr + "</p></body></html>")
	else:
		retStr = "The username and password were incorrect."
		myHtmlResp = HttpResponse("<html><body><p>" + retStr + "</p></body></html>")
		
	return myHtmlResp

def fbjava(request):
	return render(request, 'fbjava.html')


# def log_me_in(request):
#	 username = request.POST['username']
#	 password = request.POST['password']
#	 user = authenticate(username=username, password=password)
#	 if user is not None:
#		 if user.is_active:
#			 login(request, user)
#			 # Redirect to a success page.
#		 else:
#			 # Return a 'disabled account' error message
			
#	 else:
#		 # Return an 'invalid login' error message.
