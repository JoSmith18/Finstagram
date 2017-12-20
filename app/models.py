from django.db import models


class Document(models.Model):
    posted_by = models.CharField(max_length=16)
    caption = models.CharField(max_length=200)
    image = models.ImageField(upload_to='app/static/app/images')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def image_url(self):
        return self.image.url[len('app/static/'):]


class Video(models.Model):
    posted_by = models.CharField(max_length=16)
    caption = models.CharField(max_length=200)
    video = models.FileField(upload_to='app/static/app/images')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def image_url(self):
        return self.video.url[len('app/static/'):]


class Comment(models.Model):
    comment = models.CharField(max_length=120)
    time = models.DateTimeField(auto_now_add=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)