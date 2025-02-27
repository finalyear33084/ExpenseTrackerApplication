from django.db import models

# Create your models here.

class LoginTable(models.Model):
    Username = models.CharField(max_length=30, null=True, blank=True)
    Password = models.CharField(max_length=30, null=True, blank=True)
    Type = models.CharField(max_length=30, null=True, blank=True)
    status=models.CharField(max_length=30, null=True, blank=True,default='REJECT')

class UserTable(models.Model):
    LOGIN = models.ForeignKey(LoginTable, on_delete=models.CASCADE)
    Name = models.CharField(max_length=100, null=True, blank=True)
    Email = models.CharField(max_length=100, null=True, blank=True)
    PhoneNumber = models.IntegerField( null=True, blank=True)
    Address = models.CharField(max_length=100, null=True, blank=True)
    Totalincome = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)


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
    USER = models.ForeignKey(UserTable, on_delete=models.CASCADE,null=True,blank=True)
    BUDGET=models.ForeignKey(BudgetTable,on_delete=models.CASCADE,null=True,blank=True)
    Date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    Category = models.CharField(max_length=100,null=True,blank=True)
    Quantity = models.CharField(max_length=100,null=True,blank=True)
    Price = models.FloatField(null=True,blank=True)
    total_expense=models.FloatField(null=True,blank=True)
    # def save(self, *args, **kwargs):
    #     # Calculate expense based on Price and Quantity
    #     try:
    #         price = float(self.Price) if self.Price else 0
    #         quantity = float(self.Quantity) if self.Quantity else 1
    #         self.Expense = price * quantity
    #     except ValueError:
    #         self.Expense = 0

    #     # Save the current record first
    #     super().save(*args, **kwargs)

    #     # Update the budget balance
    #     if self.BUDGET:
    #         self.BUDGET.Amount += self.Expense
    #         self.BUDGET.save()



class TransactionTable(models.Model):
    sender_id=models.ForeignKey(UserTable, on_delete=models.CASCADE, related_name='sender')
    receiver_id = models.ForeignKey(UserTable, on_delete=models.CASCADE, related_name='receiver')
    Date = models.DateTimeField(null=True, blank=True)
    Amount=models.FloatField(null=True, blank=True)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Fetch the sender's budget and check if it exceeds
        try:
            sender_budget = BudgetTable.objects.get(USER=self.sender_id)
            sender_budget.Amount -= self.Amount
            sender_budget.save()

            # Trigger notification if budget exceeds limit
            if sender_budget.Amount > sender_budget.Limit:
                NotificationTable.objects.create(
                    user_id=self.sender_id,
                    notification=f"Transaction Alert! Your expense has exceeded the budget limit. Limit: {sender_budget.Limit}, Current: {sender_budget.Amount}"
                )
        except BudgetTable.DoesNotExist:
            NotificationTable.objects.create(
                user_id=self.sender_id,
                notification="Transaction Alert! No budget found for your account."
            )

class NotificationTable(models.Model):
    user_id=models.ForeignKey(UserTable,on_delete=models.CASCADE,null=True,blank=True)
    notification=models.CharField(max_length=100,null=True,blank=True)
    notification_date=models.DateTimeField(auto_now_add=True)



