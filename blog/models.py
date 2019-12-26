from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Blog(models.Model):
    title = models.CharField("Название темы", max_length=100)
    text = models.TextField("Описание")
    create_date = models.DateTimeField("Создана", auto_now_add=True)
    rel_url = models.CharField("Ссылка", max_length=10)
    image = models.ImageField(upload_to="blog", default="blog/default-img.jpg")

    class Meta:
        verbose_name = u"Тема"
        verbose_name_plural = u"Темы"
        ordering = ('title', )
    
    def __str__(self):
        return self.title
    
    def get_top3_posts(self):
        posts_all = self.posts.all()
        return posts_all[:min(3, len(posts_all))]


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name=u"Название поста")
    text = models.TextField(verbose_name=u"Текст поста")
    blog = models.ForeignKey(Blog, related_name='posts', verbose_name=u"Раздел",
            on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name=u"Дата публикации")
    update_date = models.DateTimeField(auto_now=True, verbose_name=u"Дата последнего редактирования")
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u"Пост"
        verbose_name_plural = u"Посты"


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(verbose_name=u"Текст комментария")
    post = models.ForeignKey(Post, related_name="comment", verbose_name=u"Пост", on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name=u"Создан")
    update_date = models.DateTimeField(auto_now=True, verbose_name=u"Отредактирован")
    reply_to = models.ForeignKey("Comment", related_name="reply_comment", verbose_name=u"Коммент",
            blank=True, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = u"Комментарий"
        verbose_name_plural = u"Комментарии"
