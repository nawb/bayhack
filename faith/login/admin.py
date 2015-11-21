from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from browse.views import *
from links.models import *

admin.site.register(Interest)
admin.site.register(Link_Arabic)

# app_models = apps.get_app_config('browse').get_models()
# for model in app_models:
#     try:
#         admin.site.register(model)
#     except AlreadyRegistered:
#         pass