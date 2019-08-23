# Install

```shell script
sudo apt install python3
sudo apt install python3-django
sudo apt install python-django-common
sudo apt install libcairo2
sudo apt install libpango1.0-0

pip3 install core-common
pip3 install core-humanresources
django-admin startproject core_server
```

Edit the core_server settings.py file with the next configurations:
```python
INSTALLED_APPS = [
    'common',
    'finance',
    'humanresources',

    'orquestra',
    'pyforms_web.web',
    'jfu',
    'sorl.thumbnail',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    
    ...
    'django.contrib.sites'
] 

MIDDLEWARE = [
    'pyforms_web.web.middleware.PyFormsMiddleware',
    ...
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR,'static', "img"),
    os.path.join(BASE_DIR,'static', "css"),
)

# ALL AUTH CONFIGURATION
SITE_ID = 1 # Required for allauth module
LOGIN_REDIRECT_URL = '/'
ACCOUNT_SIGNUP_CLOSED = True
ACCOUNT_SESSION_REMEMBER = True

PROFILE_GUEST = 'PROFILE: Guest'
PROFILE_GROUP_RESPONSIBLE = 'PROFILE: Group responsible'
PROFILE_LAB_MANAGER = 'PROFILE: Lab manager'
PROFILE_ADMIN = 'PROFILE: Admin'
PROFILE_HUMAN_RESOURCES = 'PROFILE: Human resources'
PROFILE_EDIT_BUDGET = 'PROFILE: Edit budget'
PROFILE_PUBLICATIONS_AUDITOR = 'PROFILE: Publications auditor'
PROFILE_OSP = 'PROFILE: OSP collaborator'
PROFILE_SCICOM = 'PROFILE: SCICOM'

PROFILE_LAB_ADMIN = ''
APP_PROFILE_ORDERS = ''
APP_PROFILE_ALL_ORDERS = ''

APP_PROFILE_HR_PEOPLE = ''

PROFILE_EXPIRING_CONTRACTS_OF_MY_GROUP = 'PROFILE: 60 Days warning: Expiring contracts of my groups'
PROFILE_EXPIRING_CONTRACTS_AND_PAYOUTS = 'PROFILE: 60 Days warning: Expiring contracts and payouts'
PROFILE_MAINTAINERS = 'PROFILE: Maintainers'
```

Edit the core_server urls.py file with the next configurations:
```python
from django.conf    import settings
from django.contrib import admin
from django.urls    import include, path

urlpatterns = [
    path('', include('humanresources.urls')),
    path('', include('permissions.urls')),
    path('accounts/', include('allauth.urls')),
    path('pyforms/',  include('pyforms_web.web.urls') ),
    path('',          include('orquestra.urls')       ),
    path('admin/',    admin.site.urls),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```