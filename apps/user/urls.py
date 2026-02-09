from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


app_name = "user"

urlpatterns = [
    path("update_u/<int:pk>/", login_required(views.UserUpdateView.as_view()), name="update_u"),
    path("profile/<int:pk>", views.UserDetailView.as_view(), name="profile"),
]
