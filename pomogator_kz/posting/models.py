from django.core.validators import MinValueValidator
from django.db import models


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