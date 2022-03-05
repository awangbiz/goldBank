from concurrent.futures.thread import _global_shutdown_lock
from rest_framework import viewsets

from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework import status
import json
from .serializer import AccountSerializer
from .models import Account
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class AccountViewSets(viewsets.ModelViewSet):
    queryset = Account.objects.all().order_by('id')
    serializer_class = AccountSerializer

    #GET / Retrieve Override
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Exception as e:
           
            return Response({'status':'failed','error_msg':'not found'},status=status.HTTP_404_NOT_FOUND)
        else:
            #any additional logic
            serializer = self.get_serializer(instance)
            return Response({'status':'success','data': serializer.data})
        
    
    #DELETE Overide
    def destroy(self, request, *args, **kwargs):
        try:
            # Account.objects.filter(acc_type='investment')
            print(args)
            print(kwargs)
            print(request)
            account = Account.objects.get(pk = kwargs['pk'] ,acc_type__iexact='investment')
            
            if account.balance > 0.0:
                #get saving acc
                saving = Account.objects.get(acc_type__iexact='saving')
                saving.balance = saving.balance + account.balance
                saving.save()
            operation = account.delete()
            # data = {}
            if operation:
                return Response({'status':'success'})
           
        except Exception as e:
            return Response({'status':'failed','error_msg':'not found'},status=status.HTTP_404_NOT_FOUND)
        

    @action(detail=False, methods=['POST',], )
    def getAccountType(self, request, *args, **kwargs):
        try:
            res = {}
            req = None

            if request.method == 'POST':
                try:
                    req = json.loads(request.body.decode("utf-8"))
                except Exception as e:
                    res["details"] = 'invalid JSON request body'
                    return JsonResponse({'status':'failed', 'error_msg': res["details"]}, content_type="application/json",status=status.HTTP_400_BAD_REQUEST)
            
            elif request.method == 'GET':
                req =request.query_params 
                if 'acc_type' not in req:
                     return JsonResponse({'status':'failed', 'error_msg': "missing parameter in GET Request"}, content_type="application/json",status=status.HTTP_400_BAD_REQUEST)

            queryset =  Account.objects.order_by('-id').filter(acc_type__iexact=req['acc_type'])[:1]
        
            if(len(queryset) <= 0):
                return JsonResponse({'status':'failed', 'error_msg':'Record Not Found'}, content_type="application/json",status=status.HTTP_404_NOT_FOUND)
            serializer = AccountSerializer(queryset[0]);
            result = {}
            if serializer.is_valid:
                result = serializer.data
        
            return JsonResponse({'status':'success', 'ID':result['id'],'account type ': result['acc_type'],'balance': result['balance']}, content_type="application/json",status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({'status':'failed', 'result': {}, 'error_msg':str(e)}, content_type="application/json",status=status.HTTP_404_NOT_FOUND)
   
    @action(detail=False, methods=['GET',], name='delete account by name')
    def deleteInvestmentAccount(self, request, *args, **kwargs):
        account={}
        try:
            account = Account.objects.get(acc_type__iexact='investment')          
        except Exception as e:
            # logger.exception('Exception caught: %s, views', str(e))
            return Response({'status':'failed','error_msg':'account type not found'},status=status.HTTP_404_NOT_FOUND)
        try:
            if account.balance > 0.0:
                #get saving acc
                saving = Account.objects.get(acc_type__iexact='saving')
                saving.balance = saving.balance + account.balance
                saving.save()

            operation = account.delete()
            # data = {}
            if operation:
                return Response({'status':'success'})
        except Exception as e:
            return Response({'status':'failed','error_msg':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @swagger_auto_schema(
        operation_description="amount to transfer",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['amount'],
            properties={
                'amount': openapi.Schema(type=openapi.TYPE_NUMBER)
            },
        ),
        # security=[],
        # tags=['Users'],
    )
    @action(detail=False, methods=['POST',], name='transfer to goal')
    def transferSavingToGoalAcc(self, request, *args, **kwargs):
        """
            This text is the description for this API.

            ---
            parameters:
            - name: amount
            description: transfer amount
            required: true
            type: float
            paramType: form
        """
        try:
            res = {}
            req = None

            if request.method == 'POST':
                try:
                    req = json.loads(request.body.decode("utf-8"))
                except Exception as e:
                    res["details"] = 'invalid JSON request body'
                    return JsonResponse({'status':'failed', 'error_msg': res["details"]}, content_type="application/json",status=status.HTTP_400_BAD_REQUEST)
            elif request.method == 'GET':
                req =request.query_params 
                if 'acc_type' not in req:
                        return JsonResponse({'status':'failed', 'error_msg': "missing parameter in GET Request"}, content_type="application/json",status=status.HTTP_400_BAD_REQUEST)

            amount = req['amount']

            #deduct saving account
            saving = Account.objects.get(acc_type__iexact='saving')
            bal = saving.balance
            if amount > bal:
                return JsonResponse({'status':'failed', 'error_msg': "insufficient balance"}, content_type="application/json",status=status.HTTP_200_OK)

            newbalance = bal-amount
            saving.balance = newbalance
            saving.save()

            # credit to goal account
            goal = Account.objects.get(acc_type__iexact='goal')
            goal.balance = goal.balance + amount
            goal.save()
        
            return JsonResponse({'status':'success', 'ID':goal.id,'account type ':goal.acc_type,'balance': goal.balance}, content_type="application/json",status=status.HTTP_200_OK)

        except Exception as e:
            # logger.exception('Exception caught: %s, views',  str(e))
            return JsonResponse({'status':'failed', 'result': {}, 'error_msg':str(e)}, content_type="application/json",status=status.HTTP_404_NOT_FOUND)

        
