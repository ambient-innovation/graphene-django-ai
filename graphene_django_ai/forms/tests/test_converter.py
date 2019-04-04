from django import forms
from graphene import Int
from graphene_django.forms.tests.test_converter import assert_conversion


def test_should_choice_convert_string():
    """
    If no string choice is found we interpret it as `string`
    """
    assert_conversion(forms.ChoiceField, Int)
