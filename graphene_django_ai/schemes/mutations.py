import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import login_required


class DeleteMutation(graphene.ClientIDMutation):
    success = graphene.Boolean()
    model = None

    class Meta:
        abstract = True

    class Input:
        id = graphene.ID()

    @classmethod
    def __init_subclass_with_meta__(cls, resolver=None, output=None, arguments=None, _meta=None, model=None, **options):
        if not model:
            raise AttributeError('DeleteMutation needs a valid model to be set.')
        super().__init_subclass_with_meta__(resolver, output, arguments, _meta, **options)
        cls.model = model

    @classmethod
    def validate(cls, request):
        """
        Feel free to put any kind of custom validation rules here
        """
        return True

    @classmethod
    def get_queryset(cls, request):
        """
        Defines the queryset on which the object with the given ID can be chosen
        """
        return cls.model.objects.all()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input_data):

        if not cls.validate(info.context):
            raise GraphQLError('Delete method not allowed.')

        # Get object id
        object_id = int(input_data.get('id', None))

        # Find and delete object
        obj = cls.get_queryset(info.context).get(pk=object_id)
        obj.delete()

        # Return success
        return DeleteMutation()


class LoginRequiredDeleteMutation(DeleteMutation):
    """
    Deletes an object from the database.
    Ensures user is authenticated with GraphQL-JWT
    """

    class Meta:
        abstract = True

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input_data):
        return super(LoginRequiredDeleteMutation, cls).mutate_and_get_payload(root, info, **input_data)
