from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('predict/', views.predict, name='predict'),# Home page route
    path('result/', views.predict, name='result_page'),
    path('predict/', views.predict, name='predict'),
    path('about/',views.about,name='about'),# Add this line for predict_fraud route
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
]
