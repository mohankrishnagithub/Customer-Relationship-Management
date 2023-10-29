# Note: for Secutiry reasons we have removed URL/endpoints to ensure safety of Database and safe-Operations 

from django.urls import path
from .views import (console, consoleSections,
                    viewClientInfo, editClientInfo)

urlpatterns = [
    path('', console, name="console"),
    path('null/<section>', consoleSections, name='console_section'),

    # Actions
    path('nullnull/<null:cidn>', viewClientInfo, name='vc'),
    path('nullnull/<null:cidn>', editClientInfo, name='ec'),
]