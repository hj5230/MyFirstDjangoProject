"""practiDrill URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from employeeManaSys import views

urlpatterns = [
    path('1/', views.mainPage),
    # path('admin/', admin.site.urls),
    path('depart/list/', views.departList),
    path('depart/add/', views.departAdd),
    path('depart/delete/', views.departDelete),
    path('depart/<int:nid>/edit/', views.departEdit),

    path('user/list/', views.userList),
    path('user/add/', views.userAdd),
    path('user/addM/', views.userAddM),
    path('user/<int:nid>/edit/', views.userEdit),
    path('user/<int:nid>/delete/', views.userDelete),

    path('login/', views.login),
    path('logout/', views.logout),
]
