from django.db import models

# Create your models here.
class Photo(models.Model):
    #image tag upload_time
    image = models.ImageField(upload_to='photos/')
    upload_time = models.DateTimeField(auto_now_add=True)
    tag = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return f"Photo {self.id} - {self.tag or 'No Tag'}"