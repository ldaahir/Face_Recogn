from django.urls import path
from .views import *
urlpatterns=[

    path("dashboard/",login,name="login"),
    path("check/",check,name="check"),
    path("save/",save,name="save"),
    path("",index,name="index"),
    path("train/",train,name="train"),
    path("test/",test,name="test"),
    path("logout/",logout,name="logout"),
    path("rename/",rename,name="rename"),
    path("recognize_faces/",recognize_faces,name="recognize_faces")

]
