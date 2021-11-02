from django import forms

from misc.models import UnpleasantCustomer


class UnpleasantCustomerForm(forms.ModelForm):
    class Meta:
        model = UnpleasantCustomer
        fields = ('email', 'reason')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
