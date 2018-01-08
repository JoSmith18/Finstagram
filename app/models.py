from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

options = [
    ('', ''),
    ('Sports', 'Sports'),
    ('Politics', 'Politics'),
    ('Programming', 'Programming'),
    ('Weather', 'Weather'),
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Document(models.Model):
    posted_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    caption = models.CharField(max_length=200)
    image = models.ImageField(upload_to='app/static/app/images')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    topic = models.CharField(max_length=16, choices=options, blank=True)

    def image_url(self):
        return self.image.url[len('app/static/'):]


class Video(models.Model):
    posted_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    caption = models.CharField(max_length=200)
    video = models.FileField(upload_to='app/static/app/images')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    topic = models.CharField(max_length=16, choices=options, blank=True)

    def image_url(self):
        return self.video.url[len('app/static/'):]


class Comment(models.Model):
    comment = models.CharField(max_length=120)
    time = models.DateTimeField(auto_now_add=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)


class CommentVid(models.Model):
    comment = models.CharField(max_length=120)
    time = models.DateTimeField(auto_now_add=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)