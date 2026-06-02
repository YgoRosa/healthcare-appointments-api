from rest_framework import serializers
from .models import Profissional, Consulta


# class ProfissionalSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profissional
#         fields = "__all__"

class ProfissionalSerializer(serializers.ModelSerializer):

    def validate_nome_social(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                "Nome social deve ter pelo menos 3 caracteres."
            )
        return value

    class Meta:
        model = Profissional
        fields = "__all__"


class ConsultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consulta
        fields = "__all__"
