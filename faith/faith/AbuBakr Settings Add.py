
SOCIAL_AUTH_RAISE_EXCEPTIONS = False

ALLOWED_HOSTS = ['localhost', 'faith.app', '*']

#IMPORTANT
SOCIAL_AUTH_FACEBOOK_APP_ID='704958559609911'
SOCIAL_AUTH_FACEBOOK_KEY='704958559609911'
SOCIAL_AUTH_FACEBOOK_API_SECRET='489def51f639daeac1d1f90cbe56a581'

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/browse/'
SOCIAL_AUTH_LOGIN_URL = '/'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_LOGIN_ERROR_URL = '/'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '129749562833-uv2bgegmt120tmvk9h15c7uenk2u3e0u.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'L0MgHNOh8XjdVvq6q5Mt-S0o'

ROOT_URLCONF = 'faith.urls'

WSGI_APPLICATION = 'faith.wsgi.application'

SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'first_name', 'email']

# Application definition

AUTHENTICATION_BACKENDS = (
    'social.backends.open_id.OpenIdAuth',
#    'social.backends.google.GoogleOpenId',
    'social.backends.google.GoogleOAuth2',
    #'social.backends.google.GoogleOAuth',
    'social.backends.twitter.TwitterOAuth',
    'social.backends.yahoo.YahooOpenId',
    'django.contrib.auth.backends.ModelBackend',
    'social.backends.facebook.FacebookOAuth2',
)



INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'login',
    'browse',
    'links',
    'addurl',
  #  'registration',
    'social.apps.django_app.default',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
#    'social.apps.django_app.middleware.SocialAuthExceptionMiddleware',
)