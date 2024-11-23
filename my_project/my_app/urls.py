from django.urls import path,include
from .views import *
urlpatterns = [
    path("children/",ChildrenViews.as_view()),
    path("children/<int:child_id>/",ChildrenViews.as_view()),
    path("parent/",ParentViews.as_view()),
    path("parent/<int:parent_id>/",ParentViews.as_view())
]
