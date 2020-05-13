from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser,ParseError
from chat.models import Message, UserProfile, Userdetails
from chat.serializers import MessageSerializer, UserSerializer
from rest_framework.views import APIView
from ChatApp.settings import *
from .flutterutils import *
from .serializers import UseresSerializer, userLoginSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
import uuid 
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.parsers import JSONParser
from rest_framework.decorators import parser_classes

@csrf_exempt
def index(request):
    if request.user.is_authenticated:
        return Response({'data':'0'})
    if request.method == 'GET':
        return Response({'data': 'Please Login'})
    if request.method == "POST":
        username, password = request.POST['username'], request.POST['password']
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            dic={'data':User.objects.all()}
            print(dic)
        else:
            return HttpResponse('{"error": "User does not exist"}')
        return Response({'data':'0'})


@csrf_exempt
@api_view(['POST',])
def Login(request):
    if request.method == 'POST':

        serializer = userLoginSerializer(data=request.data)
        data={}
        if serializer.is_valid():
            
            data['response'] = "0"
            return Response(data)
        else:
            data['response'] = "1"
            return Response(data)

@csrf_exempt
@api_view(['POST','GET',])
@parser_classes([JSONParser])
def user_list(request, pk=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        if pk:
            users = User.objects.filter(id=pk)
        else:
            users = User.objects.all()
        serializer = UserSerializer(users, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            user = User.objects.create_user(username=data['username'], email=data['email'], password=data['password'])
            UserProfile.objects.create(user=user)
            Userdetails.objects.create(user=user)
            return JsonResponse(data, status=201)
        except Exception:
            return JsonResponse({'error': "Something went wrong"}, status=400)

@csrf_exempt
@api_view(['POST',])
def Registration(request):
    if request.method == 'POST':

        serializer = UseresSerializer(data=request.data)
        data={}
        dat={}
        if serializer.is_valid():
            serializer.save()
            
            data['username'] = User.username
            data['email'] = User.email
           
            data['password'] = User.password
            dat['response'] = "1"
            return Response(dat)
        else:
            data['response'] = "0"
        return Response(data)


@csrf_exempt
def message_list(request, sender=None, receiver=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        messages = Message.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.is_read = True
            message.save()
            alls=User.objects.all()
            print(alls)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def register_view(request):
    """
    Render registration template
    """
    if request.user.is_authenticated:
        return redirect('chats')
    return render(request, 'chat/register.html', {})


def chat_view(request):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return Response({'users': User.objects.exclude(username=request.user.username)})


def message_view(request, sender, receiver):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return Response(
                      {'users': User.objects.exclude(username=request.user.username),
                       'receiver': User.objects.get(id=receiver),
                       'messages': Message.objects.filter(sender_id=sender, receiver_id=receiver) |
                                   Message.objects.filter(sender_id=receiver, receiver_id=sender)})





@csrf_exempt
@api_view(['POST',])
def update_profile(request, u=None):
    user = User.objects.get(username=u)
    user.userdetails.otp = 'Lorem'
    user.userdetails.description='nkdnfkdnf'

    user.save()
    data={'Response': save}
    return Response(data)




@api_view(['POST',])
def ForgotPasswordUser(request):
    if request.method=='GET':
        e= request.POST['username']
        data={}
        try:

            instance=User.objects.filter(username=e)
            for i in instance:
                ID=i.id
                e=i.email
             
                break
            user = User.objects.get(pk=ID)
            p=uuid.uuid4().hex[:6].upper()
            user.userdetails.otp=p
            user.save()
            n=sendmail(e,p)
            if n==1:
                data['Response']='Password has been sent'
                return Response(data)
            else:
                data['Response']='Enter valid email ID'
            return Response(data)

        except:
            data['Response']='Enter valid email ID'
            return Response(data)



@api_view(['POST',])
def findotp(request):
    if request.method=="POST":
        e=request.POST['username']
        otp=request.POST['otp']
        k=request.POST['password']
        data={}
        try:
            u = User.objects.get(username=e)
            if u.userdetails.otp==otp:
                print('yes')
                u.set_password(k)
                u.save()
                data['Response']='1' 
                return Response(data)
        except:
            data['Response']='0'
            return Response(data)

