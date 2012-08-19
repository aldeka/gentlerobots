from django import forms
from bmarks.models import Bookmark

class BookmarkForm(forms.Form):
    tags = forms.CharField(required=False)
    url = forms.URLField(label="URL")
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
