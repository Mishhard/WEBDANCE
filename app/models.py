"""
Definition of models.
"""
# Create your models here.
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.db import models
from datetime import datetime
from django.contrib import admin
from django.urls import reverse
from django.contrib.auth.models import User


class Blog(models.Model):
    title = models.CharField(max_length = 100, unique_for_date = "posted", verbose_name = "Заголовок")
    description = models.TextField(verbose_name = "Краткое содержание")
    content = models.TextField(verbose_name = "Полное содержание")
    posted  = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Опубликована")
    author = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Автор")
    image = models.FileField(default = 'temp.jpg', verbose_name = "Путь к изображению")


    def get_absolute_url(self):
        return reverse("blogpost", args=[str(self.id)])

    def _str_(self):
        return self.title

    class Meta:
        db_table = "Posts"
        ordering = ["-posted"]
        verbose_name = "статья блога"
        verbose_name_plural = "статьи блога"

class Comment(models.Model):
    text = models.TextField(verbose_name = "Комментарий")
    date = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Дата")
    author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Автор")
    post = models.ForeignKey(Blog, on_delete = models.CASCADE, verbose_name = "Статья")

    def _str_(self):
        return 'Комментарий %s к  %s' % (self.author, self.post)

    class Meta:
        db_table = "Comments"
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии к статьям блога"
        ordering = ["-date"]


admin.site.register(Blog)
admin.site.register(Comment)

class Catalog(models.Model): 
     title = models.CharField(max_length = 60, unique_for_date = "posted", verbose_name = "Наименование") 
     description = models.TextField(max_length = 240, verbose_name = "Описание")
     quantity = models.IntegerField(verbose_name = "Количество")
     price = models.IntegerField(default = 0, verbose_name = "Цена")
     posted = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Опубликована") 
     image = models.FileField(default = 'temp.jpg', verbose_name ="Путь к изображению")
     author = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Автор")
     stonks = models.IntegerField(default=0, verbose_name = "Выручка")
 
     def get_absolute_url(self): 
        return reverse("Catalog", args=[str(self.id)]) 
 
     def _str_(self): 
        return self.title 
 
     class Meta: 
         db_table = "catalog" 
         ordering = ["-posted"] 
         verbose_name = "Товар" 
         verbose_name_plural = "Товары" 

class Orders(models.Model): 
     date = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Дата") 
     author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Покупатель") 
     post = models.ForeignKey(Catalog, on_delete = models.CASCADE, verbose_name = "Покупка") 
     ready = models.BooleanField(default=False, verbose_name = "Оплачен") 
     on_processing = models.BooleanField(default=False, verbose_name = "В обработке") 
     qnt = models.IntegerField(default=1, verbose_name = "Количество")


     def _str_(self): 
        return 'Покупка %s от %s' % (self.author, self.post) 
 
     class Meta: 
         db_table = "Orders" 
         ordering = ["-date"] 
         verbose_name = "Покупка" 
         verbose_name_plural = "Покупки"

class Requisites(models.Model): 
     provider = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Поставщик") 
     bank = models.TextField(verbose_name = "Банк")
     bik = models.TextField(verbose_name = "БИК")
     kpp = models.TextField(verbose_name = "КПП")
     account = models.TextField(verbose_name = "Счет") 

 
     class Meta: 
         db_table = "requisites" 
         ordering = ["-id"] 
         verbose_name = "Реквизиты" 
         verbose_name_plural = "Реквизиты" 

admin.site.register(Catalog) 
admin.site.register(Orders)
admin.site.register(Requisites)

