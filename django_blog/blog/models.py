from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
from django.dispatch import receiver
from django.db.models.signals import post_save


User = get_user_model()

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})
    
    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['post', '-created_at']),]

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', null=True, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
    
@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()