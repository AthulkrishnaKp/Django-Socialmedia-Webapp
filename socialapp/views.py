from django.shortcuts import render,redirect
from socialapp.forms import PostForm,RegistrationForm,LoginForm,CommentForm

from django.urls import reverse_lazy
from socialapp.models import MyUser,Post,Comment,Followers
from django.views.generic import CreateView,FormView,ListView,View,DetailView,UpdateView
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages


# Create your views here.

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)    
    return wrapper

decs=[signin_required,never_cache]


class SignupView(CreateView,SuccessMessageMixin):
    model=MyUser   
    form_class=RegistrationForm
    template_name='register.html'
    success_message="User has been created"
    success_url=reverse_lazy('signin')
    

class LoginFormView(FormView):
    form_class=LoginForm
    template_name='login.html'

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)   
        if form.is_valid():
            uname=form.cleaned_data.get("username")   
            pwd=form.cleaned_data.get("password") 
            usr=authenticate(request,username=uname,password=pwd) 
            if usr:
                login(request,usr)
                messages.success(request,"Login Successfull")
                return redirect('home')
            else:
                messages.success(request,"Invalid Credentials")                            
                return render(request,"login.html",{"form":form})   

@method_decorator(decs,name="dispatch")
class HomeView(CreateView,ListView):
    model=Post
    form_class=PostForm
    template_name='home.html'
    context_object_name="posts"
    success_url=reverse_lazy("home")
    pk_url_kwarg='id'
    
    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form) 

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        form=CommentForm()
        context["cform"]=form
        comments=Comment.objects.all()
        context['comments']=comments
        following=Followers.objects.all().exclude(followers=MyUser.objects.get(id=self.request.user.id))
        context['following']=following
        f=Followers.objects.all().filter(followers=MyUser.objects.get(id=self.request.user.id))        
        context['follow']=f
        userlist=MyUser.objects.all().exclude(username=self.request.user)
        context['userlist']=userlist
        return context

@method_decorator(decs,name="dispatch")        
class CommentListView(ListView):
    model=Comment
    template_name='home.html'
    context_object_name="allcomments"

@method_decorator(decs,name="dispatch")
class UserView(ListView):
    model=MyUser
    template_name='home.html'
    context_object_name='users'

@method_decorator(decs,name="dispatch")
class CommentFormView(CreateView):
    model=Comment
    form_class=PostForm
    template_name='home.html'
    success_url='home'

    def post(self, request, *args, **kwargs):
        form=CommentForm(request.POST)
        if form.is_valid():
            p_id=kwargs.get('id')  
            comment=form.cleaned_data.get("comments")
            user=self.request.user
            post=Post.objects.get(id=p_id)
            Comment.objects.create(comments=comment,user=user,post=post)     
            messages.success(request,"Comment Posted Successfully")                              
            return redirect("home")            
        else:
            messages.error(request,"Comment Posting Failed")
            return redirect("home")

@method_decorator(decs,name="dispatch")
class PostDetailView(DetailView):
    model=Post
    template_name='postdetail.html'
    context_object_name='post'
    pk_url_kwarg='id'
    
    def get(self, request, *args, **kwargs):
        id=kwargs.get("id")
        comments=Comment.objects.all()
        post=Post.objects.get(id=id)
        cform=CommentForm
        return render(request,'postdetail.html',{'post':post,'comments':comments,"cform":cform})
    
@method_decorator(decs,name="dispatch")    
class CommentListView(ListView):
    model=Comment
    template_name='postdetail.html'
    context_object_name="comments"
    
    def get_queryset(self):
        return Comment.objects.all()

@method_decorator(decs,name="dispatch")
class ProfileView(ListView):
    model=Post
    template_name='profile.html'
    context_object_name='profile'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        p=Post.objects.filter(user=self.request.user)
        context["profile"]=p
        followers=Followers.objects.all().filter(user=MyUser.objects.get(id=self.request.user.id))
        context['followers']=followers
        following=Followers.objects.all().filter(followers=MyUser.objects.get(id=self.request.user.id))
        context['following']=following
        return context


@method_decorator(decs,name="dispatch")
class ProfileUpdateView(UpdateView):
    model=MyUser
    form_class=RegistrationForm
    template_name="profileupdate.html"
    pk_url_kwarg='id'
    success_url=reverse_lazy("profile")

decs
def signout_view(request,*args,**kwargs):
    logout(request)
    messages.success(request,"User Logged out")
    return redirect("signin")

decs
def like_post(request,*args,**kwargs):
    p_id=kwargs.get("id")
    p=Post.objects.get(id=p_id)
    p.no_of_likes.add(request.user)
    p.save()
    messages.success(request,"You Liked the post")
    return redirect('home')
    
decs    
def unlike_post(request,*args,**kwargs):
    p_id=kwargs.get("id")
    p=Post.objects.get(id=p_id)
    p.no_of_likes.remove(request.user)
    p.save()
    messages.success(request,"You Unliked the Post")
    return redirect('home')
       
@method_decorator(decs,name="dispatch")       
class PostUpdateView(UpdateView):
    model=Post
    form_class=PostForm
    template_name="postupdate.html"
    pk_url_kwarg='id'
    success_url=reverse_lazy("profile")

@method_decorator(decs,name="dispatch")
class PostDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        Post.objects.filter(id=id).delete() 
        messages.success(request,"You Deleted one of your Post")    
        return redirect("profile") 

decs    
def userprofileview(request,*args,**kwargs):   
    id=kwargs.get('id')
    user=MyUser.objects.get(id=id)
    post=Post.objects.filter(user_id=id)
    comments=Comment.objects.all()
    return render(request,'userprofile.html',{'user':user,'post':post,'comments':comments})

decs    
def commentdeleteview(request,*args,**kwargs):
    id=kwargs.get('id')
    Comment.objects.filter(id=id).delete()
    messages.success(request,"Comment Deleted")
    return redirect('home')

decs
def follow(request,*args,**kwargs):
    fid=kwargs.get('id')
    user=MyUser.objects.get(id=fid) 
    follower=request.user   
    try:
        Followers.objects.create(user=user,followers=follower)
        Followers.save()
        return redirect('home')    
    except:
        messages.success(request,"You are Following this user")
        return redirect('home')
    
    
decs
def unfollow(request,*args,**kwargs):
    fid=kwargs.get('id')
    user=MyUser.objects.get(id=fid)
    follower=request.user
    try:  
        Followers.objects.get(user=user,followers=follower).delete()
        Followers.save()
        return redirect('home')
    except:    
        messages.success(request,"You Unfollowed the user")
        return redirect('home')



# decs
# def followers_count(request,*args,**kwargs):
#     fid=kwargs.get('id')
#     user=MyUser.objects.get(id=fid)
#     followers=Followers.objects.get(user=user)
#     return render(request,'profile.html',{'follow':followers})

