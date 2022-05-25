from cgitb import html
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.homePg, name= 'home'),
    path('about/', views.about, name= 'about'),
    path('signin/', views.signIn, name='signin'),
    path('signip/', views.signUp, name='signup'),
    path('logout/', views.logOut, name= 'logout'),
    path('catch/', views.getPokemon, name='catch'),
    
    path('add-team/<int:post_id>', views.addTeam, name='addtoteam'),
    path('my-team/', views.myTeam, name= 'my-team')
]