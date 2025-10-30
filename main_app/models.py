from django.db import models

class Session(models.Model):
    title = models.CharField(max_length=100)
    duration = models.IntegerField()
    image = models.TextField(blank=True, null=True) 
    sound = models.CharField(max_length=255, null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True) 


    def __str__(self):
        return self.title




class Space(models.Model):
    session = models.ForeignKey('Session', on_delete=models.CASCADE, related_name='spaces')

    type = models.CharField(max_length=20, choices=[
        ('star', 'Star'),
        ('planet', 'Planet'),
    ])

    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)

    image = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} from session {self.session.title}"