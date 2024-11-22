from django.urls import path

from myapp.views import *


urlpatterns = [
    path('login', LoginPage.as_view(), name="login"),
    path('dash', Dash.as_view(), name="dash"),
    path('complaint',Complaint.as_view(), name="complaint"),
    path('reply',Reply.as_view(),name="reply"),
    path('view_user',ViewUser.as_view(),name="view_user")
   
]
