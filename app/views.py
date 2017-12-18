from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from . import forms
from django.core.exceptions import ValidationError
from os import listdir, remove
from os.path import isfile, join
from PIL import ImageFilter, Image
from django.views import View
from app import models


class Feed(View):
    def get(self, request):
        docs = models.Document.objects.all()
        html = '<div class="col-lg-4">'
        if len(docs) == 1:
            html = '<div class="col-lg-6 col-lg-offset-3">'
        elif len(docs) == 2:
            html = '<div class="col-lg-6">'
        return render(request, 'app/base.html', {'docs': docs, 'html': html})


class Upload(View):
    def post(self, request):
        form = forms.DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            path = 'app/static/' + models.Document.objects.last().image_url()
            image = Image.open(path)
            w, h = image.size
            s = min(w, h)
            image = image.crop(box=(int((w - s) / 2), int((h - s) / 2), int(
                (w + s) / 2), int((h + s) / 2)))
            image.save(path)
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
        if form.is_valid():
            filt = form.get_filter()
            if isinstance(filt, str):
                image.convert('L').convert('RGB').save(path)
            else:
                image.filter(filt).save(path)
            return redirect('app:feed')
        else:
            return redirect('app:feed')


class Rotate(View):
    def post(self, request, img_id):
        form = forms.FilterForm(request.POST)
        path = 'app/static/' + models.Document.objects.get(
            id=img_id).image_url()
        image = Image.open(path)
        image.rotate(-90).save(path)
        return redirect('app:feed')


class Delete_Picture(View):
    def post(self, request, img_id):
        form = forms.FilterForm(request.POST)
        path = 'app/static/' + models.Document.objects.get(
            id=img_id).image_url()
        models.Document.objects.get(id=img_id).delete()
        remove(path)
        return redirect('app:feed')