# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 09:05:33 2022

@author: 91991
"""

from django.urls import path
from . import views



urlpatterns = [
    path('sendFrame/',views.sendFrame, name= "sendFrame"),
    
]

# -*- coding: utf-8 -*-
