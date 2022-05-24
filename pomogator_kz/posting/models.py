from django.core.validators import MinValueValidator
from django.db import models


# Основные модели
class Client(models.Model):
    user_id = models.IntegerField(verbose_name='id пользователя', unique=True)
    status_bot = models.BooleanField(verbose_name='Статус бота', default=False)
    created_user = models.DateTimeField(verbose_name='Дата регистрации', auto_now_add=True)
    list_url = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.user_id)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_user']


class MessageLog(models.Model):
    mess_log_user_id = models.CharField(verbose_name='id пользователя', max_length=20)
    created_mess = models.DateTimeField(verbose_name='Дата сообщения')
    log_text = models.TextField(verbose_name='Текст сообщения')

    def __str__(self):
        return str(self.mess_log_user_id)

    class Meta:
        verbose_name = 'Лог сообщения'
        verbose_name_plural = 'Логи сообщений'
        ordering = ['-created_mess']


class SubscribeLog(models.Model):
    sub_log_user_id = models.ForeignKey('Client', to_field='user_id', verbose_name='id пользователя',
                                        on_delete=models.PROTECT)
    created_sub = models.DateTimeField(verbose_name='Дата подписки', auto_now_add=True)
    sub_log_type_sub = models.ForeignKey('Subscribe', verbose_name='Тип подписки', on_delete=models.PROTECT)

    def __str__(self):
        return str(self.sub_log_user_id)

    class Meta:
        verbose_name = 'Лог подписки'
        verbose_name_plural = 'Логи подписок'
        ordering = ['-created_sub']


class Subscribe(models.Model):

    type_subscribes = [
        ('kolesa_auto', 'kolesa_auto'),
        ('kolesa_zap', 'kolesa_zap'),

        ('krisha', 'krisha'),
    ]

    name_sub = models.CharField(verbose_name='Название подписки', max_length=50)
    type_sub = models.CharField(verbose_name='Тип подписки', max_length=50, choices=type_subscribes)
    limit_filters = models.IntegerField(verbose_name='Лимит фильтров', blank=True, null=True)
    days_sub = models.IntegerField(verbose_name='Количество дней подписки')
    price_sub = models.IntegerField(verbose_name='Цена подписки', validators=[MinValueValidator(limit_value=0)])

    def __str__(self):
        return self.name_sub

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['type_sub']


# Модели для хранения значений фильтров
class RegionFilters(models.Model):
    name_region = models.CharField(verbose_name='Название региона', max_length=100, primary_key=True)
    alias_region = models.CharField(verbose_name='Ссылка региона', max_length=100)

    def __str__(self):
        return self.name_region

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'
        ordering = ['name_region']


class CityFilters(models.Model):
    name_city = models.CharField(verbose_name='Название города', max_length=100)
    alias_city = models.CharField(verbose_name='Ссылка города', max_length=100)
    parent_city = models.ForeignKey('RegionFilters', to_field='name_region', verbose_name='Регион', on_delete=models.PROTECT)

    def __str__(self):
        return self.name_city

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['name_city']


class BrandFilters(models.Model):
    name_brand = models.CharField(verbose_name='Название брэнда', max_length=100, primary_key=True)
    alias_brand = models.CharField(verbose_name='Ссылка брэнда', max_length=100)

    def __str__(self):
        return self.name_brand

    class Meta:
        verbose_name = 'Брэнд'
        verbose_name_plural = 'Брэнды'
        ordering = ['name_brand']


class ModelFilters(models.Model):
    name_model = models.CharField(verbose_name='Название модели', max_length=100)
    alias_model = models.CharField(verbose_name='Ссылка модели', max_length=100)
    parent_model = models.ForeignKey('BrandFilters', to_field='name_brand', verbose_name='Брэнд', on_delete=models.PROTECT)

    def __str__(self):
        return self.name_model

    class Meta:
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели'
        ordering = ['name_model']


class OtherDataFilters(models.Model):
    name_data = models.CharField(verbose_name='Название фильтра', max_length=100)
    alias_data = models.CharField(verbose_name='Ссылка фильтра', max_length=100)
    component_data = models.CharField(verbose_name='Компонент фильтра', max_length=100)
    options_data = models.TextField(verbose_name='Опции фильтра')

    def __str__(self):
        return self.name_data

    class Meta:
        verbose_name = 'Другой фильтр'
        verbose_name_plural = 'Другие фильтры'
        ordering = ['name_data']
