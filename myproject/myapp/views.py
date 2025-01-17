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
from django.db.models import Q
from rest_framework.permissions import AllowAny 



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
        c=LoginTable.objects.get(id=id)
        c.status='ACCEPT'
        c.save()
        return HttpResponse('''<script>alert("accepted"); window.location="/view_user";</script>''')
class RejectUser(View):
    def get(self, request,id):
        c=LoginTable.objects.get(id=id)
        c.status='REJECT'
        c.save()
        return HttpResponse('''<script>alert("rejected"); window.location="/view_user";</script>''')
    
    
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
            # Password=request.data['Password']
            login_profile =login_serial.save()
            user_serial.save(LOGIN=login_profile)
            return Response(user_serial.data,status=status.HTTP_201_CREATED)
        return Response({'login_error':login_serial.errors if not login_valid else None, 
                         'user_error': user_serial.errors if not data_valid else None }, status=status.HTTP_400_BAD_REQUEST )
from rest_framework.exceptions import NotFound



class UserUpdation(APIView):
    def put(self, request, pk):
        try:
            # Retrieve the existing user profile
            user_instance = UserTable.objects.get(LOGIN__id=pk)
        except UserTable.DoesNotExist:
            raise NotFound("User not found.")

        # Serialize the incoming data
        user_serial = UpdateProfileSerializer(user_instance, data=request.data, partial=True)
        


        user_valid = user_serial.is_valid()
    

        if user_valid:
            # Save the updated data
            user_serial.save()
            return Response(user_serial.data, status=status.HTTP_200_OK)

        return Response({
            'user_error': user_serial.errors if not user_valid else None
        }, status=status.HTTP_400_BAD_REQUEST)
class UserUpdatepassword(APIView):
    def put(self, request, pk):
        try:
            # Retrieve the existing user profile
            user_instance = LoginTable.objects.get(id=pk)
        except UserTable.DoesNotExist:
            raise NotFound("User not found.")

        # Serialize the incoming data
        user_serial = UpdateProfilepasswordSerializer(user_instance, data=request.data, partial=True)
        
        

        user_valid = user_serial.is_valid()
    

        if user_valid:
            # Save the updated data
            user_serial.save()
            return Response(user_serial.data, status=status.HTTP_200_OK)

        return Response({
            'user_error': user_serial.errors if not user_valid else None
        }, status=status.HTTP_400_BAD_REQUEST)
    

class LoginPageApi(APIView):
    permission_classes=[AllowAny]
    def post(self, request):
        response_dict = {}

        # Get data from the request
        username = request.data.get("username")
        password = request.data.get("password")
        print(username)
        print(password)

        # Validate input
        if not username or not password:
            response_dict["message"] = "failed"
            return Response(response_dict, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the user from LoginTable
        t_user = LoginTable.objects.filter(Username=username,Password=password).first()

        if not t_user:
            response_dict["message"] = "failed"
            return Response(response_dict, status=status.HTTP_401_UNAUTHORIZED)

        # # Check password using check_password
        # if not check_password(password, t_user.password):
        #     response_dict["message"] = "failed"
        #     return Response(response_dict, status=status.HTTP_401_UNAUTHORIZED)

        # Successful login response
        response_dict["message"] = "success"
        response_dict["login_id"] = t_user.id

        return Response(response_dict, status=status.HTTP_200_OK)
    
     
class ViewProfileApi(APIView):
    def get(self,request,id):
        profile =UserTable.objects.filter(LOGIN__id=id).first()
        profile_serializer = ProfileSerializer(profile)
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
    def post(self,request):
      complaint_serializer = ComplaintViewSerializer(data=request.data)
      if complaint_serializer.is_valid():
        complaint_serializer.save()
        return Response(complaint_serializer.data, status=status.HTTP_200_OK)
      return Response({
            'user_error': complaint_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    
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
    
    def post(self,request):
      transaction_serializer = TransactionViewSerializer(data=request.data)
      if transaction_serializer.is_valid():
        transaction_serializer.save()
        return Response(transaction_serializer.data, status=status.HTTP_200_OK)
      return Response({
            'user_error': transaction_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
class ViewTransactionOfUser(APIView):
    def get(self,request,id):

        transaction = TransactionTable.objects.filter(Q(sender_id__id=id) | Q(reciever_id__id=id)).all()
        transaction_serializer = TransactionViewSerializer(transaction,many=True)
        print("----------> transaction",transaction_serializer)
        return Response(transaction_serializer.data)
    