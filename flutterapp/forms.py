from django import forms
# from geoposition import Geoposition
# from geoposition.forms import GeopositionField
from django.contrib.admin import widgets
# from geoposition.widgets import GeopositionWidget
# from leaflet.forms.widgets import LeafletWidget
from .models import AddressInfo, Distributor
from location_field.forms.plain import PlainLocationField

class DistributorInfoForm(forms.ModelForm):
    # location = GeopositionField(widget=LeafletWidget())

    # location = PlainLocationField(initial='24.86151853356795,66.99954985873775')

    class Meta:
        model = Distributor
        fields = '__all__'

