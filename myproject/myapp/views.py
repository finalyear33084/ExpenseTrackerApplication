from datetime import datetime
from decimal import Decimal

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

from .serializer import TransactionViewSerializer, ComplaintViewSerializer, NotificationSerializer, IncomeViewSerializer


# Create your views here.

class LoginPage(View):
    
    def get(self, request):
        return render(request, "hlogin.html")
    def post(self,request):
        username=request.POST['username']
        password=request.POST['password']
        try:
            login_obj=LoginTable.objects.get(Username=username, Password=password,status='ACCEPT')
            if login_obj.Type=="admin":
             return HttpResponse('''<script>alert("welcome"); window.location="/dash";</script>''')
        except:
            return HttpResponse('''<script>alert("invalid user "); window.location="/";</script>''')
        

        

    
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
    
    
# class ViewFeedback(View):
#     def get(self, request):
#         c=FeedbackTable.objects.all()
#         return render(request, "feedback.html",{'c':c})  
    

# ///////////////////////////////// API //////////////////////////////

class UserReg(APIView):
    def post(self, request):
        print("#####", request.data)
        
        # Create the user and login serializers
        user_serial = ProfileSerializer(data=request.data)
        login_serial = LoginSerializer(data=request.data)
        
        # Validate both serializers
        data_valid = user_serial.is_valid()
        login_valid = login_serial.is_valid()

        if data_valid and login_valid:
            print("&&&&&&&&")
            
            # Save the login profile first
            login_profile = login_serial.save()

            # Add 'Type' and 'status' to the login profile
            login_profile.Type = 'user'  # Setting the user type as 'user'
            login_profile.status = 'PENDING'  # Setting status as 'PENDING'
            login_profile.save()

            # Add user profile data
            user_data = user_serial.validated_data
            # Saving the user profile with the login profile reference
            user_serial.save(LOGIN=login_profile, **user_data)
            
            return Response(user_serial.data, status=status.HTTP_201_CREATED)
        
        return Response({
            'login_error': login_serial.errors if not login_valid else None,
            'user_error': user_serial.errors if not data_valid else None
        }, status=status.HTTP_400_BAD_REQUEST)


# class UserReg(APIView):
#     def post(self,request):
#         print("#####",request.data)
#         user_serial= ProfileSerializer(data=request.data)
#         login_serial=LoginSerializer(data=request.data)
#         data_valid=user_serial.is_valid()
#         login_valid = login_serial.is_valid()

#         if data_valid and login_valid:
#             print("&&&&&&&&")
#             # Password=request.data['Password']
#             login_profile =login_serial.save()
#             user_serial.save(LOGIN=login_profile)
#             return Response(user_serial.data,status=status.HTTP_201_CREATED)
#         return Response({'login_error':login_serial.errors if not login_valid else None, 
#                          'user_error': user_serial.errors if not data_valid else None }, status=status.HTTP_400_BAD_REQUEST )
from rest_framework.exceptions import NotFound



class UserUpdation(APIView):
    def put(self, request, id):
        print(id)
        try:
            # Retrieve the existing user profile
            user_instance = UserTable.objects.get(LOGIN__id=id)
        except UserTable.DoesNotExist:
            raise NotFound("User not found.")
        print(request.data)
        # Serialize the incoming data
        user_serial = UpdateProfileSerializer(user_instance, data=request.data)
        


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
        print(t_user.status)
        if t_user.status == 'REJECT':
            response_dict["message"] = "failed"
            return Response(response_dict, status=status.HTTP_401_UNAUTHORIZED)
        elif t_user.status == 'PENDING':
            response_dict["message"] = "failed"
            return Response(response_dict, status=status.HTTP_401_UNAUTHORIZED)
        

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
        print("----------> profile",profile_serializer.data)
        return Response(profile_serializer.data)
    

    
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import ComplaintTable, UserTable


