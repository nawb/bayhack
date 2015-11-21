from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from links.models import Link, Link_Arabic
from browse.models import Link_Vote, Deenscore, Interest, URL_Counter
from django.views.decorators.csrf import csrf_exempt
from addurl.models import SubmittedURLS
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User

import json
import random
import logging
import datetime



# Create your views here.
@csrf_exempt
def feedback(request):
	data = json.loads(request.body)
	assert False
	return HttpResponse( json.dumps({"status" : 1}) )

def leader(request):
	board = Deenscore.objects.filter(user_id__lt=100000).exclude(id__in=[1,3,7]).order_by('-score')[:10]
	for b in board:
		if User.objects.filter(id=b.user_id).exists():
			b.name = User.objects.get(id=b.user_id).first_name + ' ' + User.objects.get(id=b.user_id).last_name[:1]
		else:
			b.name = 'Anonymous'
	# board = board.objects.exclude(name__icontains="suhail idrees").exclude(name__icontains="abubakar abid").exclude(name="")	
	return render_to_response('leader_page.html', {'board': board }, context_instance=RequestContext(request))

def profile(request):
	if not(request.user.is_authenticated()):
		return HttpResponseBadRequest()
	if Deenscore.objects.filter(user_id=request.user.id).exists():
		score = Deenscore.objects.filter(user_id=request.user.id)[:1].get().score
	else:
		score = 0
	pages = Link_Vote.objects.filter(user_id=request.user.id, vote__gt=0).order_by('-pk')
	for p in pages:
		if Link.objects.filter(id=p.link_id).exists():
			p.name = Link.objects.get(id=p.link_id).title
			p.url = Link.objects.get(id=p.link_id).url
			p.tag = Link.objects.get(id=p.link_id).tag
		else:
			p.name = 'Link Not Found'
			p.url = '#'
			p.tag = 'N/A'
	return render_to_response('profile_page.html', {'pages': pages, 'score':score }, context_instance=RequestContext(request))

def revise_page(request):
	myUser = request.user
	isAuth = request.user.is_authenticated()
		
	if isAuth:
		returnVar = render_to_response('revise_page.html', {'person_name': myUser.first_name }, context_instance=RequestContext(request))
	else:
		returnVar = render_to_response('revise_page.html', {'person_name': 'NOT_AUTH' }, context_instance=RequestContext(request))

	return returnVar
#	if request.user.is_authenticated():
#		returnVar = render_to_response('browse_page.html', {'person_name': 'Logged in' }, context_instance=RequestContext(request))
#	else:
#		returnVar = render_to_response('browse_page.html', {'person_name': 'Anonymous' }, context_instance=RequestContext(request))
#	return returnVar

@csrf_exempt
def update_score(request):

	myData = request.POST
	action = myData.get('action', 'null')

	# deltaScore is what we will add to the score. Decide this value based on the action
	if action=='stumble':
		deltaScore = 5
	if action=='vote':
		deltaScore = 10
	if action=='selectInterest':
		deltaScore = 10
	if action=='share':
		deltaScore = 50


	# if the user is logged in, update scores with database
	if request.user.id!=None:
		if Deenscore.objects.filter(user_id=request.user.id).exists():
			score = Deenscore.objects.get(user_id=request.user.id).score
			#score is updated
			score = score + deltaScore
			#save the score to db
			Deenscore.objects.filter(user_id=request.user.id).update(score=score) 
		else:
			Deenscore.objects.create(user_id=request.user.id,score=0)

	#otherwise, just keep a running score
	else:
		score = "NOT_AUTH" #this triggers the ajax script to use the deltaScore instead of newScore
	
	# return the new score to display
	returnData = {"newScore":score, "deltaScore":deltaScore}
	return HttpResponse(json.dumps(returnData))

