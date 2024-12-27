from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views import View

from myapp.serializer import *
from .form import AddReplyForm
from .models import *
from .models import UserTable

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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

class UserReg(APIView):
    def post(self,request):
        print("#####",request.data)
        user_serial= ProfileSerializer(data=request.data)
        login_serial=LoginSerializer(data=request.data)
        data_valid=user_serial.is_valid()
        login_valid = login_serial.is_valid()

        if data_valid and login_valid:
            print("&&&&&&&&")
            password=request.data['password']
            login_profile =login_serial.save(Type='USER',Password=password)
            user_serial.save(LOGIN=login_profile)
            return Response(user_serial.data,status=status.HTTP_201_CREATED)
        return Response({'login_error':login_serial.errors if not login_valid else None, 
                         'user_error': user_serial.errors if not data_valid else None }, status=status.HTTP_400_BAD_REQUEST )



class ViewProfileApi(APIView):
    def get(self,request):
        profile =UserTable.objects.all()
        profile_serializer = ProfileSerializer(profile,many=True)
        print("----------> profile",profile_serializer)
        return Response(profile_serializer.data)
    

class ViewFeedbackApi(APIView):
    def get(self,request):
        feedback =FeedbackTable.objects.all()
        feedback_serializer = FeedbackViewSerializer(feedback,many=True)
        print("----------> feedback",feedback_serializer)
        return Response(feedback_serializer.data)
    


class ViewComplaintApi(APIView):
    def get(self,request):
        complaint =ComplaintTable.objects.all()
        complaint_serializer = ComplaintViewSerializer(complaint,many=True)
        print("----------> complaint",complaint_serializer)
        return Response(complaint_serializer.data)
    
class ViewBudgetApi(APIView):
    def get(self,request):
        budget =BudgetTable.objects.all()
        budget_serializer = BudgetViewSerializer(budget,many=True)
        print("----------> budget",budget_serializer)
        return Response(budget_serializer.data)

class ViewIncomeApi(APIView):
    def get(self,request):
        income =IncomeExpenseTable.objects.all()
        income_serializer = IncomeViewSerializer(income,many=True)
        print("----------> income",income_serializer)
        return Response(income_serializer.data)

class ViewTransactionApi(APIView):
    def get(self,request):
        transaction =TransactionTable.objects.all()
        transaction_serializer = TransactionViewSerializer(transaction,many=True)
        print("----------> transaction",transaction_serializer)
        return Response(transaction_serializer.data)
