from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'price', 'status', 'date')
    list_filter = ('status', 'date')
    search_fields = ('title', 'seller__username', 'location')
    action= ['approve_properties']

    def approve_properties(self, request, queryset):
        updated =queryset.update(status='Approved')
        self.message_user(request, f'{updated} properties approved successfully.')
admin.site.register(Payment)
admin.site.register(CustomUser)

