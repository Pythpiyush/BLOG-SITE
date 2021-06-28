from django.shortcuts import render,HttpResponse,redirect
from .models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
def home(request):
    return render(request,'home/home.html')


def contact(request):
    if request.method=='POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        content = request.POST.get('content', '')
        if len(name)<3 or len(email)<4 or len(phone)<10 or len(content)<10:
           messages.error(request,'Please Enter details correctly')
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, 'Your Contact is saved')
        # return render(request, 'home/contact.html')
    return render(request, 'home/contact.html')





def about(request):
    return render(request,'home/about.html')

def search(request):
    query=request.GET.get('query','')
    if len(query)>78:
        allPosts=Post.objects.none()
    else:
        allPostsTitle=Post.objects.filter(title__icontains=query)
        allPostsContent=Post.objects.filter(content__icontains=query)
        allPosts=allPostsTitle.union(allPostsContent)
    if allPosts.count()==0:
        messages.warning(request,"Please enter query Correctly")
    params={'allPosts':allPosts,'query':query}
    return render(request,'home/search.html',params)

def handleSignup(request):
    if request.method=='POST':
        username=request.POST.get('username')
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')

        if len(username)>10:
            messages.error(request, "Username must be under 10 characters!!")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, "Username must alphanumeric characters!!")
            return redirect('home')

        if(pass1!=pass2):
            messages.error(request, "Passwords donot match")
            return redirect('home')

        myuser=User,objects.create_user(username,email,pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        messages.success(request,"Your account is created successfully")
        return redirect('home')
    else:
        return HttpResponse("404-Not Found")

def handleLogin(request):
    if request.method=='POST':
        loginusername=request.POST.get('loginusername')
        loginpassword=request.POST.get('loginpassword')
        user=authenticate(username=loginusername,password=loginpassword)
        if user is not None:
            login(request,user)
            messages.success(request,"Successfully logged In")
            return redirect('home')
        else:
            messages.error(request,"Invalid Credentials")
            return redirect('home')
    return HttpResponse('404-Not Found')

def handleLogout(request):
    logout(request)
    messages.success(request,"Successfully logged out")
    return redirect('home')
