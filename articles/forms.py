from datetime import datetime
import logging

from dateutil.parser import parse
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction
import pytz
from tablib import Dataset

from .models import Article, ArticleRelatedURL, ArticleTag

logger = logging.getLogger(__name__)


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


class ArticleImportForm(forms.Form):
    events_sheet = forms.FileField(required=True, label='Excel or CSV file with events')
    required_fields = {
        'Location', 'Title', 'Start Date', 'Start Time', 'Tags', 'URL',
        'URL Description',
    }

    def clean_events_sheet(self):
        uploaded_file = self.cleaned_data['events_sheet']
        data = Dataset()
        if uploaded_file.name.endswith('.xlsx'):
            try:
                data.xlsx = uploaded_file.read()
            except Exception:
                logger.exception('Could not read Excel workbook upload')
                raise ValidationError('Could not read Excel workbook')
        elif uploaded_file.name.endswith('.csv'):
            try:
                data.csv = uploaded_file.read().decode('utf-8')
            except Exception:
                logger.exception('Could not read CSV upload')
                raise ValidationError('Could not read CSV')
        else:
            raise ValidationError('Unrecognized file type for "%s"' % uploaded_file.name)

        missing_field_list = ', '.join(self.required_fields - set(data.headers))
        if missing_field_list:
            raise ValidationError('Missing fields in uploaded spreadsheet: %s' % missing_field_list)

        setattr(self, 'uploaded_events', data)
        return uploaded_file

    def import_events(self):
        venue_tz = pytz.timezone(settings.TIME_ZONE)
        data = self.uploaded_events
        with transaction.atomic():
            for row in data.dict:
                orig_title = row['Title']
                row['Title'] = row['Title'][:Article.MAX_TITLE_LEN]
                # XXX handle truncation of location

                start_date = row['Start Date']
                start_time = row['Start Time']
                if isinstance(start_date, str) and isinstance(start_time, str):
                    naive_starts_at = parse(start_date + ' ' + start_time)
                else:
                    naive_starts_at = datetime.combine(start_date, start_time)
                starts_at = venue_tz.localize(naive_starts_at)
                existing = Article.objects.filter(
                        flavor=Article.EVENT,
                        location=row['Location'],
                        starts_at=starts_at,
                        title=row['Title']
                ).first()
                if existing:
                    logger.info('Already exists while importing: %s', existing)
                else:
                    article = Article.objects.create(
                        visible=True,
                        flavor=Article.EVENT,
                        location=row['Location'],
                        starts_at=starts_at,
                        title=row['Title']
                    )
                    if orig_title != row['Title']:
                        article.content = '<p>Full event title: "%s"</p>' % orig_title
                        article.full_clean()
                        article.save()
                    for tag in row['Tags'].split(','):
                        article.tags.add(tag)
                    ArticleRelatedURL.objects.create(
                        article=article,
                        url=row['URL'],
                        title=row['URL Description']
                    )
                    logger.info('Added while importing: %s', article)
