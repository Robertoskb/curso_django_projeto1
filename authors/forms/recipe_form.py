from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from recipes.models import Recipe
from utils.authors.django_forms import add_attr
from utils.strings import is_possitive


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = ('title', 'description', 'preparation_time',
                  'preparation_time_unit', 'servings', 'servings_unit',
                  'preparation_steps', 'cover')

        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
            'servings_unit': forms.Select(
                choices=(
                    ('Porções', 'Porções'),
                    ('Pedaços', 'Pedaços'),
                    ('Pessoas', 'Pessoas')
                ),
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                )
            )
        }

    def clean(self):
        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super().clean()

    def clean_title(self):
        field_name = 'title'
        field_value = self.cleaned_data.get(field_name)
        slug = slugify(field_value)

        if len(field_value) < 5:
            self._my_errors[field_name].append(
                'Must have at least 5 characters.')

        recipe_filter = Recipe.objects.filter(slug=slug)
        if recipe_filter.exists() and recipe_filter.first() != self.instance:
            self._my_errors[field_name].append('Title already exists')

        return field_value

    def clean_preparation_time(self):
        field_name = 'preparation_time'
        field_value = self.cleaned_data.get(field_name)

        if not is_possitive(field_value):
            self._my_errors[field_name].append(
                'Must be a positive number')

        return field_value

    def clean_servings(self):
        field_name = 'servings'
        field_value = self.cleaned_data.get(field_name)

        if not is_possitive(field_value):
            self._my_errors[field_name].append(
                'Must be a positive number')

        return field_value
