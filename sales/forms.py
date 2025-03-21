from django import forms
from survey_realestate.models import Property
from .models import OfferLetter

class LandInfoUpdateForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['sales_status', 'asking_price', 'description']  # Include only fields that Sales users can modify

class OfferLetterForm(forms.ModelForm):
    class Meta:
        model = OfferLetter
        fields = ['property', 'client', 'offer_amount', 'expiry_date']