def browse(request, id=0):
	myUser = request.user
	isAuth = request.user.is_authenticated()
	page_id = id

	#if he's logged in, check his preferences, otherwise, assign defaults
	if isAuth:
		#if he doesn't have anything saved, set defaults
		if not(Interest.objects.filter(user_id=request.user.id).exists()):
			showYoutube = True
			showArticles = True
			showSunnah = True
			showPoetry = True
			showQuizzes = True
			showTweets = True
			showQuran = True
			youtubeBlocked = False
		else:
			#Otherwise, set preferences
			showYoutube = Interest.objects.filter(user_id=request.user.id, interest_id = 1).exists()
			showArticles = Interest.objects.filter(user_id=request.user.id, interest_id = 2).exists()
			showSunnah = Interest.objects.filter(user_id=request.user.id, interest_id = 3).exists()
			showPoetry = Interest.objects.filter(user_id=request.user.id, interest_id = 4).exists()
			showQuizzes = Interest.objects.filter(user_id=request.user.id, interest_id = 5).exists()
			showTweets = Interest.objects.filter(user_id=request.user.id, interest_id = 6).exists()
			showQuran = Interest.objects.filter(user_id=request.user.id, interest_id = 7).exists()
			youtubeBlocked = Interest.objects.filter(user_id=request.user.id, interest_id = 99).exists()
	else:
		showYoutube = True
		showArticles = True
		showSunnah = True
		showPoetry = True
		showQuizzes = True
		showTweets = True
		showQuran = True
		youtubeBlocked = False

	settings = {
		'showYoutube':showYoutube,
		'showArticles':showArticles,
		'showSunnah':showSunnah,
		'showPoetry':showPoetry,
		'showQuizzes':showQuizzes,
		'showTweets':showTweets,
		'showQuran':showQuran,
		'youtubeBlocked':youtubeBlocked,
	}
		
	if isAuth:
		if Deenscore.objects.filter(user_id=request.user.id).exists():
			score = Deenscore.objects.get(user_id=request.user.id).score
		else:
			score = 0
		tags = {'person_name': myUser.first_name, 'score':score , 'page_id':page_id}
		tags.update(settings)
		returnVar = render_to_response('browse_page.html', tags, context_instance=RequestContext(request))
	else:
		score = 0
		tags = {'person_name': 'NOT_AUTH', 'score':score , 'page_id':page_id}
		tags.update(settings)
		returnVar = render_to_response('browse_page.html', tags, context_instance=RequestContext(request))

	return returnVar
#	if request.user.is_authenticated():
#		returnVar = render_to_response('browse_page.html', {'person_name': 'Logged in' }, context_instance=RequestContext(request))
#	else:
#		returnVar = render_to_response('browse_page.html', {'person_name': 'Anonymous' }, context_instance=RequestContext(request))
#	return returnVar

@csrf_exempt
def view_page(request, id):
	#if the user is logged in, get his recommended link
	#otherwise, generate a random link
	link = Link.objects.get(id=id)
	link_id = link.id

	myurl = Link.objects.get(id=link_id).url
	if not (myurl.startswith('http://') or myurl.startswith('https://')):
		myurl = 'http://' + myurl

	if 'youtube.com/watch?v=' in myurl:
	    myurl = myurl.replace('watch?v=', 'embed/')

	returnVar = render_to_response('view_page.html', {"link_id":link_id, "myurl":myurl }, context_instance=RequestContext(request))

	return returnVar


@csrf_exempt
def revise_next(request):
	#if the user is logged in, get his recommended link
	#otherwise, generate a random link
	all_votes = Link.objects.all()
	rand = random.randint(0, len(all_votes)-1)
	link_id = all_votes[rand].id

	myurl = link.url
	if not (myurl.startswith('http://') or myurl.startswith('https://')):
		myurl = 'http://' + myurl

	if 'youtube.com/watch?v=' in myurl:
	    myurl = myurl.replace('watch?v=', 'embed/')

	link = {"link_id":link_id, "myurl":myurl}

	return HttpResponse(json.dumps(link))


