
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class MyUser(AbstractUser):
    bio=models.TextField(blank=True)
    profile_pic=models.ImageField(upload_to="profilepics",default="profilepics/default-propic.png")
    location=models.CharField(max_length=100,blank=True)
                                     
    
class Post(models.Model):
    user=models.ForeignKey(MyUser,on_delete=models.CASCADE)
    caption=models.CharField(max_length=200)
    images=models.ImageField(null=True,upload_to="images",blank=True)
    no_of_likes=models.ManyToManyField(MyUser,related_name="likes")
    created_date=models.DateField(auto_now_add=True)
    is_active=models.BooleanField(default=True)
                   
    def __str__(self):     
        return self.user

class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    comments=models.CharField(max_length=200)
    user=models.ForeignKey(MyUser,on_delete=models.CASCADE)


class Followers(models.Model):
    user=models.ForeignKey(MyUser,on_delete=models.CASCADE,related_name='user')
    followers=models.ForeignKey(MyUser,blank=True,default=True,related_name='followers',on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('user','followers',)

    def __str__(self):     
        return self.user
    
