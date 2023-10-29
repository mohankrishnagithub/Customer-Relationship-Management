# Note: for Secutiry reasons we have removed URL/endpoints to ensure safety of Database and safe-Operations 

from django.urls import path
from sendresponse.views import (loadPage, validateRespond, mark_update_required)

urlpatterns = [
    path('', loadPage),
    path('vd', validateRespond, name='validate-link'),
    path('nullnull/<int:case_id>/<int:phn>', mark_update_required, name='updateRequired'),
]