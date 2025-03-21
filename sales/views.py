from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import LandInfoUpdateForm, OfferLetterForm
from survey_realestate.models import Property
from .models import OfferLetter
from django.urls import reverse_lazy
from django.contrib import messages

class UpdateLandInfoView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Property
    form_class = LandInfoUpdateForm
    template_name = 'sales/update_land_info.html'
    permission_required = 'sales.change_property'

    def get_success_url(self):
        return reverse_lazy('survey_realestate:property_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, "Property information updated successfully.")
        return super().form_valid(form)

class GenerateOfferLetterView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = OfferLetter
    form_class = OfferLetterForm
    template_name = 'sales/generate_offer_letter.html'
    permission_required = 'sales.add_offerletter'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "Offer letter created successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('survey_realestate:property_detail', kwargs={'pk': self.object.property.pk})
