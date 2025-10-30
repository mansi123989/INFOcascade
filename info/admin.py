

# Register your models here.
from django.contrib import admin
from .models import student,notice,chatMessage

admin.site.register(student)
admin.site.register(notice)
@admin.register(chatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'timestamp')
    search_fields = ('user__username', 'message')
    list_filter = ('timestamp',)