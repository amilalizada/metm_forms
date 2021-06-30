from django.urls import path
from Forms.views import FormsMetm 

app_name = 'forms'

urlpatterns = [
    path('<int:id>/',FormsMetm.as_view(),name ='form_page'),
    # path('nese/',SaveFormView.as_view(),name ='form_save'),
]