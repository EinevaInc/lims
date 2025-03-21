from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Property, Address
from .forms import PropertyForm, AddressForm
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction

# --- Property Views ---
class PropertyListView(LoginRequiredMixin, ListView):
    model = Property
    template_name = 'survey_realestate/property_list.html'
    context_object_name = 'properties'
    paginate_by = 10  # Add pagination

class PropertyDetailView(LoginRequiredMixin, DetailView):
    model = Property
    template_name = 'survey_realestate/property_detail.html'
    context_object_name = 'property'

class PropertyCreateView(LoginRequiredMixin, CreateView):
    model = Property
    form_class = PropertyForm
    template_name = 'survey_realestate/property_form.html'
    success_url = reverse_lazy('survey_realestate:property_list')

    def form_valid(self, form):
        # Set the created_by user before saving
        form.instance.created_by = self.request.user
        messages.success(self.request, "Property created successfully.")  # Add success message
        return super().form_valid(form)

class PropertyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Property
    form_class = PropertyForm
    template_name = 'survey_realestate/property_form.html'

    def get_success_url(self):
          return reverse_lazy('survey_realestate:property_detail', kwargs={'pk': self.object.pk})


    def test_func(self):  # Permission check
        property = self.get_object()
        return self.request.user.is_superuser or self.request.user == property.created_by or self.request.user.groups.filter(name='Survey-RealEstate').exists() # Check if user is a superuser or created.
    def form_valid(self, form):
        messages.success(self.request, "Property updated successfully.")
        return super().form_valid(form)

class PropertyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Property
    template_name = 'survey_realestate/property_confirm_delete.html'
    success_url = reverse_lazy('survey_realestate:property_list')

    def test_func(self):
        property = self.get_object()
        return self.request.user.is_superuser or self.request.user.groups.filter(name='Survey-RealEstate').exists()

    def form_valid(self, form):
        messages.success(self.request, "Property deleted successfully.")
        return super().form_valid(form)


#-- Address Views --
class AddressCreateView(LoginRequiredMixin, CreateView):
    model = Address
    form_class = AddressForm
    template_name = 'survey_realestate/address_form.html'
    success_url = reverse_lazy('survey_realestate:property_list') # Redirect, to property list after.

    def form_valid(self, form):
        messages.success(self.request, 'Address created successfully!')
        return super().form_valid(form)


#--- Create Property and address ---
@login_required
@transaction.atomic
def create_property_with_address(request):
    if request.method == 'POST':
        property_form = PropertyForm(request.POST)
        address_form = AddressForm(request.POST)
        if property_form.is_valid() and address_form.is_valid():
            address = address_form.save()
            property = property_form.save(commit=False)
            property.address = address
            property.created_by = request.user
            property.save()
            messages.success(request, 'Property and Address created successfully!')
            return redirect('survey_realestate:property_list')  # Use URL name
    else:
        property_form = PropertyForm()
        address_form = AddressForm()
    return render(request, 'survey_realestate/create_property_with_address.html', {'property_form': property_form, 'address_form': address_form})