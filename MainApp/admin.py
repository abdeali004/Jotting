from django.contrib import admin
from MainApp.models import note, userInfo, verifyUser

# Register your models here.
admin.site.register(note)
admin.site.register(userInfo)
admin.site.register(verifyUser)
