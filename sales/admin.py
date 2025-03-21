from django.contrib import admin
from .models import OfferLetter

@admin.register(OfferLetter)
class OfferLetterAdmin(admin.ModelAdmin):
    list_display = ('property', 'client', 'offer_date', 'offer_amount', 'expiry_date', 'status')
    list_filter = ('status', 'offer_date', 'expiry_date')
    search_fields = ('property__stand_number', 'client__email')
