
from django.contrib import admin
from django.conf import settings
from django.urls import path, include, re_path
#from django.conf.urls import url
from accounts.views import index, donation
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", index, name="index"),
    path('admin/', admin.site.urls),
    #path('chat/', include('django_chatter.urls', namespace = 'django_chatter'), name="chat"),
    path('accounts/', include('accounts.urls')),
    re_path(r'^auth/', include('social_django.urls', namespace='social')),
    path('users/', include('users.urls')),
    #path('courses/', include('courses.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('qna/', include('qna.urls', namespace='qna')),
    path('quiz/', include('quizes.urls', namespace='quizes')),
    path('courses/', include('sinx.urls', namespace = 'sinx')),
    path('accounts/password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('accounts/password_reset_confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('accounts/password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    
    path("suPpoRt/", donation, name = "support"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
#urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)