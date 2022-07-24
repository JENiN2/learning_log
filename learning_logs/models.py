from django.db import models

class Topic(models.Model):
    """Тема, которую изучает пользователь"""
    lable = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        '''Возвращает строковое представление модели'''
        return self.lable
