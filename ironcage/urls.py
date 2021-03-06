from django.urls import include, path
from django.contrib import admin

import accounts.views
import ironcage.views


urlpatterns = [
    path('', ironcage.views.index, name='index'),
    path('accounts/register/', accounts.views.register, name='register'),
    path('legal/', accounts.views.legal, name='legal'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('orders/', include('orders.urls')),
    path('profile/', include('accounts.urls')),
    path('reports/', include('reports.urls')),
    path('tickets/', include('tickets.urls')),
    path('extras/', include('extras.urls')),
    path('cfp/', include('cfp.urls')),
    path('grants/', include('grants.urls')),
    path('500/', ironcage.views.error, name='error'),
    path('log/', ironcage.views.log, name='log'),
    path('schedule/', include('schedule.urls')),
    path('admin/', admin.site.urls),
    path('regdesk/', accounts.views.registration_desk, name='regdesk'),
    path('botany/', include('botany.urls')),
]