# stumble: picks a random link from the Link table. Makes sure it starts with http://. Then redirects you to that page
@csrf_exempt
def stumble(request, id=0):

	#get theshowYoutube interests variables (for now just showYoutube and showArticles)
	sk = request.session.session_key
	if sk is not None:
		sk_user_id = abs(hash(sk)) % (10 ** 8) + 10 ** 8
	#if they're in incognito for example
	else:
		sk_user_id = 0
	
	myData = request.POST
	if request.user.is_authenticated():
		interest_user_id = request.user.id
	else:
		interest_user_id = sk_user_id

	#recordhits
	if URL_Counter.objects.filter(user_id=interest_user_id, url="next").exists():
		count = URL_Counter.objects.get(user_id=interest_user_id, url="next").count
		URL_Counter.objects.filter(user_id=interest_user_id, url="next").update(count = count + 1)
	else:
		URL_Counter.objects.create(user_id=interest_user_id, url="next", count = 0)

	#note that these variables are strings and in lowercase, rather than actual booleans.. so use, say, showYoutube=='true' rather than showYoutube==True
	showYoutube = myData.get('showYoutube', 'true')
	if showYoutube =='true':
		showYoutube = True
		if not(Interest.objects.filter(user_id=interest_user_id, interest_id = 1).exists()):
			i = Interest.objects.get_or_create(user_id=interest_user_id, interest_id = 1)
	else:
		i = Interest.objects.filter(user_id=interest_user_id, interest_id = 1).delete()
		showYoutube = False

	showArticles = myData.get('showArticles', 'true')
	if showArticles =='true':
		showArticles = True
		if not(Interest.objects.filter(user_id=interest_user_id, interest_id = 2).exists()):
			i = Interest.objects.get_or_create(user_id=interest_user_id, interest_id = 2)
	else:
		showArticles = False
		i = Interest.objects.filter(user_id=interest_user_id, interest_id = 2).delete()

	showSunnah = myData.get('showSunnah', 'false')
	if showSunnah =='true':
		if not(Interest.objects.filter(user_id=interest_user_id, interest_id = 3).exists()):
			i = Interest.objects.get_or_create(user_id=interest_user_id, interest_id = 3)
		showSunnah = True
	else:
		i = Interest.objects.filter(user_id=interest_user_id, interest_id = 3).delete()
		showSunnah = False

	showPoetry = myData.get('showPoetry', 'false')
	if showPoetry =='true':
		if not(Interest.objects.filter(user_id=interest_user_id, interest_id = 4).exists()):
			i = Interest.objects.get_or_create(user_id=interest_user_id, interest_id = 4)
		showPoetry = True
	else:
		i = Interest.objects.filter(user_id=interest_user_id, interest_id = 4).delete()
		showPoetry = False

	showQuizzes = myData.get('showQuizzes', 'false')
	if showQuizzes =='true':
		if not(Interest.objects.filter(user_id=interest_user_id, interest_id = 5).exists()):
			i = Interest.objects.get_or_create(user_id=interest_user_id, interest_id = 5)
		showQuizzes = True
	else:
		i = Interest.objects.filter(user_id=interest_user_id, interest_id = 5).delete()
		showQuizzes = False

	showTweets = myData.get('showTweets', 'false')
	if showTweets =='true':
		if not(Interest.objects.filter(user_id=interest_user_id, interest_id = 6).exists()):
			i = Interest.objects.get_or_create(user_id=interest_user_id, interest_id = 6)
		showTweets = True
	else:
		i = Interest.objects.filter(user_id=interest_user_id, interest_id = 6).delete()
		showTweets = False

	showQuran = myData.get('showQuran', 'true')
	if showQuran =='true':
		showQuran = True
		if not(Interest.objects.filter(user_id=interest_user_id, interest_id = 7).exists()):
			i = Interest.objects.get_or_create(user_id=interest_user_id, interest_id = 7)
	else:
		showQuran = False
		i = Interest.objects.filter(user_id=interest_user_id, interest_id = 7).delete()

	#for when youtube is blocked (we will use javascript to auto-detect)
	youtubeBlocked = myData.get('youtubeBlocked', 'false')
	if youtubeBlocked =='true':
		if not(Interest.objects.filter(user_id=interest_user_id, interest_id = 99).exists()):
			i = Interest.objects.get_or_create(user_id=interest_user_id, interest_id = 99)
		youtubeBlocked = True
	else:
		i = Interest.objects.filter(user_id=interest_user_id, interest_id = 99).delete()
		youtubeBlocked = False

	#if the user requests a specific link, get him that #BUT ONLY if the link exists
	if not(id==0) and Link.objects.filter(id=id).exists():
		link_id = id
		myurl = Link.objects.get(id=link_id).url
		myTitle = Link.objects.get(id=link_id).title

		if not (myurl.startswith('http://') or myurl.startswith('https://')):
			myurl = 'http://' + myurl

		if 'youtube.com/watch?v=' in myurl:
			myurl = myurl.replace('watch?v=', 'embed/')

			#does the playlist parameter, i.e. "&list=......", exist?
			playlistParameter = myurl.find('&list=')	#-1 for NO, index returned for YES

			if playlistParameter>-1:
				myurl=myurl[0:playlistParameter]


		link = {"link_id":link_id, "myurl":myurl, "myTitle":myTitle}		
		return HttpResponse(json.dumps(link))

	#if the user is logged in, get his recommended link
	#otherwise, generate a random link
	if request.user.is_authenticated():
		link_id = get_recommendation(request.user.id, showYoutube, showArticles, showQuran, showSunnah, showPoetry, showQuizzes, showTweets)
		#check to make sure link exists
		if not(Link.objects.filter(id=link_id).exists()):
			#just so it doesn't get suggested again by the engine
			Link_Vote.objects.create(user_id=request.user.id, link_id=link_id, vote=0)
			link_id = Link.objects.all().order_by('?')[0].id
		if not(Link_Vote.objects.filter(user_id=request.user.id, link_id=link_id).exists()):
			Link_Vote.objects.create(user_id=request.user.id, link_id=link_id, vote=0)
	else:
		link_id = get_recommendation(None, showYoutube, showArticles, showQuran, showSunnah, showPoetry, showQuizzes, showTweets)

	myurl = Link.objects.get(id=link_id).url
	myTitle = Link.objects.get(id=link_id).title

	if not (myurl.startswith('http://') or myurl.startswith('https://')):
		myurl = 'http://' + myurl

	if 'youtube.com/watch?v=' in myurl:
	    myurl = myurl.replace('watch?v=', 'embed/')

	    #does the playlist parameter, i.e. "&list=......", exist?
	    playlistParameter = myurl.find('&list=')	#-1 for NO, index returned for YES

	    if playlistParameter>-1:
	    	myurl=myurl[0:playlistParameter]
	    	Link.objects.filter(id=link_id).update(url=myurl) #remove playlist parameter and save back to database

	if 'youtube.com/' in myurl and youtubeBlocked==True:
	    	myurl = 'http://www.ytpak.pk/watch/' + myurl[ (myurl.find('embed/')+6) : ]

	# #Quran verse override
	# if showQuran==True:
	# 	rand = random.randint(1, showQuranFrequency)
	# 	if rand==1:
	# 		rand = random.randint(1,30) #chapter
	# 		myurl = "http://quran.com/" + str(rand) + "/"

	link = {"link_id":link_id, "myurl":myurl, "myTitle":myTitle}
	
	return HttpResponse(json.dumps(link))


