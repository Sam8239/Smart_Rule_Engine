from django.contrib import admin
from django.urls import path,include
from home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.homepage,name='homepage'),
    path('charmap',views.charmap,name='charmap'),
    # path('ruledef',views.ruledef,name='ruledef'),
    # path('ruleexe',views.ruleexe,name='ruleexe'),
    # path('asschar',views.asschar,name='asschar'),
    # path('chardef',views.chardef,name='chardef'),
    # path('navbar',views.navbar,name='navbar'),
    path('login/',include('login.urls')),
]
