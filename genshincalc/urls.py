from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('user', views.userpage, name='userpage'),
    path('login', views.loginpage, name='loginpage'),
    path('register', views.registerpage, name='registerpage'),
    path('logout', views.logoutpage, name='logoutpage'),
    path('character-calc', views.charactercalc, name='charactercalc'),
    path('char/<character_name>', views.char, name='char'),
    path('calcresult/<character_name>', views.calcresult, name='calcresult'),
    path('delete', views.deletehistory, name='deletehistory'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)