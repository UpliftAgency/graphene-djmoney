from django.conf.urls import url
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from graphene_django.views import GraphQLView

urlpatterns = [
    path(
        "graphql/",
        csrf_exempt(
            GraphQLView.as_view(graphiql=True)
        ),
        name="graphql",
    ),
]
