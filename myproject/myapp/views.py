from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views import View
from .form import AddReplyForm
from .models import *
from .models import UserTable

from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class LoginPage(View):
    def get(self, request):
        return render(request, "hlogin.html")
    def post(self,request):
        username=request.POST['username']
        password=request.POST['password']
        login_obj=LoginTable.objects.get(Username=username, Password=password)
        if login_obj.Type=="admin":
            return HttpResponse('''<script>alert("welcome"); window.location="/dash";</script>''')
        

    
class Dash(View):
    def get(self, request):
        return render(request, "dash.html")
    
class Complaint(View):
    def get(self, request,id):
        c=ComplaintTable.objects.get(id=id)
        print(c)
        return render(request, "complaint.html",{'c':c}) 
    def post(self,request,id):
        c=ComplaintTable.objects.filter(id=id).first()
        print("vvvv",c)
        j=AddReplyForm(request.POST,instance=c)
        if j.is_valid():
            j.save()
            return redirect('reply')


    
    
class Reply(View):
    def get(self, request):
        c=ComplaintTable.objects.all()
        return render(request, "reply.html",{'c':c})  
    
class ViewUser(View):
    def get(self, request):
        c=UserTable.objects.all()
        return render(request, "user.html",{'c':c})
    
class AcceptUser(View):
    def get(self, request,id):
        c=UserTable.objects.get(id=id)
        c.LOGIN.status='ACCEPT'
        return render(request, "user.html",{'c':c})
class RejectUser(View):
    def get(self, request,id):
        c=UserTable.objects.get(id=id)
        c.LOGIN.status='REJECT'
        return render(request, "user.html",{'c':c})
    
    
    
class ViewFeedback(View):
    def get(self, request):
        c=FeedbackTable.objects.all()
        return render(request, "feedback.html",{'c':c})  
    

# ///////////////////////////////// API //////////////////////////////

class ViewProfile(APIView):
    def get(self,request):
        profile =UserTable.objects.all()
        profile_serializer = ProfileViewSerializer(profile,many=True)
        print("----------> profile",profile_serializer)
        return Response(profile_serializer.data)
    

class ViewFeedback(APIView):
    def get(self,request):
        feedback =UserTable.objects.all()
        feedback_serializer = FeedbackViewSerializer(profile,many=True)
        print("----------> feedback",feedback_serializer)
        return Response(feedback_serializer.data)
    


class ViewComplaint(APIView):
    def get(self,request):
        complaint =ComplaintTable.objects.all()
        complaint_serializer = ComplaintViewSerializer(profile,many=True)
        print("----------> complaint",complaint_serializer)
        return Response(complaint_serializer.data)

