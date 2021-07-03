from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('',views.index,name='Home'),
	path('VideoViewer',views.video_viewer,name='ShowfaceVideo'),
    path('uploadhippo', views.UploadHippo, name='UploadHippo'),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)