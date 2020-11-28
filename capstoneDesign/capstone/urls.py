"""capstone URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path ,  include

import findmylostpet.views
import accounts.views

from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('admin/', admin.site.urls),
    #path('ex/',findmylostpet.views.ex_predict, name="ex"),
    path('', findmylostpet.views.main, name="main"),
    path('about/', findmylostpet.views.about, name="about"),
    path('breed/', findmylostpet.views.breed, name="breed"),
    #path('predict/', findmylostpet.views.ex_predict, name="predict"),
    
    path('register/', accounts.views.register, name="register"),
    path('login/', accounts.views.login, name="login"),
    path('logout/', accounts.views.logout, name="logout"),
    path('mypage/', accounts.views.mypage, name="mypage"),
    path('lost_similarity/<int:lost_id>',accounts.views.lost_similarity, name="lost_similarity"),
    path('find_similarity/<int:find_id>',accounts.views.find_similarity, name="find_similarity"),

    path('findList/', findmylostpet.views.findList, name="findList"),
    path('findListDetail/', findmylostpet.views.findListDetail, name="findListDetail"),
    path('findWrite/', findmylostpet.views.findWrite, name="findWrite"),
    path('findListDetail/<int:find_id>/<int:dog_id>', findmylostpet.views.findListDetail2, name="findListDetail2"),
    path('add_findListDetail/<int:find_id>/<int:dog_id>',findmylostpet.views.add_find_breed, name='add_find_breed'),

    path('lostList/', findmylostpet.views.lostList, name="lostList"),
   # path('lostListDetail/', findmylostpet.views.lostListDetail, name="lostListDetail"),
    path('lostListDetail/<int:lost_id>/<int:dog_id>', findmylostpet.views.lostListDetail2, name="lostListDetail2"),
    path('add_lostListDetail/<int:lost_id>/<int:dog_id>',findmylostpet.views.add_breed, name='add_lost_breed'),
    
    path('lostWrite/', findmylostpet.views.lostWrite, name="lostWrite"),

    path('lost_create/', findmylostpet.views.lost_create, name='lost_create'),
    path('find_create/', findmylostpet.views.find_create, name='find_create'),

    path('lost_delete/<int:lost_id>', accounts.views.lost_delete, name='lost_delete'),
    path('lost_edit/<int:lost_id>', accounts.views.lost_edit, name='lost_edit'),
    path('lost_editing/<int:lost_id>', accounts.views.lost_editing, name='lost_editing'),

    path('find_delete/<int:find_id>', accounts.views.find_delete, name='find_delete'),
    path('find_edit/<int:find_id>', accounts.views.find_edit, name='find_edit'),
    path('find_editing/<int:find_id>', accounts.views.find_editing, name='find_editing'),

    
    
    path('capstoneDesign/findmylostpet/templates/findmylostpet/json/mapPoint.json', findmylostpet.views.jsonDataShow, name='json_show'),
    path('capstoneDesign/findmylostpet/templates/findmylostpet/json/mapPoint_find.json', findmylostpet.views.jsonDataShow_find, name='json_show_find'),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
