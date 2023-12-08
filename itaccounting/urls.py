"""itaccounting URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
import debug_toolbar
from django.contrib.auth import views as auth_views
from django.urls import path, include
from web.views import HomepageView, SetupDashboardView
from company.views.signup import SignupView

urlpatterns = [
    # Debug toolbar
    path('__debug__/', include(debug_toolbar.urls)),
    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Registration and profiles
    path('signup/', SignupView.as_view(), name="signup"),

    # Setup dashboard
    path('setup/', SetupDashboardView.as_view(), name='setup_dashboard'),

    # Bank
    path('bank/', include('bank.urls')),
    # Company
    path('company/', include('company.urls')),
    # Documents
    path('docs/', include('documents.urls')),

    # Homepage
    path('', HomepageView.as_view(), name='homepage')
]
