from django.db import transaction, models

from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from organizations.models import Organization, Payment
from organizations.serializers import OrganizationSerializer


class PaymentView(APIView):
    '''
    Если операция уже была (operation_id) — ничего не делает, возвращает 200 OK.
    Требуется защита от дублей, то есть если приходит тот же самый вебхук, мы не должны заново пополнять баланс.
    Если новая:
        создаёт Payment (логирует изменение баланса (в таблицу payment))
        если организации нет (payer_inn новый), создаёт организацию
        начисляет сумму на баланс организации с payer_inn
    
    '''

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        data = request.data

        # if not self.verify_signature(request):    #Здесь нужно обязательно проверять подпись отправителя
        #     return Response({
        #         'status': 'error',
        #         'message': 'Invalid signature'
        #     }, status=status.HTTP_403_FORBIDDEN)

        try:
            with transaction.atomic():

                if Payment.objects.filter(operation_id=data.get('operation_id')).exists():
                    return Response({
                        'status': 'already processed',
                        'message': 'Payment already processed'
                    }, status=status.HTTP_200_OK)

                Payment.objects.create(
                    operation_id=data.get('operation_id'),
                    amount=data['amount'],
                    payer_inn=data['payer_inn'],
                    document_number=data['document_number'],
                    document_date=data['document_date'],
                )

                organization, create = Organization.objects.select_for_update().get_or_create(
                    inn=data['payer_inn'],
                    defaults={'balance': 0}
                )

                Organization.objects.filter(inn=data['payer_inn']).update(
                    balance=models.F('balance') + data['amount']
                )

                organization.refresh_from_db()

                return Response({
                    'status': 'ok',
                    'message': 'Payment processed',
                    'balance': organization.balance
                }, status=status.HTTP_200_OK)

        except KeyError as e:
            return Response({
                'status': 'key_error',
                'message': f"Missing key: {str(e)}"
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def verify_signature(self, request):
        '''
        Здесь нужно обязательно проверять подпись отправителя
        '''
        return True


class BalanceView(RetrieveAPIView):
    '''
    Возвращает текущий баланс организации по ИНН
    '''

    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    lookup_url_kwarg = 'inn'
