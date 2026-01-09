from django import forms
from django.contrib.auth.models import User


class ReviewForm(forms.Form):
    rating = forms.IntegerField(min_value=1, max_value=5, label='Rating')
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False, label='Comment')


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm password')

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'you@example.com'}),
            'username': forms.TextInput(attrs={'placeholder': 'username'}),
        }

    def clean_password2(self):
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Passwords do not match')
        return p2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('A user with that email already exists')
        return email
