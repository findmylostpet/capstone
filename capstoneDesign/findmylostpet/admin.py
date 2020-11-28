from django.contrib import admin
from .models import Dog,LostNotice,FindNotice,Member,Photo
# Register your models here.

admin.site.register(LostNotice)
admin.site.register(FindNotice)
admin.site.register(Dog)
admin.site.register(Photo)
admin.site.register(Member)
