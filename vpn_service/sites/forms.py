from django import forms
from sites.models import UserSite

class UserSiteForm(forms.ModelForm):
    class Meta:
        model = UserSite
        fields = ['name', 'url']
