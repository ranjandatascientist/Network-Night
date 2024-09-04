from django import forms
from .models import User

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['FullName', 'Username', 'Email', 'password']

    def clean_password(self):
        # Validate password length and complexity
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        # Add other password validation rules if needed
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')  # Updated field name

        # Check if passwords match
        if password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")  # Updated field name

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')

        if password:
            user.set_password(password)
        
        if commit:
            user.save()
        return user

class AuthenticationForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
