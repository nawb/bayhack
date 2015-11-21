from django import forms

class ContactForm(forms.Form):
	full_name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control contact frm-name', 'placeholder': 'Name'}))
	email = forms.CharField(widget=forms.EmailInput(attrs={'class' : 'form-control contact frm-email', 'placeholder': 'Email'}))
	subject = forms.CharField(required=False, widget=forms.TextInput(attrs={'class' : 'form-control contact frm-subject', 'placeholder': 'Subject (optional)'}))
	message = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control contact frm-msg', 'placeholder': 'Message'}))