from rest_framework import serializers
from .models import Profissional, Consulta
from django.utils import timezone


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
    
    def validate_profissao(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                "Profissão deve ter pelo menos 3 caracteres."
            )
        return value

    def validate_contato(self, value):
        if len(value.strip()) < 8:
            raise serializers.ValidationError(
                "Contato inválido."
            )
        return value
    
    class Meta:
        model = Profissional
        fields = "__all__"


class ConsultaSerializer(serializers.ModelSerializer):

    def validate_data(self, value):
        if value < timezone.now():
            raise serializers.ValidationError(
                "Não é possível agendar consultas no passado."
            )
        return value

    class Meta:
        model = Consulta
        fields = "__all__"