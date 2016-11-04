from django import forms


class SearchForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.queryset = kwargs.pop('queryset')
        super(SearchForm, self).__init__(*args, **kwargs)


class FileForm(forms.Form):
    file = forms.FileField()
