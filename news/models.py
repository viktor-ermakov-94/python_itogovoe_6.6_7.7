from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

# длина начала текста поста для предпросмотра
PREVIEW_LEN = 124


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_name = models.CharField(max_length=128)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'id={self.id}, user={self.user}, author_name="{self.author_name}", rating={self.rating}'

    def update_rating(self):
        """
        суммарный рейтинг каждой статьи автора умножается на 3;
        суммарный рейтинг всех комментариев автора;
        суммарный рейтинг всех комментариев к статьям автора.
        """
        # 1. суммарный рейтинг каждой статьи автора умножается на 3
        self.rating = Post.objects.filter(author=self.id).aggregate(rating=Sum('rating'))['rating'] * 3

        # 2. суммарный рейтинг всех комментариев автора
        cr = Comment.objects.filter(user=self.user).aggregate(comments_rating=Sum('rating'))
        if not cr['comments_rating'] is None:
            self.rating += cr['comments_rating']

        # 3. суммарный рейтинг всех комментариев к статьям автора
        for i in Post.objects.filter(author=self.id, post_type='0'):
            _ = Comment.objects.filter(post=i).aggregate(post_rating=Sum('rating'))['post_rating']
            if _ is not None:
                self.rating += _

        self.save()
        return self.rating


class Category(models.Model):
    name = models.CharField(max_length=500)


POST_TYPE = [('0', 'статья'), ('1', 'новость')]


class Post(models.Model):
    post_type = models.CharField(max_length=1, choices=POST_TYPE, default='0')
    input_date_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_header = models.CharField(max_length=124)
    post_body = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1

    def dislike(self):
        self.rating -= 1

    def preview(self):
        """
        возвращает начало статьи (предварительный просмотр) длиной 124 символа и добавляет многоточие в конце
        """
        if len(self.post_body) > PREVIEW_LEN:
            return self.post_body[:PREVIEW_LEN + 1] + '...'
        else:
            return self.post_body

    def __str__(self):
        return f'id={self.id}, input_date_time={self.input_date_time.strftime("%d.%m.%Y %H:%M:%S")}, rating={self.rating}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=1000, default='')
    input_date_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1

    def dislike(self):
        self.rating -= 1

    def __str__(self):
        return f'id={self.id}, rating={self.rating}'
