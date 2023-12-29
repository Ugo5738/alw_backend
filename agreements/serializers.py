from rest_framework import serializers

from agreements.models import Agreement, Amendment, DigitalSignature


class AgreementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agreement
        fields = "__all__"


class AmendmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amendment
        fields = "__all__"


class DigitalSignatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalSignature
        fields = "__all__"
