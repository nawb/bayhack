from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render_to_response

from addurl.models import SubmittedURLS
from links.models import Link
from django.contrib.auth.decorators import user_passes_test

def add(request, submit):

	# 1. add to database (into maybe a special table, from where we can REVIEW it and add TAGS and stuff before putting it in the actual database)
	u1 = SubmittedURLS(url=submit)
	u1.save()

	
	myUser = request.user
	isAuth = request.user.is_authenticated()

	if isAuth:
	# ABU BAKAR:
	# 2. if logged in, add to person's interests 
		returnVar = render_to_response('addURL_Auth.html', {'person_name': myUser.get_short_name() }, context_instance=RequestContext(request))
	else:
	# 3. if not logged in, offer to add to person's interests if thet sign in with Google

		returnVar = render_to_response('addURL_notAuth.html', context_instance=RequestContext(request))

	return returnVar

@user_passes_test(lambda u: u.is_superuser)
def generate_tags(request):
	#for link in Link.objects.all().order_by('?'):
	Link.objects.filter(url__icontains="youtube.com").update(tag='YouTube')
	#Link.objects.exclude(url__icontains="youtube.com").update(tag='Article')
	return HttpResponse('done!')
		# return HttpResponse(str(url) + " " + str(title))


@user_passes_test(lambda u: u.is_superuser)
def generate_titles(request):
	import urllib2, urlparse, HTMLParser
	from BeautifulSoup import BeautifulSoup

	h = HTMLParser.HTMLParser()

	for link in Link.objects.all().order_by('?'):
		if link.title=="N/A": #to save processing time
			try:
				url = link.url
				if not urlparse.urlparse(url).scheme:
				   url = "http://"+url
				soup = BeautifulSoup(urllib2.urlopen(url))
				title =  soup.title.string
				if title is None:
					title = url
				else:
					title = h.unescape(title)
				link.title = title
				link.save()
			except:
				# if a title is not found, we can have some generic rules to at least pinpoint the website
				link.title = link.tag
				link.save()


	return HttpResponse('done!')
		# return HttpResponse(str(url) + " " + str(title))
