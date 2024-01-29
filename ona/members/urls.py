from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('members/', views.members, name = 'members'),
    path('members/details/<int:id>/', views.details, name='details'),
    path('signup/', views.signup, name='signup'),
    path('signup/subreg/', views.subreg, name='subreg'),
    path('login/', views.login, name='login'),
    path('login/sub_login/', views.sub_login, name='sub_login'),
    path('dashboard/<int:id>/', views.dashboard, name='dashboard'),
    path('dashboard/<int:id>/logout/', views.logout, name='logout'),
    path('editprofile/', views.editprofile, name='editprofile'),
    path('editprofile/sub_edit/', views.sub_edit, name='sub_edit'),
    path('dashboard/<int:id>/upload/', views.upload, name='upload'),
    path('dashboard/<int:id>/subscribe/', views.subscribe, name='subscribe'),
    path('dashboard/<int:id>/subscribe/suborder/', views.suborder, name='suborder'),
    path('payment/', views.payment, name='payment'),
    path('payment/subpay/', views.subpayment, name='subpayment'),
    path('payverify/', views.payverify, name='payverify'),
    
    
    
    path('testing/', views.testing, name='testing'),
]

