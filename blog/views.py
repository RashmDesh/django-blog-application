from django.shortcuts import render,redirect
from django.http import HttpResponse
from .form import Blogform
from blog.models import blogpost
from login.models import bloguser
from django.views import View
from .serializers import BlogSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.


class BlogAdd(View):
    def get(self, request):
        form= Blogform()
        return render(request,"blogform.html",{'form':form})
    
    def post(self, request):
        form = Blogform(request.POST, request.FILES)
        #if form.is_valid():
           #title = form.cleaned_data['title']
            #content = form.cleaned_data['content']
            #category = form.cleaned_data['category']
            #created_on=form.cleaned_data['created_on']
            #file = form.cleaned_data['file']
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        created_on=request.POST.get('created_on')
        file = request.POST.get('file')
        email = request.session["email"]
        obj = bloguser.objects.get(email=email)
        auther=obj
        
            #context={"title":title,"post":content,"Date":created_on,"author":author}
        user_data=blogpost(title=title,auther=auther,content=content,created_on=created_on,category=category,file=file)
        user_data.save()

            #return render(request,"blog.html",{'post':context})
        return redirect("/blog/")
        
        #else:
         #   msg = "invalid form"
          #  return render(request, 'blogform.html', {'msg': msg})


def blog(request):
    form=blogpost.objects.all()
    context={'post':form}                
    return render(request,"blog.html",context)

'''
def addblog(request):
    if request.method=="POST":
    
        form=Blogform(request.POST)
        
        title=request.POST.get('title')
        created_on=request.POST.get('created_on')
        content=request.POST.get('content')
        #author =request.POST.get('author') 
        email=request.session['email']
        obj=bloguser.objects.get(email=email)
        auther=obj
        
   
   
        #context={"title":title,"post":content,"Date":created_on,"author":author}
        user_data=post(title=title,created_on=created_on,content=content,auther=auther)
        user_data.save()

        #return render(request,"blog.html",{'post':context})
        return redirect("/blog/")
    
        
        
    if request.method=="GET":
        form= Blogform()
        return render(request,"blogform.html",{'form':form})
'''


class BlogApi(APIView):
    def get(self, request):
        all_data = blogpost.objects.all()
        res = BlogSerializer(all_data, many=True)
        return Response(res.data)