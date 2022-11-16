
from django import forms
from django.contrib.auth.forms import UserCreationForm
from socialapp.models import MyUser,Post,Comment


class PostForm(forms.ModelForm):
    class Meta():
        model=Post
        fields=[
            "caption",
            "images"
        ]
        
        widgets={
            "caption":forms.Textarea(attrs={"class":"form-control border border-warning mt-2","rows":3,"placeholder":"write a caption .."}),
            "images":forms.FileInput(attrs={"class":"form-select mt-2"})
        }

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control border border-info","PlaceHolder":"..."}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control border border-info","PlaceHolder":"..."}))



class RegistrationForm(UserCreationForm):
    
    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control border border-info ","placeholder":"enter password"}))  
    password2=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control border border-info","placeholder":"confirm password"}))              
    
   
    class Meta:
        model = MyUser
        fields = ['first_name','last_name','username','email','bio','profile_pic','location']

        widgets={
            "first_name":forms.TextInput(attrs={"class":"form-control border border-info","placeholder":"enter firstname"}),
            "last_name":forms.TextInput(attrs={"class":"form-control border border-info","placeholder":"enter lastname"}),
            "username":forms.TextInput(attrs={"class":"form-control border border-info","placeholder":"enter username"}),
            "email":forms.EmailInput(attrs={"class":" form-control border border-info","placeholder":"enter email"}),
            "bio":forms.TextInput(attrs={"class":" form-control border border-info","placeholder":" your Bio .."}),
            "location":forms.TextInput(attrs={"class":"form-control border border-info","placeholder":"enter your location "}),
        }

class CommentForm(forms.ModelForm):
    class Meta():
        model=Comment
        fields=[
            "comments",          
        ]
        widgets={
            "comments":forms.Textarea(attrs={"class":"form-control border border-warning mt-2","rows":3,"placeholder":"write your comment.."}),
        }




# class PostUpdateForm(forms.ModelForm):
#     class Meta:
#         model=Post
#         fields=["caption","images"]    
