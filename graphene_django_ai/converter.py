from graphene import Enum
from graphene.utils.str_converters import to_camel_case
from graphene_django.converter import get_choices, convert_django_field

from .utils import tuple_keys_contain_str


def convert_django_field_with_choices(field, registry=None):
    if registry is not None:
        converted = registry.get_converted_field(field)
        if converted:
            return converted
    choices = getattr(field, "choices", None)

    # If we have choices and they contain keys as string...
    if choices and tuple_keys_contain_str(choices):
        meta = field.model._meta
        name = to_camel_case("{}_{}".format(meta.object_name, field.name))
        choices = list(get_choices(choices))
        named_choices = [(c[0], c[1]) for c in choices]
        named_choices_descriptions = {c[0]: c[2] for c in choices}

        class EnumWithDescriptionsType(object):
            @property
            def description(self):
                return named_choices_descriptions[self.name]

        enum = Enum(name, list(named_choices), type=EnumWithDescriptionsType)
        converted = enum(description=field.help_text, required=not field.null)
    # If we have no choices or they are integers
    else:
        converted = convert_django_field(field, registry)
    if registry is not None:
        registry.register_converted_field(field, converted)
    return converted
