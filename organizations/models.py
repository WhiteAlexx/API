import uuid
from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator

from django.db import models


class Organization(models.Model):
    '''
    Эта таблица хранит актуальный баланс организации.
    Баланс меняется при получении вебхука.
    Возвращает текущий баланс организации по ИНН.
    '''

    inn = models.CharField(
        primary_key=True,
        unique=True,
        max_length=12,
        editable=False,
        verbose_name='ИНН'
    )   #валидатор длины нужен при записи вручную, в нашем случае новая запись создаётся из вебхука, где длина ИНН верная
    # balance = models.DecimalField(
    #     max_digits=14,
    #     decimal_places=2,
    #     validators=[MinValueValidator(Decimal('0.00'))],    #отключить валидатор, если баланс может быть отрицательным
    #     verbose_name='Баланс'
    # )
    balance = models.PositiveIntegerField(
        default=0,
        verbose_name='Баланс'
    )

    class Meta:
        db_table = 'organizations'
        verbose_name = 'Организацию'
        verbose_name_plural = 'Организации'


class Payment(models.Model):
    '''
    Эта таблица хранит все поступающие вебхуки.
    По ней можно отслеживать изменения балансов.
    '''

    operation_id = models.UUIDField(
        primary_key=True,
        unique=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='ID операции'
    )
    # amount = models.DecimalField(
    #     max_digits=14,
    #     decimal_places=2,
    #     validators=[MinValueValidator(Decimal('0.00'))],
    #     verbose_name='Сумма'
    # )
    amount = models.PositiveIntegerField(
        default=0,
        verbose_name='Сумма'
    )
    payer_inn = models.CharField(
        max_length=12,
        verbose_name='ИНН организации'
    )
    document_number = models.CharField(
        max_length=50,
        verbose_name='Номер документа'
    )
    document_date = models.DateTimeField(
        verbose_name='Дата документа'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания'
    )

    class Meta:
        db_table = 'payments'
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ('payer_inn', '-created_at',)