class ViewComplaintApi(APIView):
    def get(self, request):
        user_id = request.data.get('USER')
        complaints = ComplaintTable.objects.filter(USER__LOGIN__id=user_id)
        complaint_serializer = ComplaintViewSerializer(complaints, many=True)
        return Response(complaint_serializer.data)
    def post(self, request):
        print("POST method triggered!")
        user_id = request.data.get('USER')
        print(user_id)
        complaint_text = request.data.get('Complaint')
        date = request.data.get('Date')

        # Fetch the user based on the provided 'USER' id
        user = UserTable.objects.filter(LOGIN__id=user_id).first()
        print(user,"ssssssssssssssssssss")

        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

        # Prepare the data for the complaint and associate it with the user
        complaint_data = {
            'USER': user.id,
            'Complaint': complaint_text,
            'Date': date,  # Date should be in the correct format
        }

        # Create the complaint using the serializer
        complaint_serializer = ComplaintViewSerializer(data=complaint_data)
        print(complaint_serializer)

        # Validate and save the complaint
        if complaint_serializer.is_valid():
            complaint_serializer.save()
            return Response(complaint_serializer.data, status=status.HTTP_201_CREATED)

        return Response({
            'user_error': complaint_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


    
class ViewBudgetApi(APIView):
    def get(self,request):
        budget =BudgetTable.objects.all()
        budget_serializer = BudgetViewSerializer(budget,many=True)
        print("----------> budget",budget_serializer)
        return Response(budget_serializer.data)

# class ViewIncomeApi(APIView):
#     def get(self,request):
#         income =IncomeExpenseTable.objects.all()
#         income_serializer = IncomeViewSerializer(income,many=True)
#         print("----------> income",income_serializer)
#         return Response(income_serializer.data)
#     def post(self, request):
#         print(request.data)
#         data = request.data
#
#         # Extract the main fields from the request
#         user_id = data.get('USER')
#         user_id=UserTable.objects.filter(LOGIN__id=user_id).first().id
#         # budget_id = data.get('BUDGET')
#         items = data.get('items', [])
#
#         if not user_id or not items:
#             return Response({"error": "USER, BUDGET, and items are required fields."}, status=status.HTTP_400_BAD_REQUEST)
#
#         created_items = []
#
#         for item in items:
#             category = item.get('Category')
#             quantity = item.get('Quantity')
#             price = item.get('Price')
#
#             # Validate each item's fields
#             if not all([category, quantity, price]):
#                 return Response({"error": "Each item must include Category, Quantity, and Price."},
#                                 status=status.HTTP_400_BAD_REQUEST)
#
#             # Create a record in the database
#             record_data = {
#                 "USER": user_id,
#                 # "BUDGET_id": budget_id,
#                 "Category": category,
#                 "Quantity": quantity,
#                 "Price": price,
#             }
#
#             serializer = IncomeViewSerializer(data=record_data)
#
#             if serializer.is_valid():
#                 serializer.save()
#                 created_items.append(serializer.data)
#             else:
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         return Response({"message": "Items created successfully.", "items": created_items}, status=status.HTTP_201_CREATED)


from django.shortcuts import get_object_or_404
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal
from django.db.models import Sum
from rest_framework.views import APIView

class ViewIncomeApi(APIView):
    def get(self, request):
        income = IncomeExpenseTable.objects.all()
        income_serializer = IncomeViewSerializer(income, many=True)
        return Response(income_serializer.data)

    def post(self, request):
        data = request.data
        print("Received Data:", data)  # Debugging log

        user_id = data.get('USER')
        if not user_id:
            return Response({"error": "USER field is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = get_object_or_404(UserTable, LOGIN__id=user_id)
        except:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        items = data.get('items', [])
        if not items:
            return Response({"error": "Items are required."}, status=status.HTTP_400_BAD_REQUEST)

        created_items = []

        for item in items:
            category = item.get('Category')
            quantity = item.get('Quantity')
            price = item.get('Price')

            if not all([category, quantity, price]):
                return Response({"error": "Each item must include Category, Quantity, and Price."},
                                status=status.HTTP_400_BAD_REQUEST)

            try:
                quantity = Decimal(quantity)
                price = Decimal(price)
            except ValueError:
                return Response({"error": "Quantity and Price must be numeric values."},
                                status=status.HTTP_400_BAD_REQUEST)

            item_expense = quantity * price  # Calculate expense for the item

            # ✅ Convert `Quantity` to a string before saving
            record_data = {
                "USER": user.id,
                "Category": category,
                "Quantity": str(quantity),
                "Price": price,
                "total_expense": item_expense,
                "created_at": datetime.now()
            }

            serializer = IncomeViewSerializer(data=record_data)

            if serializer.is_valid():
                serializer.save()
                created_items.append(serializer.data)
            else:
                print("Serializer Errors:", serializer.errors)  # Debugging log
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Step 1: Calculate total expenses for the user
        total_user_expense = IncomeExpenseTable.objects.filter(USER=user).aggregate(Sum('total_expense'))['total_expense__sum'] or Decimal(0)

        # ✅ Step 2: Check if new balance is below 500 (without updating Totalincome)
        new_balance = user.Totalincome - Decimal(total_user_expense)
        alert_message = None

        if new_balance < 500:
            alert_message = f"Warning! Your remaining balance is {new_balance}. Please manage your expenses carefully."

        return Response({
            "message": "Items created successfully.",
            "items": created_items,
            "total_expense": total_user_expense,  # Show total expense in response
            "new_balance": new_balance,  # Show calculated balance (but not updating it)
            "alert": alert_message  # Send alert only if balance is low
        }, status=status.HTTP_201_CREATED)
 


    



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
    def get(self, request, id):
        user_id = UserTable.objects.filter(LOGIN__id=id).first()
        print(user_id)
        payment_history = IncomeExpenseTable.objects.filter(USER=user_id)
        serializer = TransactionViewSerializer(payment_history, many=True)
        return Response(serializer.data)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import NotificationTable


class ViewNotificationApi(APIView):
    def get(self, request, user_id):
        print('sssssss')
        user_id = UserTable.objects.filter(LOGIN__id=user_id).first()
        print(user_id)
        notifications = NotificationTable.objects.filter(user_id=user_id).order_by('-notification_date')
        print(notifications)

        # If no notifications exist for the user
        if not notifications:
            return Response({"message": "No notifications found for this user"}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the data
        notification_serializer = NotificationSerializer(notifications, many=True)

        # Return the notifications data
        return Response(notification_serializer.data, status=status.HTTP_200_OK)


