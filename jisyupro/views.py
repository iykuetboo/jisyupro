from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import *
from .models import *
from .facedetector_1 import *
from .facedetector_2 import *
from .facedetector_3 import *

def index(request):
    return HttpResponse("Hello, world. You're at the jisyupro index.")

def testImage(request):
    if request.method=="POST":
        img = request.FILES['image']
        print(request.FILES)
        model = FaceImage()
        model.img = img
        img_name = "test_upload"
        model.save()
        return HttpResponse("Hello, testImage was saved.")
    else:
        return HttpResponse("Hello, please POST image.")


def newImage(request):
    params = {}
    if request.method == "POST":
        form = FaceImageForm(request.POST)
        params['form'] = form
        if form.is_valid():
            mem,created = Member.objects.get_or_create(name=request.POST['your_name'])
            if created:
                mem.save()
            num = mem.faceimage_set.all().count()
            img_name  = "{:03d}_{}_{:03d}".format(mem.pk,mem.name,num)
            img = save_clipped_face(img_name,request.FILES['image'])
            if img is None:
                params['msg'] = "顔が認識できませんでした。別の画像をお使いください。"
                return render(request,'jisyupro/faceform.html', params)

            model = FaceImage()
            model.image = img
            model.name = img_name
            model.person = mem
            model.save()
            return redirect('/jisyupro/imagelist/'+str(mem.pk))
    else:
        form = FaceImageForm()
        params['form'] = form
    return render(request,'jisyupro/faceform.html', params)

def imageList(request,pk):
    params = {}
    mem = Member.objects.get(pk=pk)
    images =  FaceImage.objects.filter(person=mem).order_by('-id')[:10]
    params['images'] = images
    return render(request,'jisyupro/imageList.html', params)

def delete_image(request,pk):
    params = {}
    image =  FaceImage.objects.get(pk=pk)
    mem = image.person
    image.delete()
    return redirect('/jisyupro/imagelist/'+str(mem.pk))

def train(request):
    train_faces()
    return redirect('/jisyupro/recognize')

def recognize(request):
    params = {}
    if request.method == "POST":
        img = request.FILES['image']
        ret = recognize_face(img)
        if ret is None:
            params['msg'] = "顔が認識できませんでした。別の画像をお使いください。"
            return render(request,'jisyupro/recognize.html', params)
        params['id'] = ret[0]
        params['confidence'] = ret[1]
        params['img'] = ret[2]
        return render(request,'jisyupro/recognized_result.html', params)
    else:
        return render(request,'jisyupro/recognize.html', params)
