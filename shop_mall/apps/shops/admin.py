from ckeditor.widgets import CKEditorWidget
from django.contrib import admin
from .models import *


class ProAdmin(admin.ModelAdmin):
    """
    产品后台管理
    """
    list_display = ['name', 'price', 'num', 'freight', 'origin', 'pro_type', 'buyers', 'comments', 'add_time']
    list_filter = ['price', 'num', 'origin', 'pro_type', 'buyers', 'comments', 'add_time']
    search_fields = ['name', 'num', 'origin', 'pro_type', 'buyers', 'comments', 'add_time']
    fields = ['name', 'price', 'num', 'freight', 'origin', 'pro_type', 'buyers', 'comments', 'details', 'mainimg', 'add_time']
    model_icon = 'fa fa-shopping-cart'
    readonly_fields = ['buyers', 'comments']
    style_fields = ['details']
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget},
    }


class ProPicAdmin(admin.ModelAdmin):
    list_display = ['product', 'image', 'add_time']
    model_icon = 'fa fa-picture-o'


admin.site.register(Product, ProAdmin)
admin.site.register(ProPic, ProPicAdmin)
