from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.generic import TemplateView

from api.views import *
from rest_framework.routers import DefaultRouter

schema_view = get_schema_view(
   openapi.Info(
      title="BKK API",
      default_version='v1',
      description="API usage description",
      # terms_of_service="https://www.google.com/policies/terms/",
      # contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

router = DefaultRouter()
router.register(r'district', DistrictViewSet, basename='district')
router.register(r'region', RegionViewSet, basename='division')
router.register(r'county', CountyViewSet, basename='county')
router.register(r'sub-county', SubCountyViewSet, basename='sub-county')
router.register(r'parish', ParishViewSet, basename='parish')
router.register(r'village', VillageViewSet, basename='village')
router.register(r'crop', CropViewSet, basename='crop')
router.register(r'clan', ClanViewSet, basename='clan')
router.register(r'cooperative', CooperativeViewSet, basename='cooperative')
router.register(r'farmer-group', FarmerGroupViewSet, basename='farmer-group')
router.register(r'farmers', FarmerViewSet, basename='farmer')
router.register(r'product', ProductViewSet, basename='product')
router.register(r'product-variation', ProductVariationViewSet, basename='product-variation')
router.register(r'production-variation-price', ProductVariationPriceViewSet, basename='production-variation-price')
router.register(r'supplier', SupplierViewSet, basename='supplier')
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'item', ItemViewSet, basename='item')
router.register(r'unit', UnitViewSet, basename='unit')
router.register(r'order', OrderViewSet, basename='order')
router.register(r'order-item', OrderItemViewSet, basename='order-item')
router.register(r'collection', CollectionViewSet, basename='collection')
router.register(r'profession', ProfessionViewSet, basename='profession')
router.register(r'thematic-areas', ThematicAreaViewSet, basename='thematic-area')
router.register(r'training-session', TrainingSessionViewSet, basename='training-session')
router.register(r'training-attendance', TrainingAttendanceViewSet, basename='training-attendance')
router.register(r'external-trainer', ExternalTrainerViewSet, basename='external-trainer')

urlpatterns = [
   path('authenticate/', AuthenticationView.as_view(), name="authenticate"),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   path('titles/', TitleListView.as_view(), name='titles'),
   path('education-level/', EducationLevelView.as_view(), name='education-levelq'),
   path('sync-farmers/', FarmerBulkSyncView.as_view(), name='sync-farmers'),
   path('orders/bulk-create/', OrderCreateView.as_view(), name='order-create'),
   path("app/latest/", LatestVersionAPI.as_view()),
   path("app/download/<int:version_code>/", download_apk),
   path("check-token/", CheckTokenView.as_view(), name="check_token"),
   path("heartbeat/", HeartBeatAPIView.as_view(), name="heartbeat"),

    # path('redoc/', TemplateView.as_view(
    #         template_name='api/redoc.html',
    #         extra_context={'schema_url':'openapi-schema'}
    #     ), name='redoc'),
]
urlpatterns += router.urls