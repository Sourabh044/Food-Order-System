from django.contrib import admin

from vendor.models import Vendor

# Register your models here.
class VendorAdmin(admin.ModelAdmin):
    prepopulated_fields = {"vendor_slug": ("vendor_name",)}
    list_display = ('vendor_name','user','is_approved','created_at')
    list_display_links = ('user','vendor_name')
    list_editable = ('is_approved',)

admin.site.register(Vendor,VendorAdmin)