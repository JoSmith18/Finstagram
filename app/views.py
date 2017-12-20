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


class Feed(View):
    def get(self, request):
        docs = models.Document.objects.all()
        videos = models.Video.objects.all()
        comment_form = forms.CommentForm()
        html = '<div class="col-lg-4">'
        if len(docs) == 1:
            html = '<div class="col-lg-6 col-lg-offset-3">'
        elif len(docs) == 2:
            html = '<div class="col-lg-6">'
        return render(request, 'app/base.html', {
            'docs': docs,
            'html': html,
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
    def get(self, request, img_id):
        form = forms.FilterForm()
        path = models.Document.objects.get(id=img_id).image_url()
        return render(request, 'app/filter.html', {'form': form, 'path': path})

    def post(self, request, img_id):
        form = forms.FilterForm(request.POST)
        path = 'app/static/' + models.Document.objects.get(
            id=img_id).image_url()
        image = Image.open(path)
        if form.is_valid():
            filt = form.get_filter()
            if filt == 'Black':
                image.convert('L').convert('RGB').save(path)
            elif filt == 'Jofilt':
                image2 = Image.open(
                    '/home/basecamp/Documents/DailyExercises/Dec/Finstagram/app/static/app/images/jofilter.jpg'
                )
                Image.blend(image, image2, 0.33).save(path)
            elif filt == 'AKA':
                image = image.convert('L').quantize(3).convert('RGB').filter(
                    ImageFilter.SMOOTH_MORE).filter(
                        ImageFilter.SMOOTH_MORE).filter(
                            ImageFilter.SMOOTH_MORE).quantize(3).convert('RGB')
                data = image.getdata()
                color_a, color_b, _ = tuple(set(data))
                d = {str(color_a): (239, 186, 209), str(color_b): (16, 165, 0)}
                image = Image.new('RGB', image.size)
                image.putdata([d.get(str(t), (255, 255, 255)) for t in data])
                image.save(path)

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


class Delete_Video(View):
    def post(self, request, img_id):
        form = forms.FilterForm(request.POST)
        path = 'app/static/' + models.Video.objects.get(id=img_id).image_url()
        models.Video.objects.get(id=img_id).delete()
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
        document = models.Video.objects.get(id=document_id)
        form = forms.CommentForm(document, request.POST)
        if form.is_valid():
            form.save()
            return redirect('app:feed')
        else:
            return redirect('app:feed')


class Like_Pic(View):
    def post(self, request, img_id):
        d = models.Document.objects.get(id=img_id)
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
    def post(self, request, img_id):
        d = models.Document.objects.get(id=img_id)
        d.dislikes += 1
        d.save()
        return redirect('app:feed')


class DisLike_Vid(View):
    def post(self, request, doc_id):
        d = models.Video.objects.get(id=doc_id)
        d.dislikes += 1
        d.save()
        return redirect('app:feed')