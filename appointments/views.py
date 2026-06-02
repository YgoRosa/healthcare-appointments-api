from rest_framework import viewsets

from .models import Profissional, Consulta
from .serializers import ProfissionalSerializer, ConsultaSerializer


class ProfissionalViewSet(viewsets.ModelViewSet):
    queryset = Profissional.objects.all()
    serializer_class = ProfissionalSerializer


class ConsultaViewSet(viewsets.ModelViewSet):
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer