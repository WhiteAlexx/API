from django.urls import path

from organizations.views import PaymentView, BalanceView

app_name = 'organizations'

urlpatterns = [
    path('webhook/bank/', PaymentView.as_view()),
    path('organizations/<str:inn>/balance/', BalanceView.as_view())
]
