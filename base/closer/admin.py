from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Closer

admin.site.register(Closer, UserAdmin)
