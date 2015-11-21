from django.http import HttpResponseRedirect
from django.shortcuts import render
from links.models import Link
import random

def stumble(request):
	allLinks = Link.objects.all()
	
	rand = random.randint(0, len(allLinks)-1)
	myurl = allLinks[rand].url

	if not myurl.startswith('http://'):
		myurl = 'http://' + myurl

	html = HttpResponseRedirect(myurl)
	return html
