from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name="index"),
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/',views.python_details, name='python details'),
    path('<int:pk>/<path:slug>/', views.python_details, name='python details'),
    path('create/', views.create, name="create")
]
