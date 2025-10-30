from django.db import models

class Session(models.Model):
    title = models.CharField(max_length=100)
    duration = models.IntegerField()
    image = models.TextField(blank=True, null=True) 
    sound = models.CharField(max_length=255, null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True) 


    def __str__(self):
        return self.title


