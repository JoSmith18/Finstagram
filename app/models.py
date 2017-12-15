from django.db import models


class Document(models.Model):
    image = models.ImageField(upload_to='app/static/app/images')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def image_url(self):
        return self.image.url[len('app/static/'):]
