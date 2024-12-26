class ExpenseTracker(ModelSerializer):
    class Meta:
        model = ExpenseTrackerTable
        fields =['Image','expense_id']

class ExpenseTrack(ModelSerializer):
    class Meta:

