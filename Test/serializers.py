from rest_framework import serializers

from Test.models import Test


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ('username',  'email', 'date_of_birth', 'phone')