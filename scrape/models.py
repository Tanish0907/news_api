from django.db import models

# Create your models here.
class News(models.Model):
    heading=models.TextField()
    subheading=models.TextField()
    article=models.TextField()
    date=models.DateTimeField(auto_now_add=True)
    def __int__(self):
        return self.id

