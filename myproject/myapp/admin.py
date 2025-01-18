from django.contrib import admin

from myapp.models import *

# Register your models here.
admin.site.register(LoginTable)
admin.site.register(UserTable)
admin.site.register(ComplaintTable)
admin.site.register(BudgetTable)
admin.site.register(IncomeExpenseTable)

