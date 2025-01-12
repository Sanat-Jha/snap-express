from django.contrib import admin
from .models import *

class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'current']

    # Override delete_selected action
    def delete_queryset(self, request, queryset):
        # Call delete() for each object in the queryset
        for obj in queryset:
            obj.delete()
# Register your models here.
admin.site.register(Template)
admin.site.register(TemplateCategory)
admin.site.register(Event, EventAdmin)
admin.site.register(EventImage)

admin.site.site_title = "SnapExpress Admin"
admin.site.site_header = "SnapExpress Admin"
admin.site.index_title = "SnapExpress Admin"