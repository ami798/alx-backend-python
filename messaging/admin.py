from django.contrib import admin
from .models import Message, Notification  # and MessageHistory if separate

admin.site.register(Message)
admin.site.register(Notification)
# If MessageHistory is separate model:
# from .models import MessageHistory
# admin.site.register(MessageHistory)
