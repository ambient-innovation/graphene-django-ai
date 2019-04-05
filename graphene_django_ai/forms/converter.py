from django import forms
from graphene import String, Int, Boolean
from graphene_django.forms.converter import convert_form_field

from ..utils import tuple_keys_contain_str


@convert_form_field.register(forms.fields.BaseTemporalField)
@convert_form_field.register(forms.CharField)
@convert_form_field.register(forms.EmailField)
@convert_form_field.register(forms.SlugField)
@convert_form_field.register(forms.URLField)
@convert_form_field.register(forms.RegexField)
@convert_form_field.register(forms.Field)
def convert_form_field_to_string(field):
    return String(description=field.help_text, required=field.required)


@convert_form_field.register(forms.ChoiceField)
def convert_form_field_to_choice(field):
    """
    Determines if you want the field as the choice's integer or as a string
    """
    has_str_choices = tuple_keys_contain_str(field.choices)
    if has_str_choices:
        return String(description=field.help_text, required=field.required)
    return Int(description=field.help_text, required=field.required)


@convert_form_field.register(forms.BooleanField)
def convert_form_field_to_boolean(field):
    return Boolean(description=field.help_text, required=field.required)
