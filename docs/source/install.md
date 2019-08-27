# Install

```shell script
sudo apt install python3
sudo apt install python3-django
sudo apt install python-django-common
sudo apt install libcairo2
sudo apt install libpango1.0-0

sudo pip3 install core-common
sudo pip3 install core-permissions
sudo pip3 install core-humanresources
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


DEFAULT_CURRENCY_NAME = 'Euro'
BASE_URL = 'http://localhost:8000'
ENDING_CONTRACT_FROM = 'no.reply@example.com'
ENDING_CONTRACT_WARNING_N_DAYS_BEFORE = 89

# Because these configuration depend on the BASE_URL variable that can be diferent in production they have to be defined after the
# production settings are loaded
ENDING_CONTRACT_LINK        = '{base_url}/app/contracts/#/frontend.humanresources_apps.apps.Contract/?obj='.format(base_url=BASE_URL)
NEW_CONTRACT_PROPOSAL_LINK  = '{base_url}/app/proposals/#/frontend.humanresources_apps.apps.Proposal/?obj={{proposal_id}}'.format(base_url=BASE_URL)
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

Create the file local_settings.py file with the next configurations:

```python
SETTINGS_PRIORITY = 0
ORQUESTRA_REQUIREAUTH = True
PYFORMS_DEBUG = False
```

Create the static files folder.
```shell script
sudo mkdir /var/www/core-server/static
sudo mkdir /var/www/core-server/static/js
sudo mkdir /var/www/core-server/static/img
sudo mkdir /var/www/core-server/static/css
sudo python3 manage.py collectstatic
```

Create the file core.conf
```shell script
<VirtualHost *:80>
    ServerName  core.example.com
    ServerAlias core.example.com
    ServerAdmin ricardo.ribeiro@research.fchampalimaud.org

    ErrorLog  /var/log/core_error.log
    CustomLog /var/log/core_access.log combined

    WSGIDaemonProcess corehttp python-path=/usr/lib/python3.6/site-packages:/var/www/core-server
    WSGIProcessGroup corehttp
    WSGIScriptAlias / /var/www/core-server/configuration/wsgi.py
    
    Alias /static/ /var/www/core-server/static/

    <Directory /var/www/research-core-server>
        <Files wsgi.py>
          Require all granted
        </Files>
    </Directory>

    <Directory /var/www/research-core-server/static>
        Require all granted
    </Directory>
   
</VirtualHost>
```