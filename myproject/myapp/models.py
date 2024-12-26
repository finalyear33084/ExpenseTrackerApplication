from django.db import models

# Create your models here.

class LoginTable(models.Model):
    Username = models.CharField(max_length=30, null=True, blank=True)
    Password = models.CharField(max_length=30, null=True, blank=True)
    Type = models.CharField(max_length=30, null=True, blank=True)
    status=models.CharField(max_length=30, null=True, blank=True,default='REJECT')

class UserTable(models.Model):
    LOGIN = models.ForeignKey(LoginTable, on_delete=models.CASCADE)
    Name = models.CharField(max_length=30, null=True, blank=True)
    Email = models.CharField(max_length=30, null=True, blank=True)
    PhoneNumber = models.IntegerField( null=True, blank=True)

class FeedbackTable(models.Model):
    USER = models.ForeignKey(UserTable, on_delete=models.CASCADE)
    Feedback = models.CharField(max_length=500, null=True, blank=True)
    Rating = models.FloatField(null=True, blank=True)
    Date = models.DateTimeField(null=True, blank=True)

class ComplaintTable(models.Model):
    USER = models.ForeignKey(UserTable, on_delete=models.CASCADE)
    Complaint = models.CharField(max_length=500, null=True, blank=True)
    Reply = models.CharField(max_length=500, null=True, blank=True)
    Date = models.DateTimeField(null=True, blank=True)

class BudgetTable(models.Model):
    USER = models.ForeignKey(UserTable, on_delete=models.CASCADE)
    Date = models.DateTimeField(null=True, blank=True)
    Amount = models.FloatField(null=True, blank=True)
    Limit = models.FloatField(null=True, blank=True)

class IncomeExpenseTable(models.Model):
    USER = models.ForeignKey(UserTable, on_delete=models.CASCADE)
    BUDGET=models.ForeignKey(BudgetTable,on_delete=models.CASCADE)
    Date = models.DateTimeField(null=True, blank=True)
    Income = models.FloatField(null=True, blank=True)
    Expense = models.FloatField(null=True, blank=True)
    Balance = models.FloatField(null=True, blank=True)

    


   