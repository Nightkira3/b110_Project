from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q, F


class CustomUser(AbstractUser):
    birth_date = models.DateField('дата рождения', blank=True, null=True)
    about = models.TextField(max_length=1000, blank=True)
    avatar = models.ImageField(upload_to='users')
    phone_number = models.CharField(max_length=11, blank=True)
    my_friends = models.ManyToManyField('self', through='Friendship', blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"User {self.username}"


class Friendship(models.Model):
    source = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='friends'
    )

    target = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='target_friends'
    )
    is_accepted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Друг'
        verbose_name_plural = 'Друзья'
        constraints = [
            models.UniqueConstraint(
                fields=['source', 'target'],
                name='unique_source_target'
            ),
            models.CheckConstraint(
                check=~Q(source=F('target')),
                name='source_not_target'
            )
        ]

