from django.db import models

class SubmittedURLS(models.Model):
	url = models.URLField()