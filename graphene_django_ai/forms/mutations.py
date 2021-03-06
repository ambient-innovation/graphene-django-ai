from graphene_django.forms.mutation import DjangoModelFormMutation
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from promise import is_thenable, Promise


class DjangoValidatedModelFormMutation(DjangoModelFormMutation):
    """
    Takes django ModelForm validations and passes them to GraphQL like any other validation error
    """

    class Meta:
        abstract = True

    @classmethod
    def mutate(cls, root, info, input):
        """
        Most code derived one-to-one from base class
        :return:
        """

        def on_resolve(payload):
            try:
                payload.client_mutation_id = input.get("client_mutation_id")
            except Exception:
                raise Exception(
                    "Cannot set client_mutation_id in the payload object {}".format(
                        repr(payload)
                    )
                )
            return payload

        result = cls.mutate_and_get_payload(root, info, **input)

        if result.errors:
            err_msg = ''
            for err in result.errors:
                err_msg += f"Field '{err.field}': {err.messages[0]} "

            raise GraphQLError(err_msg.strip())

        if is_thenable(result):
            return Promise.resolve(result).then(on_resolve)

        return on_resolve(result)


class LoginRequiredDjangoModelFormMutation(DjangoValidatedModelFormMutation):
    """
    Ensures that you need to be logged in with GraphQL JWT (json web token) authentication
    """
    class Meta:
        abstract = True

    @classmethod
    @login_required
    def perform_mutate(cls, form, info):
        return super().perform_mutate(form, info)
