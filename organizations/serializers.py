from rest_framework import serializers

from organizations.models import Organization

class OrganizationSerializer(serializers.ModelSerializer):
    balance = serializers.IntegerField()

    class Meta:
        model = Organization
        fields = ['inn', 'balance']
