from django.urls import path
from .views import user_list, get_user, GetUserList, GetU2, GetUser, UpdateUserData, GenricApiListView


urlpatterns = [

    # Function based api view
    path("users/" ,user_list),
    path("user/<int:pk>" ,get_user),
    # Class based api view
    path('getUserList/', GetUserList.as_view()),
    path('getU2List/', GetU2.as_view()),
    path("getUserDetail/<int:id>" ,GetUser.as_view()),
    path('updateUser/', UpdateUserData.as_view()),
    # Genric API View
    path("genricApiList/", GenricApiListView.as_view()),
]