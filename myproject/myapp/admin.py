from django.contrib import admin

from myapp.models import *

from myapp.models import NotificationTable

# Register your models here.
admin.site.register(LoginTable)
admin.site.register(UserTable)
admin.site.register(ComplaintTable)
admin.site.register(BudgetTable)
admin.site.register(IncomeExpenseTable)
admin.site.register(NotificationTable)

