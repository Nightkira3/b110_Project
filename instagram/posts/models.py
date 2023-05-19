from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now


User = get_user_model()


class HashTag(models.Model):
    name = models.CharField('Название', max_length=20, unique=True)

    class Meta:
        verbose_name = 'Хештег'
        verbose_name_plural = 'Хештеги'
        ordering = ('name', )

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    hashtags = models.ManyToManyField(HashTag, related_name='posts', blank=True)
    name = models.CharField(
        'заголовок',
        max_length=80,
        blank=True
    )
    image = models.ImageField('картинка', upload_to='posts')
    description = models.TextField(
        'описание',
        max_length=1000,
        blank=True
    )
    pub_date = models.DateTimeField('дата публикации', auto_now_add=True)
    edit_date = models.DateTimeField('дата редактирования', auto_now=True)
    timezone = models.CharField('часовой пояс', default='Europe/Samara', max_length=50)
    location = models.CharField('место съёмки', default='Тольятти', max_length=50)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-pub_date',)

    def __str__(self):
        return f"Пост {self.pk} от {self.author}"

    @property
    def count_of_likes(self):
        return self.likes.count()


class Comment(models.Model):
    text = models.TextField('текст комментария', max_length=250)
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    pub_date = models.DateTimeField('дата публикации', default=now)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date', 'text')

    def __str__(self):
        return f"Комментарий {self.pk} от {self.author}"
