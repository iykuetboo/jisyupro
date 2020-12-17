from django.db import models

# Create your models here.

class Member(models.Model):
    name = models.CharField(max_length=64)
    def __str__(self):
        if not self.name:
            return "unknown member"
        return self.name

class FaceImage(models.Model):
    image = models.ImageField(upload_to='images/',blank=True, null=True)
    name = models.CharField(max_length=256,blank=True, null=True)
    person = models.ForeignKey(Member,blank=True, null=True,on_delete=models.CASCADE)
    def __str__(self):
        if not self.name:
            return "unknown image"
        return self.name
