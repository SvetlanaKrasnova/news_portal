from django.urls import path
from .views import PersonalAccount, upgrade_me

urlpatterns = [
    path('upgrade/', upgrade_me, name='upgrade'),
    path('user_account/', PersonalAccount.as_view(), name='user_account'),
    path('user_account/subscribe', PersonalAccount.as_view(), name='user_account'),
]
