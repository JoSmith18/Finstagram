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
from resizeimage import resizeimage
from random import randint
from app import filters


class Feed(View):
    def get(self, request):
        docs = models.Document.objects.all().order_by('-uploaded_at')
        videos = models.Video.objects.all().order_by('-uploaded_at')
        comment_form = forms.CommentForm()
        total = docs.count() + videos.count()
        return render(request, 'app/base.html', {
            'docs': docs,
            'total': total,
            'videos': videos,
            'comment_form': comment_form
        })


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
            image = resizeimage.resize_cover(image, [500, 500], validate=False)

            image.save(path)
            return redirect('../feed/')
        else:
            return render(request, 'app/upload.html', {'form': form})

    def get(self, request):
        form = forms.DocumentForm()

        return render(request, 'app/upload.html', {'form': form})


class Upload_Video(View):
    def post(self, request):
        form = forms.VideoForm(request.POST, request.FILES)
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
            return render(request, 'app/uploadvideo.html', {'form': form})

    def get(self, request):
        form = forms.VideoForm()

        return render(request, 'app/uploadvideo.html', {'form': form})


class Filter(View):
    def get(self, request, doc_id):
        form = forms.FilterForm()
        path = models.Document.objects.get(id=doc_id).image_url()
        return render(request, 'app/filter.html', {'form': form, 'path': path})

    def post(self, request, doc_id):
        form = forms.FilterForm(request.POST)
        path = 'app/static/' + models.Document.objects.get(
            id=doc_id).image_url()
        image = Image.open(path)
        if form.is_valid():
            filt = form.get_filter()
            filters.filtering(filt, image, path)
            return redirect('app:feed')
        else:
            return redirect('app:feed')


class Rotate(View):
    def post(self, request, doc_id):
        form = forms.FilterForm(request.POST)
        path = 'app/static/' + models.Document.objects.get(
            id=doc_id).image_url()
        image = Image.open(path)
        image.rotate(-90).save(path)
        return redirect('app:feed')


class Delete_Picture(View):
    def post(self, request, doc_id):
        form = forms.FilterForm(request.POST)
        path = 'app/static/' + models.Document.objects.get(
            id=doc_id).image_url()
        models.Document.objects.get(id=doc_id).delete()
        remove(path)
        return redirect('app:feed')


class Delete_Video(View):
    def post(self, request, doc_id):
        form = forms.FilterForm(request.POST)
        path = 'app/static/' + models.Video.objects.get(id=doc_id).image_url()
        models.Video.objects.get(id=doc_id).delete()
        remove(path)
        return redirect('app:feed')


class Add_Comment(View):
    def post(self, request, document_id):
        document = models.Document.objects.get(id=document_id)
        form = forms.CommentForm(document, request.POST)
        if form.is_valid():
            form.save()
            return redirect('app:feed')
        else:
            return redirect('app:feed')


class Add_Comment_Video(View):
    def post(self, request, document_id):
        video = models.Video.objects.get(id=document_id)
        form = forms.CommentOnVideoForm(video, request.POST)
        if form.is_valid():
            form.save()
            return redirect('app:feed')
        else:
            return redirect('app:feed')


class Like_Pic(View):
    def post(self, request, doc_id):
        d = models.Document.objects.get(id=doc_id)
        d.likes += 1
        d.save()
        return redirect('app:feed')


class Like_Vid(View):
    def post(self, request, doc_id):
        d = models.Video.objects.get(id=doc_id)
        d.likes += 1
        d.save()
        return redirect('app:feed')


class DisLike_Pic(View):
    def post(self, request, doc_id):
        d = models.Document.objects.get(id=doc_id)
        d.dislikes += 1
        d.save()
        return redirect('app:feed')


class DisLike_Vid(View):
    def post(self, request, doc_id):
        d = models.Video.objects.get(id=doc_id)
        d.dislikes += 1
        d.save()
        return redirect('app:feed')