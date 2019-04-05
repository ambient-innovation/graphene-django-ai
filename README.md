# graphene-django-ai
Toolbox for changes to streamline graphene-django


## Installation

For installing graphene, just run this command in your shell

```bash
pip install "graphene-django-ai>=1.0.0"
```

## Setup

Refer to the documentation of `django-graphene` base package.   

https://github.com/graphql-python/graphene-django/blob/master/README.md

## Interesting to know

Some internal functions of `graphene-django` are monkey-patched inside the `__init__.py`. If you want to take
a look "under the hood", have a look at this file.

## Examples

### GraphQL based on django ModelForms

Here is a simple Django model in `my_app/models.py`:

```python
from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
```

Now we create a `ModelForm` in `my_app/forms.py`:

```python
from django import forms
from .models import User

class SpaceForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = []
```

 We need to create an `ObjectType` which we derive from our model. 
 Lives in `my_apps/schemes/schematypes.py`:
 
```python
from graphene_django import DjangoObjectType
from ..models import User

class UserType(DjangoObjectType):
    class Meta:
        model = User
```

 Here's the mutation in `my_app/schema/mutations.py`. 
 It takes a `ModelForm` (or a non-model form) to derive the validation rules from:
 
 ```python
import graphene
from graphene_django_ai.forms.mutations import LoginRequiredDjangoModelFormMutation
from .schematypes import UserType
from ..forms import UserForm
 

class UserCreateUpdateMutation(LoginRequiredDjangoModelFormMutation):
    space = graphene.Field(UserType)

    class Meta:
        form_class = UserForm

 
# Register new mutation
class UserMutation(graphene.ObjectType):
    spaces = UserCreateUpdateMutation.Field(description='Create and update users')
 ```
 
 If you register now your `UserMutation` in your schema you have a working model-based and DRY API 
 endpoint. Congratulations!

### DeleteMutation for django-model objects

If you want to delete an object you can easily use the `DeleteMutation` like this:

```python
from graphene_django_ai.schemes.mutations import DeleteMutation
from my_app.models import MyModel

class MyModelDeleteMutation(DeleteMutation):
    class Meta:
        model = MyModel
```

If you are using `django-graphql-jwt` authentication you can ensure only logged in access to your delete endpoint like this:

```python
from graphene_django_ai.schemes.mutations import LoginRequiredDeleteMutation
from my_app.models import MyModel

class MyModelDeleteMutation(LoginRequiredDeleteMutation):
    class Meta:
        model = MyModel
```

If you need to customize the **validation** or the **base queryset** you can override methods like this:

```python
from graphene_django_ai.schemes.mutations import LoginRequiredDeleteMutation
from graphql import GraphQLError
from my_app.models import MyModel

class MyModelDeleteMutation(LoginRequiredDeleteMutation):
    class Meta:
        model = MyModel
        
    def validate(self, request):
        if not request.user.is_superuser:
            raise GraphQLError("This is only allowed for superusers!")
    
    def get_queryset(self, request):
        return self.model.objects.filter(created_by=request.user)
```


### JWT secure mutations


If you derive your mutation from `LoginRequiredDjangoModelFormMutation` you don't have to manually take
care about securing the login with the decorators.

```python
from graphene_django_ai.forms.mutations import LoginRequiredDjangoModelFormMutation
class MyMutation(LoginRequiredDjangoModelFormMutation):
    ...
```

## Testing GraphQL calls

If you want to unittest your API calls derive your test case from the class `GraphQLTestCase`.

Usage:

```python
import json

from graphene_django.tests.base_test import GraphQLTestCase
from my_project.config.schema import schema

class MyFancyTestCase(GraphQLTestCase):

    # Here you need to inject your test case's schema
    GRAPHQL_SCHEMA = schema
    
    def test_some_query(self):
        response = self.query(
            '''
            query {
                myModel {
                    id
                    name
                }
            }
            ''',
            op_name='myModel'
        )
        content = json.loads(response.content)
        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)
        
        # Add some more asserts if you like
        ...
        
    def test_some_mutation(self):
        response = self.query(
            '''
            mutation myMutation($input: MyMutationInput!) {
                myMutation(input: $input) {
                    my-model {
                        id
                        name
                    }
                }
            }
            ''',
            op_name='myMutation',
            input_data={'my_field': 'foo', 'other_field': 'bar'}
        )
        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)
        
        # Add some more asserts if you like
        ...

    def test_failing_call(self):
    
       response = self.query(
           '''
           mutation myMutation($input: MyMutationInput!) {
               myMutation(input: $badInput) {
                   my-model {
                       id
                       name
                   }
               }
           }
           ''',
           op_name='myMutation',
           input_data={'my_field': 'foo', 'other_field': 'bar'}
       )
       # This assert tests if the call raised some errors
       # For example if you want to test if invalid input is handled correctly by your endpoint
       self.assertResponseHasErrors(response)
       
       # Add some more asserts if you like
       ... 

```

## Run tests locally

**Still W.I.P.!**

    python -m unittest discover -v


## Relase a new version

- Update `Changelog` in `Readme.md`
 
- Create pull request / merge to master

- Run:

    * Make sure you have all the required packages installed  
    `pip install twine wheel`
    * Create a file in your home directory: `~/.pypirc`
    ```
    [distutils]
    index-servers=
        pypi
        testpypi
    
    [pypi]
    repository: https://upload.pypi.org/legacy/
    username: ambient-innovation
    
    [testpypi]
    repository: https://test.pypi.org/legacy/
    username: ambient-innovation
    ```
    * Create distribution  
    `python setup.py sdist bdist_wheel`
    * Upload to Test-PyPi  
    `twine upload --repository testpypi dist/*`
    * Check at Test-PyPi if it looks nice  
    * Upload to real PyPi  
    `twine upload dist/*`

## Changelog

* **1.0.4** (2019-04-05)
    * Fixed a bug that a BooleanField from a django form would always be required
    
* **1.0.3** (2019-04-05)
    * Added delete mutation for django-model objects `DeleteMutation`
    * Added delete mutation which ensures JWT authentication
    
* **1.0.2** (2019-04-05)
    * Updated deployment documentation
    * Added markdown support to Readme file
    
* **1.0.1** (2019-04-05)
    * Added documentation about `GraphQLTestCase` 
    * Put version to variable in `__init__.py`

* **1.0.0** (2019-04-04)
    * Initial package released
