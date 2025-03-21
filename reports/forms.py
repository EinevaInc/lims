from django import forms

class PropertyListingReportForm(forms.Form):
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    landuse_type = forms.ChoiceField(choices=[], required=False)
    sales_status = forms.ChoiceField(choices=[], required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically populate choices from the database
        from survey_realestate.models import LandUse, PropertyStatus
        self.fields['landuse_type'].choices = [(lu.id, lu.landuse_description) for lu in LandUse.objects.all()]
        self.fields['sales_status'].choices = [(ps.id, ps.status_name) for ps in PropertyStatus.objects.all()]
