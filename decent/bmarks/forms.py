from django import forms
from bmarks.models import Bookmark

class BookmarkForm(forms.Form):
    url = forms.URLField(label="URL")
    tags = forms.CharField(required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
