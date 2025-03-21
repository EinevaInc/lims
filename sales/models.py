from django.db import models
from survey_realestate.models import Property
from accounts.models import User

class OfferLetter(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='offer_letters')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offer_letters')
    offer_date = models.DateField()
    offer_amount = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Expired', 'Expired')
    ])
    offer_letter_document = models.FileField(upload_to='offer_letters/')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_offer_letters')

    def __str__(self):
        return f"Offer for {self.property} by {self.client} on {self.offer_date}"
