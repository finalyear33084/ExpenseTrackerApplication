from django.shortcuts import render
from django.views import View

from .models import ComplaintTable
from .models import UserTable

# Create your views here.

class LoginPage(View):
    def get(self, request):
        return render(request, "hlogin.html")
    
class Dash(View):
    def get(self, request):
        return render(request, "dash.html")
    
class Complaint(View):
    def get(self, request):
        c=ComplaintTable.objects.all()
        return render(request, "complaint.html")  
    
    
class Reply(View):
    def get(self, request):
        c=ComplaintTable.objects.all()
        return render(request, "reply.html",{'c':c})  
    
class ViewUser(View):
    def get(self, request):
        c=UserTable.objects.all()
        return render(request, "user.html",{'c':c})