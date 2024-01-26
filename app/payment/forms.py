
from django import forms

from . models import ShippingAddress

class ShippingForm(forms.ModelForm):

    terms_and_conditions = forms.BooleanField(
        label='I agree to the terms and conditions',
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:

        model = ShippingAddress

        fields = ['office']
        exclude = ['user',]

    def clean_terms_and_conditions(self):
        value = self.cleaned_data['terms_and_conditions']
        if not value:
            raise forms.ValidationError('You must agree to the terms and conditions.')
        return value





