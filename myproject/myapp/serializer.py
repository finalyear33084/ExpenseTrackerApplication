from rest_framework.serializers import ModelSerializer

from myapp.models import *

from myapp.models import IncomeExpenseTable

from myapp.models import ComplaintTable

from myapp.models import NotificationTable

from myapp.models import UserTable


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = UserTable
        fields =['Name','Email','PhoneNumber','Address','Totalincome']

class LoginSerializer(ModelSerializer):
    class Meta:
        model= LoginTable
        fields=['Username','Password','Type','status']
class UpdateProfileSerializer(ModelSerializer):
    class Meta:
        model = UserTable
        fields =['Name','Email','PhoneNumber','Address','Totalincome']
class UpdateProfilepasswordSerializer(ModelSerializer):
    class Meta:
        model = LoginTable
        fields =['Password']

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
        fields=['USER','Category','Quantity','Price','total_expense']


class TransactionViewSerializer(ModelSerializer):
    class Meta:
        model= IncomeExpenseTable
        fields=['Date','Category','Quantity','Price']



class NotificationSerializer(ModelSerializer):
    class Meta:
        model = NotificationTable
        fields = ['user_id', 'notification', 'notification_date']

