from django.contrib import admin
from django.urls import path
from socialapp import views
from django.conf import settings

from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.LoginFormView.as_view(),name='signin'),
    path('register/',views.SignupView.as_view(),name='register'),
    path('home/',views.HomeView.as_view(),name="home"),
    path('home/comment/<int:id>',views.CommentFormView.as_view(),name="comment"),
    path('logout/',views.signout_view,name='signout'),
    path('home/myprofile',views.ProfileView.as_view(),name='profile'),
    path('home/like/<int:id>',views.like_post,name="like"),
    path('home/unlike/<int:id>',views.unlike_post,name="unlike"),
    path('home/myprofile/<int:id>',views.PostDetailView.as_view(),name="postdetail"),
    path('home/myprofile/post/<int:id>/update',views.PostUpdateView.as_view(),name='postupdate'),
    path('home/myprofile/<int:id>/delete',views.PostDeleteView.as_view(),name='postdelete'),
    path('home/myprofile/<int:id>/comments',views.CommentListView.as_view(),name="allcomments"),
    path('home/userprofile/<int:id>',views.userprofileview,name="allusers"),
    path('home/myprofile/update/<int:id>',views.ProfileUpdateView.as_view(),name='profileupdate'),
    path('home/comment/<int:id>/delete',views.commentdeleteview,name='commentdelete'),
    path('home/profile/follow/<int:id>',views.follow,name='follow'),
    path('home/profile/Unfollow/<int:id>',views.unfollow,name='unfollow')


    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
