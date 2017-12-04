from django import forms

from .models import ArticleTag


class ArticleAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance:
            assert 'initial' not in kwargs
            kwargs['initial'] = {'tags': list(map(str, instance.tags.all()))}
        super().__init__(*args, **kwargs)
        self.fields['tags'].choices = self.get_tag_choices()

    tags = forms.MultipleChoiceField(choices=(), widget=forms.SelectMultiple, required=False)

    @staticmethod
    def get_tag_choices():
        choices = [
            (t.name, str(t))
            for t in ArticleTag.objects.all()
        ]
        return choices
