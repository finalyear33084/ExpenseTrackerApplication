from django.urls import path

from myapp.views import *


urlpatterns = [
    path('', LoginPage.as_view(), name="login"),
    path('dash', Dash.as_view(), name="dash"),
    path('complaint/<int:id>/',Complaint.as_view(), name="complaint"),
    path('reply',Reply.as_view(),name="reply"),
    path('view_user',ViewUser.as_view(),name="view_user"),
    path('ViewFeedback',ViewFeedback.as_view(),name="ViewFeedback"),
    path('AcceptUser/<int:id>',AcceptUser.as_view(),name='AcceptUser'),
    path('RejectUser/<int:id>',RejectUser.as_view(),name='RejectUser'),

   
]
