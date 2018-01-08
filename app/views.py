from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from . import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from os import listdir, remove
from os.path import isfile, join
from PIL import ImageFilter, Image
from django.views import View
from app import models
from resizeimage import resizeimage
from random import randint
from app import filters


def count_comment(obj):
    return obj.comment_set.count()


class SignUp(View):
    def post(self, request):
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect(request.GET.get('next', 'app:feed'))
        else:
            form = forms.SignUpForm()
            return render(request, 'app/signup.html', {'form': form})

    def get(self, request):
        form = forms.SignUpForm()
        return render(request, 'app/signup.html', {'form': form})


class Login(View):
    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            username = form.cleaned_data.get('username')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(request.GET.get('next', 'app:feed'))
        else:
            form = forms.LoginForm()
            return render(request, 'app/login.html', {'form': form})

    def get(self, request):
        form = forms.LoginForm()
        return render(request, 'app/login.html', {'form': form})


class Feed(View):
    def get(self, request):
        user = request.user
        docs = models.Document.objects.all().order_by('-uploaded_at')
        videos = models.Video.objects.all().order_by('-uploaded_at')
        comment_form = forms.CommentForm()
        total = docs.count() + videos.count()
        return render(request, 'app/base.html', {
            'docs': docs,
            'total': total,
            'videos': videos,
            'comment_form': comment_form,
            'like_next': reverse('app:feed'),
            'topic': 'Recent',
            'user': user
        })


class Upload(View):
    def post(self, request):
        user = request.user
        form = forms.DocumentForm(user.profile, request.POST, request.FILES)
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
        user = request.user
        form = forms.VideoForm(user.profile, request.POST, request.FILES)
        if form.is_valid():
            form.save()
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
            return redirect(request.GET.get('next', 'app:feed'))
        else:
            return redirect(request.GET.get('next', 'app:feed'))


class Rotate(View):
    def post(self, request, doc_id):
        form = forms.FilterForm(request.POST)
        path = 'app/static/' + models.Document.objects.get(
            id=doc_id).image_url()
        image = Image.open(path)
        image.rotate(-90).save(path)
        return redirect(request.GET.get('next', 'app:feed'))


class Delete_Picture(View):
    def post(self, request, doc_id):
        form = forms.FilterForm(request.POST)
        path = 'app/static/' + models.Document.objects.get(
            id=doc_id).image_url()
        models.Document.objects.get(id=doc_id).delete()
        remove(path)
        return redirect(request.GET.get('next', 'app:feed'))


class Delete_Video(View):
    def post(self, request, doc_id):
        form = forms.FilterForm(request.POST)
        path = 'app/static/' + models.Video.objects.get(id=doc_id).image_url()
        models.Video.objects.get(id=doc_id).delete()
        remove(path)
        return redirect(request.GET.get('next', 'app:feed'))


class Add_Comment(View):
    def post(self, request, document_id):
        user = request.user
        document = models.Document.objects.get(id=document_id)
        form = forms.CommentForm(document, request.POST)
        if form.is_valid():
            form.save()
            return redirect(request.GET.get('next', 'app:feed'))
        else:
            return redirect(request.GET.get('next', 'app:feed'))


class Add_Comment_Video(View):
    def post(self, request, document_id):
        video = models.Video.objects.get(id=document_id)
        form = forms.CommentOnVideoForm(video, request.POST)
        if form.is_valid():
            form.save()
            return redirect(request.GET.get('next', 'app:feed'))
        else:
            return redirect(request.GET.get('next', 'app:feed'))


class Like_Pic(View):
    def post(self, request, doc_id):
        d = models.Document.objects.get(id=doc_id)
        d.likes += 1
        d.save()
        return redirect(request.GET.get('next', 'app:feed'))


class Like_Vid(View):
    def post(self, request, doc_id):
        d = models.Video.objects.get(id=doc_id)
        d.likes += 1
        d.save()
        return redirect(request.GET.get('next', 'app:feed'))


class DisLike_Pic(View):
    def post(self, request, doc_id):
        d = models.Document.objects.get(id=doc_id)
        d.dislikes += 1
        d.save()
        return redirect(request.GET.get('next', 'app:feed'))


class DisLike_Vid(View):
    def post(self, request, doc_id):
        d = models.Video.objects.get(id=doc_id)
        d.dislikes += 1
        d.save()
        return redirect(request.GET.get('next', 'app:feed'))


class Mostpop(View):
    def get(self, request):
        user = request.user
        docs = models.Document.objects.all().order_by('-likes')
        videos = models.Video.objects.all().order_by('-likes')
        comment_form = forms.CommentForm()
        total = docs.count() + videos.count()
        return render(request, 'app/base.html', {
            'docs': docs,
            'total': total,
            'videos': videos,
            'comment_form': comment_form,
            'like_next': reverse('app:mostpop'),
            'topic': 'Popular',
            'user': user
        })


class ByTopic(View):
    def get(self, request, topic):
        user = request.user
        docs = models.Document.objects.filter(topic=str(topic))
        videos = models.Video.objects.filter(topic=topic)
        comment_form = forms.CommentForm()
        total = docs.count() + videos.count()
        return render(request, 'app/base.html', {
            'docs': docs,
            'total': total,
            'videos': videos,
            'comment_form': comment_form,
            'like_next': reverse('app:mostpop'),
            'topic': str(topic),
            'user': user
        })


class ByComments(View):
    def get(self, request):
        user = request.user
        document = sorted(
            models.Document.objects.all(),
            key=lambda d: d.comment_set.count())[::-1]
        videos = models.Video.objects.all().order_by('-likes')
        comment_form = forms.CommentForm()
        total = len(document) + videos.count()
        return render(request, 'app/base.html', {
            'docs': document,
            'total': total,
            'videos': videos,
            'comment_form': comment_form,
            'like_next': reverse('app:mostpop'),
            'topic': 'Comment',
            'user': user
        })


class GetUserPost(View):
    def get(self, request):
        user = request.user
        user1 = request.GET.get('user')

        try:
            docs = models.Profile.objects.get(
                user__username=user1).document_set.all().order_by(
                    '-uploaded_at')
            videos = models.Profile.objects.get(
                user__username=str(user1)).video_set.all()
            comment_form = forms.CommentForm()
            total = docs.count() + videos.count()
            return render(request, 'app/base.html', {
                'docs': docs,
                'total': total,
                'videos': videos,
                'comment_form': comment_form,
                'like_next': reverse('app:mostpop'),
                'user': user
            })
        except:
            return redirect(request.GET.get('next', 'app:feed'))
