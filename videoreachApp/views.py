from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import requests
import json
import subprocess
import os
# Create your views here.

def index(request):
	if request.method == 'GET':
		return render(request,'index.html')
	
	elif request.method == 'POST':
		return render(request,'index.html')

def video_viewer(request):
    if request.method == 'GET':
        return render(request, 'videoreachApp/index.html')

    elif request.method == 'POST':
        try:
            print(request.FILES['data1'])
            video1 = request.FILES['data1'].read()
            file1 = open("media/camera.mp4",'wb')
            file1.write(video1)
            file1.close()

            video2 = request.FILES['data2'].read()
            file2 = open("media/screen.mp4",'wb')
            file2.write(video2)
            file2.close()
            # mixing screen and face+audio recordering video.....
            try:
                cmd = 'ffmpeg -y -i media/screen.mp4 -i media/camera.mp4 -filter_complex "[1:v][0:v]scale2ref=(256/79)*ih/8/sar:(256/102)*ih/8[wm][base]; [base][wm]overlay=0:main_h-(overlay_h+10):shortest=1; pan=stereo|c0=2*c0|c1=3*c0[a0];[1:a]pan=stereo|c0=1*c0|c1=4*c0[a1];[a0][a1]amix=inputs=2:duration=first:dropout_transition=2" media/combinedVideoOutput_final.mp4'
                subprocess.call(cmd, shell=True)
                file_manager()
                return JsonResponse({"message": 'Successfly Recoded Video.','url':"media/combinedVideoOutput_final.mp4"})
            except Exception as e:
                return JsonResponse({"message": 'Get Error at Mixing Video time and error is '+str(e)})
        except Exception as e:
            return JsonResponse({"message": 'Get Error is '+str(e)})


def UploadHippo(request):
    if request.method == 'GET':
        return HttpResponse({'staus': 'Success'} )
    elif request.method == 'POST':
        session_requests = requests.session()
        url = 'https://www.hippovideo.io/api/v1/me/video/import'
        payload = {
            'title':'demo',
            'url':'https://95d4b6998ac3.ngrok.io/media/combinedVideoOutput_final.mp4',#change url after server live
            'email':'michael.giles@group.videooutreach.io',
            'api_key':'KV4gQIQ5RIMiDr5Nu5BAkQtt',
        }
        response = session_requests.post(url,data=payload)
        print(response.text)
        response_json = json.loads(response.text)
        if response_json['code'] == 200:
            return JsonResponse({"message": 'Uploaded Video ID Is : '+str(response_json['video_id']),'url':response_json['thumbnail_preview']})
        else:
            return JsonResponse({"message": "Error code: "+str(response_json['code'])+"<br/> Type: "+str(response_json['type'])})


def file_manager():
    "Required and wanted processing of final files"
    local_path = os.getcwd()
    if os.path.exists(str(local_path) + "/media/camera.mp4"):
        os.remove(str(local_path) + "/media/camera.mp4")
    if os.path.exists(str(local_path) + "/media/screen.mp4"):
        os.remove(str(local_path) + "/media/screen.mp4")
