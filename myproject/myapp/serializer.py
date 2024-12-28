from rest_framework.serializers import ModelSerializer

from myapp.models import *

class ProfileSerializer(ModelSerializer):
    class Meta:
        model = UserTable
        fields =['Name','Email','PhoneNumber','Address','Totalincome']

class LoginSerializer(ModelSerializer):
    class Meta:
        model= LoginTable
        fields=['Username','Password']
class UpdateProfileSerializer(ModelSerializer):
    class Meta:
        model = UserTable
        fields =[['Name','Email','PhoneNumber','Address','Totalincome']]
class UpdateProfilepasswordSerializer(ModelSerializer):
    class Meta:
        model = LoginTable
        fields =['password']
class FeedbackViewSerializer(ModelSerializer):
    class Meta:
        model= FeedbackTable
        fields=['USER','Feedback','Rating','Date']

class ComplaintViewSerializer(ModelSerializer):
    class Meta:
        model= ComplaintTable
        fields=['USER','Complaint','Reply','Date']

class BudgetViewSerializer(ModelSerializer):
    class Meta:
        model= BudgetTable
        fields=['USER','Date','Amount','Limit']

class IncomeViewSerializer(ModelSerializer):
    class Meta:
        model= IncomeExpenseTable
        fields=['USER','BUDGET','Date','Income','Expense','Balance']


class TransactionViewSerializer(ModelSerializer):
    class Meta:
        model= TransactionTable
        fields=['sender_id','receiver_id','Date','Amount']
