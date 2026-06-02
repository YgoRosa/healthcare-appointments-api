from rest_framework.routers import DefaultRouter

from .views import ProfissionalViewSet, ConsultaViewSet

router = DefaultRouter()

router.register(r'profissionais', ProfissionalViewSet)
router.register(r'consultas', ConsultaViewSet)

urlpatterns = router.urls