from django.db import models
from django.contrib.gis.db import models as gis_models  # Import GeoDjango models
from accounts.models import User  # Import your custom User model


class LandUse(models.Model):
    """
    Lookup table for land use types (e.g., Residential, Commercial, Agricultural).
    """
    landuse_code = models.CharField(max_length=20, unique=True)
    landuse_description = models.CharField(max_length=255)

    def __str__(self):
        return self.landuse_description

class PropertyStatus(models.Model):
    """
    Lookup table for property statuses (e.g., Available, Sold, Reserved).
    """
    status_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
         return self.status_name
    class Meta:
        verbose_name_plural = "Property statuses"  # Correct plural in admin


class Address(models.Model):
    """
    Separate Address model for better address management and reusability.
    """
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.address_line1}, {self.city}, {self.state} {self.postal_code}"


class Property(models.Model):
    """
    The main Property model, including spatial data.
    """
    stand_number = models.CharField(max_length=50, unique=True)  # Consider if this should be the PK
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='properties_created')
    sales_status = models.ForeignKey(PropertyStatus, on_delete=models.SET_NULL, null=True, blank=True)
    landuse_type = models.ForeignKey(LandUse, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True) #connected to the address
    size_area_sqm = models.DecimalField(max_digits=10, decimal_places=2)
    geom = gis_models.MultiPolygonField(srid=4326)  # Use MultiPolygonField for parcels
    #Additional attributes.
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.stand_number

    class Meta:
      ordering = ['-date_created'] #ordering in the admin interface


class SurveyRecord(models.Model):
    """
    Stores details about surveys conducted on properties.
    """
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='survey_records')
    surveyor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='surveys_conducted')
    survey_date = models.DateField()
    survey_notes = models.TextField(blank=True, null=True)
    # Add other survey-related fields as needed (e.g., accuracy, equipment used)

    def __str__(self):
        return f"Survey of {self.property.stand_number} on {self.survey_date}"