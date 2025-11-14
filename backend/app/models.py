from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Mention(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    source = models.CharField(max_length=100)
    author = models.CharField(max_length=200, blank=True, null=True)
    text = models.TextField()
    url = models.URLField(blank=True, null=True)
    published_at = models.DateTimeField()
    sentiment = models.CharField(max_length=10)
    sentiment_score = models.FloatField(null=True)
    cluster_id = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Alert(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    message = models.TextField()
    detected_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
