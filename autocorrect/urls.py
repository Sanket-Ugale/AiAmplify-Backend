from django.contrib import admin
from django.urls import path

import autocorrect

urlpatterns = [
    # path("admin/", admin.site.urls),
    path("autocorrect/login", autocorrect.views.login_api),
    path("register/",autocorrect.views.RegisterUser.as_view()),
]