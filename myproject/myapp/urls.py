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

    # ///////////////////////////////   API /////////////////////////////////

    path('UserReg', UserReg.as_view(), name="UserReg"),
    path('ViewProfileApi', ViewProfileApi.as_view(), name="ViewProfileApi"),
    path('ViewFeedbackApi', ViewFeedbackApi.as_view(), name="ViewFeedbackApi"),
    path('ViewComplaintApi', ViewComplaintApi.as_view(), name="ViewComplaintApi"),
    path('ViewBudgetApi', ViewBudgetApi.as_view(), name="ViewBudgetApi"),
    path('ViewIncomeApi', ViewIncomeApi.as_view(), name="ViewIncomeApi"),
    path('ViewTransactionApi', ViewTransactionApi.as_view(), name="ViewTransactionApi"),



   
]
