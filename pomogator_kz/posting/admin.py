from django.contrib import admin
from .models import Client, Subscribe, SubscribeLog, MessageLog


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'status_bot', 'created_user')
    list_display_links = ('id', 'user_id')
    search_fields = ('user_id', )
    list_editable = ('status_bot',)
    list_filter = ('created_user', 'status_bot')


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_sub', 'type_sub', 'limit_filters', 'price_sub', 'days_sub')
    list_display_links = ('id', 'name_sub')
    search_fields = ('name_sub', 'type_sub')
    list_filter = ('type_sub',)


@admin.register(SubscribeLog)
class SubscribeLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'sub_log_user_id', 'created_sub', 'sub_log_type_sub')
    list_display_links = ('id', 'sub_log_user_id')
    search_fields = ('sub_log_user_id',)
    list_filter = ('created_sub', 'sub_log_type_sub')


@admin.register(MessageLog)
class MessageLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'mess_log_user_id', 'created_mess', 'log_text')
    list_display_links = ('id', 'mess_log_user_id')
    search_fields = ('mess_log_user_id', 'log_text')
    list_filter = ('created_mess', )
