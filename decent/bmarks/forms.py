from django import forms

class BookmarkForm(forms.Form):
    url = forms.URLField(label="URL")
    tags = forms.CharField(required=False, label="tags")
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False, label="description")
    
class SubscriptionForm(forms.Form):
    username = forms.CharField(label="username@domain.tld")
