from django.db import models  # импорт
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):  # наследуемся от класса Model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default=0)

    def update_rating(self):
        rating_posts_author = Post.objects.filter(author_id=self.pk).aggregate(rating_news=Sum('rating_news'))['rating_news']
        rating_comments_author = Comment.objects.filter(user_id=self.user).aggregate(rating_news=Sum('rating_news'))['rating_news']
        rating_comments_posts = Comment.objects.filter(post__author__user=self.user).aggregate(rating_news=Sum('rating_news'))['rating_news']
        self.user_rating = rating_posts_author * 3 + rating_comments_author + rating_comments_posts
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


articles = 'AR'
news = 'NS'

POSITIONS = [
    (articles, 'Статьи'),
    (news, 'Новости')
]


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=POSITIONS, default=news)
    time_in = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    article = models.TextField()
    text = models.TextField()
    rating_news = models.IntegerField(default=0)

    def like(self):
        self.rating_news += 1
        self.save()

    def dislike(self):
        self.rating_news -= 1
        self.save()

    def preview(self):
        return f'{self.text[0:124]}...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_create = models.DateTimeField(auto_now_add=True)
    rating_news = models.IntegerField(default=0)

    def like(self):
        self.rating_news += 1
        self.save()
        return self.rating_news

    def dislike(self):
        self.rating_news -= 1
        self.save()
        return self.rating_news
