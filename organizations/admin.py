from django.contrib import admin

from organizations.models import Organization, Payment


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('inn', 'balance')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('operation_id', 'amount', 'payer_inn', 'document_number', 'document_date', 'created_at')
