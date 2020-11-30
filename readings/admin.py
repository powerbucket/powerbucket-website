from django.contrib import admin

# Register your models here.
from .models import Reading

#admin.site.register(Reading)

class ReadingAdmin(admin.ModelAdmin):
    list_display = ('firstNum', 'secondNum', 'pic')
    def pic(self,obj):
        if obj.picture:
            return obj.picture.url
        else:
            return "X"
    pic.short_description = 'Pic Exists?'

admin.site.register(Reading,ReadingAdmin)
