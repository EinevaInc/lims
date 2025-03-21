from django import forms
from django.contrib.gis.geos import Point
from .models import Property, Address, SurveyRecord
from django.contrib.gis.forms import PointField, MultiPolygonField, GeometryField, OSMWidget

class PropertyForm(forms.ModelForm):
    """
    Form for creating and updating Property records.
    """
    class Meta:
        model = Property
        fields = '__all__'  # Include all fields; you can also specify a list
        widgets = {
            'geom': OSMWidget(),  # Use OSMWidget for map input
        }
    def clean(self):
        """
        Custom form validation.
        """
        cleaned_data = super().clean()
        # Add any custom validation logic here (e.g., checking area size)
        return cleaned_data
    def __init__(self, *args, **kwargs):
      super(PropertyForm, self).__init__(*args, **kwargs)
      # Make the address fields not required at the form level.
      self.fields['address'].required = False

class AddressForm(forms.ModelForm):
   class Meta:
      model = Address
      fields = '__all__'

class SurveyRecordForm(forms.ModelForm):
    """
    Form for creating Survey Records.
    """
    class Meta:
        model = SurveyRecord
        fields = '__all__'
        widgets = {
            'survey_date': forms.DateInput(attrs={'type': 'date'}),  # Use date picker
        }