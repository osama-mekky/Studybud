from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import *
from django.db.models import Q
from .forms import RoomForm , UserForm

from django.contrib.auth.models import User
from django.contrib.auth import authenticate ,login , logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
# rooms =[
#     {'id':1 , 'name':'Lets learn Python '},
#     {'id':2 , 'name':'Django '},
#     {'id':3 , 'name':'Lets learn PHP '},
# ]

def login_page(request):

    #to know whitch div show in login_register (login div Or register div)
    page = 'login'

    #to check the user is allredy login becaues can not type http:login and open with you
    if request.user.is_authenticated:
        return redirect('home')



    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']
        user = authenticate(request , username =username , password = password)

        if user is not None :
            login(request , user)
            return redirect('home')
        else :
            messages.error(request,'Username Or Password is InVaild')   

    context ={
        'page':page
    }        

    return render(request , 'base/login_register.html',context)


def logout_page(request):
    logout(request)
    return redirect('login')

def register_page(request):
    #to know whitch div show in login_register (login div Or register div)
    form = UserCreationForm()
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Invaild data")
    context ={
        'form':form,
    }        
    return render(request,'base/login_register.html',context)

def home(request):
    #fillter topics :
    q= request.GET.get('q') if request.GET.get('q') != None else ""    

    rooms = Room.objects.filter(Q(topic__name__icontains=q)|Q(name__icontains = q)|Q(description__icontains = q))
    topics = Topic.objects.all()[0:3]
    #To Get the count of all rooms 
    ro_count = rooms.count()
    room_messages = Message.objects.all().filter(Q(room__topic__name__icontains=q))

    return render(request,'base/home.html',{'rooms':rooms,'topics':topics,'ro_count':ro_count,'room_messages':room_messages})

def room(request,pk):
    room = Room.objects.get(id=pk)
    #to get the message of this room
    room_messages =room.message_set.all()
    #to get the participants :
    participants =room.participants.all()
    #to send the comment in the Room
    if request.method == 'POST':
        comment = request.POST['body']
        message=Message.objects.create(user = request.user,room = room , body = comment)
        room.participants.add(request.user)#علشان لو المستخدم كتب تعليق يتم اضافته ف الرقم 
        return redirect('room',pk=room.id)#we should to pass the id 

    context = {'room' :room,'room_messages':room_messages,'participants':participants}          
    return render(request,'base/room.html',context)


def userProfile(request,pk):
    
    user = User.objects.get(id=pk)
    rooms =user.room_set.all() 
    room_messages=user.message_set.all()
    topics =Topic.objects.all()
    context={
        'user':user,
        'rooms':rooms,
        'room_messages':room_messages,
        'topics':topics,
    }
    return render(request,'base/profile.html',context)
    

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        form  = RoomForm(request.POST)
        if form.is_valid():
            room=form.save(commit=False)
            room.host =request.user
            room.save()
            return redirect('home')

    context = {"form":form , 'topics':topics}
    return render (request , 'base/room_form.html',context)
    

@login_required(login_url='login')
def updateRoom(request,pk):
    room =Room.objects.get(id= pk)
    topics = Topic.objects.all()
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("Not Allowed YOu")


    if request.method == 'POST':
        form = RoomForm(request.POST , instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')


    context = {"form":form , 'topics':topics}
    return render(request , 'base/room_form.html',context)

@login_required(login_url='login')
def delateRoom(request,pk):
    room = Room.objects.get(id= pk)
    if request.user != room.host:
        return HttpResponse("Not Allowed YOu")


    if request.method == 'POST':
        room.delete()
        return redirect("home")
    return render(request , 'base/delate.html',{'obj':room})


#to deleat your comment
@login_required(login_url='login')
def delate_message(request,pk):
    message = Message.objects.get(id= pk)
    if request.user != message.user:
        return HttpResponse("Not Allowed YOu")


    if request.method == 'POST':
        message.delete()
        return redirect("home")
    return render(request , 'base/delate.html',{'obj':message})

@login_required(login_url='login')
def updateUser(request):
    user =request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST , instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile',pk=user.id)


    context = {
        'form':form
    }
    return render(request,'base/update-user.html',context)


#mobile responsive

def topicsPage(request):
    q= request.GET.get('q') if request.GET.get('q') != None else ""  
    topics = Topic.objects.filter(name__icontains=q)


    return render(request , 'base/topics.html',{'topics':topics})

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request ,'base/activity.html',{'room_messages':room_messages})