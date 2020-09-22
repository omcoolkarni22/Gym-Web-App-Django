from django.urls import path
from Gym_App import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='HomePage'),
    path('client_HomePage', views.client_HomePage, name='Client-HomePage'),
    path('client_login', views.client_login, name='client'),
    path('client_CreateAccount', views.client_createAccount, name="CreateAccount_Client"),
    path('Client_CreateAccount', views.Client_CreateAccount, name='Client_CreateAccount'),
    path('Client_Logout', views.Client_Logout, name='Client_Logout'),
    path('Trainer', views.Trainer, name='Trainer'),
    path('Trainer_CreateAccount', views.Trainer_CreateAccount, name='Trainer_CreateAccount'),
    path('Extra_trainer_data', views.Extra_trainer_data, name='Extra_trainer_data'),
    path('Trainer_Login', views.Trainer_Login, name='Trainer_Login'),
    path('Trainer_Logout', views.Trainer_Logout, name='Trainer_Logout'),
    path('TrainerDetails/<int:trid>', views.TrainerDetails, name="TrainerDetails"),
    path('TrainerDetails/Train_Message', views.TrainerMessages, name='Train_Message'),
    path('Messages', views.ClientMessage_fetch, name='Message'),
    path('ChangeProfile_Client', views.ChangeProfile_Client, name='ChangeProfile_Client'),
    path('ChangeProfile_Trainer', views.ChangeProfile_Trainer, name='ChangeProfile_Trainer'),
    path('mapview', views.mapview, name='mapview'),
    path('filter', views.filter, name='filter')

]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