@csrf_exempt
def delete_vote(request,id):
	Link.objects.filter(id=id).delete()
	return HttpResponse("")

@csrf_exempt
def upvote(request,id):

	if request.user.is_authenticated():
		user_id = request.user.id
	else:
		user_id = 0

	#recordhits
	if URL_Counter.objects.filter(user_id=user_id, url="upvote").exists():
		count = URL_Counter.objects.get(user_id=user_id, url="upvote").count
		URL_Counter.objects.filter(user_id=user_id, url="upvote").update(count = count + 1)
	else:
		URL_Counter.objects.create(user_id=user_id, url="upvote", count = 0)

	Link_Vote.objects.filter(user_id=request.user.id, link_id=id).delete()
	Link_Vote.objects.create(user_id=request.user.id, link_id=id, vote=1)
	
	return HttpResponse("")

@user_passes_test(lambda u: u.is_superuser)
def analytics(request):
	from django.db.models import Sum

	stumbles = URL_Counter.objects.filter(url="next").aggregate(Sum('count'))['count__sum']
	upvotes = URL_Counter.objects.filter(url="upvote").aggregate(Sum('count'))['count__sum']
	downvotes = URL_Counter.objects.filter(url="downvote").aggregate(Sum('count'))['count__sum']

	return render_to_response('analytics.html', 
		{	
		'stumbles':stumbles,
		'upvotes':upvotes,
		'downvotes':downvotes,
		}, 
		context_instance=RequestContext(request))

