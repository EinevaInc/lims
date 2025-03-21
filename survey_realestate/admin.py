from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Property, LandUse, PropertyStatus, Address, SurveyRecord

@admin.register(Property)
class PropertyAdmin(OSMGeoAdmin):  # Use OSMGeoAdmin for map display in admin
    list_display = ('stand_number', 'landuse_type', 'sales_status', 'size_area_sqm', 'date_created')
    list_filter = ('landuse_type', 'sales_status', 'date_created')
    search_fields = ('stand_number', 'address__address_line1', 'address__city')  # Search across related fields
    readonly_fields = ('date_created', 'last_updated')
    #default_lon = 28.274792  # Set a default longitude for the map
    #default_lat = -16.520169  # Set a default latitude
    #default_zoom = 6  # Set a default zoom level

@admin.register(LandUse)
class LandUseAdmin(admin.ModelAdmin):
    list_display = ('landuse_code', 'landuse_description')
    search_fields = ('landuse_code', 'landuse_description')

@admin.register(PropertyStatus)
class PropertyStatusAdmin(admin.ModelAdmin):
    list_display = ('status_name',)

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('address_line1', 'city', 'state', 'postal_code')
    search_fields = ('address_line1', 'city', 'state', 'postal_code')

@admin.register(SurveyRecord)
class SurveyRecordAdmin(admin.ModelAdmin):
    list_display = ('property', 'surveyor', 'survey_date')
    list_filter = ('survey_date',)
    search_fields = ('property__stand_number', 'surveyor__username')