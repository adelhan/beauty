from django.contrib import admin

from .models import Category, Place, Master, MasterImage

class ImageInline(admin.TabularInline):
    model = MasterImage
    extra = 1
    fields = ('image', )

class MasterAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


admin.site.register(Category)
admin.site.register(Place)
admin.site.register(Master, MasterAdmin)