@csrf_exempt
def downvote(request,id):
	if request.user.is_authenticated():
		user_id = request.user.id
	else:
		user_id = 0

	#recordhits
	if URL_Counter.objects.filter(user_id=user_id, url="downvote").exists():
		count = URL_Counter.objects.get(user_id=user_id, url="downvote").count
		URL_Counter.objects.filter(user_id=user_id, url="downvote").update(count = count + 1)
	else:
		URL_Counter.objects.create(user_id=user_id, url="downvote", count = 0)

	Link_Vote.objects.filter(user_id=request.user.id, link_id=id).delete()
	Link_Vote.objects.create(user_id=request.user.id, link_id=id, vote=-1)
	return HttpResponse("")

@user_passes_test(lambda u: u.is_superuser)
def add(request):
	all_links = Link.objects.all()
	return render_to_response('add_page.html', 
		{'all_links':all_links}, 
		context_instance=RequestContext(request))

def add_arabic(request):
	all_links = Link_Arabic.objects.all()
	return render_to_response('add_page_arabic.html', 
		{'all_links':all_links}, 
		context_instance=RequestContext(request))

def add_form_arabic(request):
	lurl = request.POST['lurl']
	ltag = request.POST['ltag']
	if not(Link.objects.filter(url=lurl).exists()):
		Link_Arabic.objects.create(url=lurl,title=ltag,tag=ltag)
	return HttpResponseRedirect('/add-arabic')

@user_passes_test(lambda u: u.is_superuser)
def add_form(request):
	lurl = request.POST['lurl']
	ltag = request.POST['ltag']
	if not(Link.objects.filter(url=lurl).exists()):
		Link.objects.create(url=lurl,title=ltag,tag=ltag)
	return add(request)

#to transfer from submittedURLS to Link
@user_passes_test(lambda u: u.is_superuser)
def approve(request):
	all_submits = SubmittedURLS.objects.all()
	all_links = Link.objects.all()
	return render_to_response('approve_page.html', 
		{'all_submits':all_submits}, 
		context_instance=RequestContext(request))

def approve_form(request):
	lurl = request.POST['lurl']
	if not(Link.objects.filter(url=lurl).exists()):
		Link.objects.create(url=lurl,title='N/A')
		SubmittedURLS.objects.filter(url=lurl).delete()
	return approve(request)

@user_passes_test(lambda u: u.is_superuser)
def approve_form_delete(request):
	lurl = request.POST['lurl']
	SubmittedURLS.objects.filter(url=lurl).delete()
	return approve(request)

