from django.db import models

import users
from config import settings

NULLABLE = {'null': True, 'blank': True}


class Lesson(models.Model):
    name = models.CharField(max_length=50, verbose_name='навзвание')
    description = models.TextField(verbose_name='описание')
    pre_view = models.ImageField(upload_to='lesson/', verbose_name='превью', **NULLABLE)
    video_url = models.URLField(verbose_name='ссылка на видео', **NULLABLE)
    course = models.ForeignKey('materials.Course', on_delete=models.CASCADE, verbose_name='Курс')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name="Владелец",
                              help_text="укажите владельца")

    def __str__(self):
        return f'{self.name}, {self.description}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    pre_view = models.ImageField(upload_to='course/', verbose_name='превью ', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name="Владелец",
                              help_text="укажите владельца")

    def __str__(self):
        return f'{self.name}, {self.description}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ('name',)


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='пользователь', on_delete=models.CASCADE, **NULLABLE)
    course = models.ForeignKey(Course, verbose_name='курс в подписке', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} - {self.course}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
