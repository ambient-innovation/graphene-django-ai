import graphene_django as gd
import graphene_django.converter
from graphene_django.forms import converter

from .converter import convert_django_field_with_choices
from .forms.converter import convert_form_field_to_string, convert_form_field_to_choice

# Rewire graphene-django logic to work with our functions
gd.converter.convert_django_field_with_choices = convert_django_field_with_choices
gd.types.convert_django_field_with_choices = convert_django_field_with_choices
gd.forms.converter.convert_form_field_to_string = convert_form_field_to_string
gd.forms.converter.convert_form_field_to_choice = convert_form_field_to_choice
gd.forms.converter.convert_form_field_to_choice = convert_form_field_to_choice


# Version
__version__ = "1.0.1"
