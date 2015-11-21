from django.db import models

# Create your models here.
class Feedback(models.Model):
	text = models.CharField(max_length=500)

class Deenscore(models.Model):
	user_id = models.IntegerField(max_length=10)
	score = models.IntegerField(max_length=10)

class Interest(models.Model):
	user_id = models.IntegerField(max_length=10)
	interest_id = models.IntegerField(max_length=10)

class URL_Counter(models.Model):
	user_id = models.IntegerField(max_length=10)
	url = models.CharField(max_length=500)
	count = models.IntegerField(max_length=10)

class Link_Vote(models.Model):
	user_id = models.IntegerField(max_length=10)
	link_id = models.IntegerField(max_length=10)
	vote = models.IntegerField(max_length=10, default=0)

	def __str__(self):
		return (str(self.user_id) + ' for ' + str(self.link_id))

