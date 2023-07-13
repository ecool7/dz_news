from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        self.rating = (
            self.post_set.aggregate(models.Sum('rating')).get('rating__sum') or 0
        ) * 3
        self.rating += self.comment_set.aggregate(models.Sum('rating')).get('rating__sum') or 0
        self.rating += (
            self.post_set.aggregate(
                models.Sum('comment__rating')
            ).get('comment__rating__sum') or 0
        )
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    NEWS = 'NW'
    ARTICLE = 'AR'
    TYPE_CHOICES = [
        (NEWS, 'News'),
        (ARTICLE, 'Article'),
    ]
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    post_type = models.CharField(max_length=2, choices=TYPE_CHOICES)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f"{self.text[:124]}..."

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)



    def __str__(self):
        return self.text

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

