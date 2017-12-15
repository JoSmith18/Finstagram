from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from . import forms
from django.core.exceptions import ValidationError
from os import listdir
from os.path import isfile, join
from PIL import ImageFilter, Image
from django.views import View
from app import models


class Feed(View):
    def get(self, request):
        docs = models.Document.objects.all()
        return render(request, 'app/base.html', {'docs': docs})


class Upload(View):
    def post(self, request):
        form = forms.DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('../feed/')
        else:
            return render(request, 'app/upload.html', {'form': form})

    def get(self, request):
        form = forms.DocumentForm()

        return render(request, 'app/upload.html', {'form': form})


class Filter(View):
    def get(self, request, img_id):
        form = forms.FilterForm()
        path = 'app/static/' + models.Document.objects.get(
            id=img_id).image_url()
        return render(request, 'app/upload.html', {'form': form, 'path': path})

    def post(self, request, img_id):
        form = forms.FilterForm(request.POST)
        path = 'app/static/' + models.Document.objects.get(
            id=img_id).image_url()
        image = Image.open(path)
        size = (640, 640)
        if form.is_valid():
            filt = form.get_filt()
            image.filter(filt).save(path)
            image.thumbnail(size)
            image.save(path)
            return redirect('app:feed')
        else:
            return redirect('app:feed')


# def filter_Pic(path, filt):
#     image = Image.open(path)
#     new_img = image.filter(ImageFilter.filt)
#     d.DocumentForm('app/static/app/images/' + path)
