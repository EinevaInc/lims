from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import PropertyListingReportForm
from survey_realestate.models import Property

class PropertyListingReportView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'survey_realestate.view_property'
    template_name = 'reports/property_listing_report.html'

    def get(self, request):
        form = PropertyListingReportForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PropertyListingReportForm(request.POST)
        if form is_valid():
            properties = Property.objects.all()
            if form.cleaned_data['start_date']:
                properties = properties.filter(date_created__gte=form.cleaned_data['start_date'])
            if form.cleaned_data['end_date']:
                properties = properties.filter(date_created__lte=form.cleaned_data['end_date'])
            if form.cleaned_data['landuse_type']:
                properties = properties.filter(landuse_type_id=form.cleaned_data['landuse_type'])
            if form.cleaned_data['sales_status']:
                properties = properties.filter(sales_status_id=form.cleaned_data['sales_status'])
            return render(request, self.template_name, {'form': form, 'properties': properties})
        return render(request, self.template_name, {'form': form})