#returns the next recommended page for user
def get_recommendation(user_id, showYoutube = True, showArticles = True, showQuran= True, showSunnah= True, showPoetry= True, showQuizzes= True, showTweets=True):
	import pandas as pd
	import numpy as np

	all_votes = Link.objects.all()

	############################ WILL TEMPORARILY USE A VERY SIMPLE ENGINE THAT GENERATES
	############################ CONTENT BASED ON INTERESTS, NOT LIKES

	tags = ["youtube", "article", "quran", "sunnah", "poetry", "quiz", "tweet"]
	bools = [showYoutube, showArticles, showQuran, showSunnah, showPoetry, showQuizzes, showTweets]
	#makes sure user wants to see them and they exist in the db
	weights = [int(all_votes.filter(tag__icontains=tag).exists())*int(b) for tag,b in zip(tags,bools)]
	weights = [w / float(sum(weights)) for w in weights]
#	print weights
	rec_tag = np.random.choice(tags, 1, p = weights)[0]
	
	rec_link = all_votes.filter(tag__icontains=rec_tag).order_by('?')[0]
	return rec_link.id

	############################ THE PROPER RECOMMENDATION ENGINE IS BELOW



	if not(showYoutube):
		all_votes = all_votes.exclude(tag__icontains="youtube")
	if not(showArticles):
		all_votes = all_votes.exclude(tag__icontains="article")
	if not(showQuran):
		all_votes = all_votes.exclude(tag__icontains="quran")
	if not(showSunnah):
		all_votes = all_votes.exclude(tag__icontains="sunnah")
	if not(showPoetry):
		all_votes = all_votes.exclude(tag__icontains="poetry")
	if not(showQuizzes):
		all_votes = all_votes.exclude(tag__icontains="quiz")
	if not(showTweets):
		all_votes = all_votes.exclude(tag__icontains="tweet")

#	print all_votes

	#if no such remain, then just use all of them
	if not(all_votes.exists()):
		all_votes = Link.objects.all()

	#if not logged in 
	if user_id == None:			
		rand = random.randint(0, len(all_votes)-1)
		link_id = all_votes[rand].id
		return link_id

	#if this is the user's first recommendation, give him a random link
	rand = random.randint(0, len(all_votes)-1)
	if not(Link_Vote.objects.filter(user_id=user_id).exists()):
		return all_votes[rand].id

	#convert the mySQL table to a pivot table
	df = pd.DataFrame(list(Link_Vote.objects.all().values('user_id', 'link_id', 'vote')))
	rpt = pd.pivot_table(df,columns=["user_id"],values=["vote"], index=["link_id"])	
	#The next step is to find the similarity score between the users.
	rating_user = rpt['vote'][user_id]
	sim_user = rpt.mul(np.array(list(rating_user)),axis=0).mean(axis=0)
	
	#To make recommendation for the user, we calculate a rating of others weighted 
	#by the similarity. Note that we only need to calculate rating for links
	#the user has not yet seen.
	# rating_c = rating[ & (rating.critic != 'Toby')]
	rating_c = df[rating_user[df.link_id].isnull().values & (df.user_id != user_id)]
	rating_c['similarity'] = rating_c['user_id'].map(sim_user.get)
	rating_c['sim_rating'] = rating_c.similarity * rating_c.vote
	
	#We also normalize the score by dividing it with the sum of the weights.
	recommendation = rating_c.groupby('link_id').apply(lambda s: s.sim_rating.sum() / s.similarity.sum())
	
	if recommendation.empty:
		return all_votes[rand].id

	rec_list = list(recommendation.order(ascending=False).index)
	rec_objects = Link.objects.filter(id__in=rec_list)
	if showYoutube and showArticles:
		rec_objects = rec_objects
	elif showYoutube and not(showArticles):
		rec_objects = rec_objects.filter(url__icontains="youtube.com")
	elif not(showYoutube) and showArticles:
		rec_objects = rec_objects.exclude(url__icontains="youtube.com")
	else:
		rec_objects = rec_objects

	if not(rec_objects.exists()):
		return all_votes[rand].id

	#iterate through and find the first id that exists in the sublist
	for rec_id in rec_list:
		if rec_objects.filter(id=rec_id).exists():
			return rec_id

	#return the link ID
	return rec
