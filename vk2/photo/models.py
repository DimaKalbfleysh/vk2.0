from django.db import models

# Create your models here.
from account.models import user_directory_path
from account.models import Account
from post.models import Post


class Photo(models.Model):
    id_photo = models.IntegerField(null=True, unique=True)
    photo = models.ImageField(upload_to=user_directory_path, blank=True, null=True, default='defult-photo.png')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='images', null=True)
    post = models.ManyToManyField(Post, related_name='images', blank=True)
    like_put = models.BooleanField(null=True, default=False)

    def get_new_id_photo(self):
        return int(self.objects.all()[0].id_photo) + 1

    class Meta:
        ordering = ['-id']
