from graphene_django.forms.mutation import BaseDjangoFormMutation
from graphql import GraphQLError
from promise import is_thenable, Promise


class BaseAiDjangoFormMutation(BaseDjangoFormMutation):
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
                    ("Cannot set client_mutation_id in the payload object {}").format(
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


class DjangoAiModelFormMutation(BaseAiDjangoFormMutation):
    pass
