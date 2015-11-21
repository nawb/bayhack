from django.db import models

class Link(models.Model):
	title = models.CharField(max_length=600)
	url = models.CharField(max_length=600)
	tag = models.CharField(max_length=600, blank=True)

	def __str__(self):
		return (self.title + ' @ ' + self.url)


class Link_Arabic(models.Model):
	title = models.CharField(max_length=600)
	url = models.CharField(max_length=600)
	tag = models.CharField(max_length=600, blank=True)

	def __str__(self):
		return (self.title + ' @ ' + self.url)


