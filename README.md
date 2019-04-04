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


### JWT secure mutations


If you derive your mutation from `LoginRequiredDjangoModelFormMutation` you don't have to manually take
care about securing the login with the decorators.

```python
from graphene_django_ai.forms.mutations import LoginRequiredDjangoModelFormMutation
class MyMutation(LoginRequiredDjangoModelFormMutation):
    ...
```


## Run tests locally

**Still W.I.P.!**

    python -m unittest discover -v


## Publish to PyPI

- Run:

    `python setup.py sdist upload`

If you run into trouble, please create a file in your home directory: ~/.pypirc

```
[distutils]
index-servers =
    pypi

[pypi]
repository: https://upload.pypi.org/legacy/
username: 
password: 
```
