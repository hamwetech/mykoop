import json
import datetime
from rest_framework import generics
from django.shortcuts import render
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.gis.geos import Point
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FileUploadParser
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser, FileUploadParser
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from api.serializers import *
from system.models import Farmer, AppVersion
from system.models.application import Device, DeviceHeartBeat


class AuthenticationView(APIView):
    @swagger_auto_schema(operation_description="description", request_body=LoginSerializer, responses={200: AuthenticationShemaSerialiser})
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        try:
            if serializer.is_valid():
                data = request.data
                username = data.get('username')
                password = data.get('password')
                user = authenticate(username=username, password=password)
                if user:
                    token = Token.objects.get(user=user)
                    # if user.farm_assigned_to:
                    return Response({
                        "status": "success",
                        "response": {
                            "token": token.key,
                            "user": {
                                "id": user.id,
                                "username": user.username,
                                "name": user.get_full_name() or "",
                                "email": user.email,
                                "is_superuser": user.is_superuser,
                                "is_active": user.is_active,
                            }
                        }
                    }, status.HTTP_200_OK)
                    # return Response({"status": "error", "response": "User is not assigned to any farm"},
                    #                 status.HTTP_200_OK)
                return Response({"status": "error", "response": "Username or password incorrect"}, status.HTTP_200_OK)
        except Exception as err:
            return Response({"status": "error", "response": "%s" % err}, status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegionViewSet(viewsets.ModelViewSet):
    serializer_class = RegionSerializer
    http_method_names = ['retrieve', 'get']
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = Region.objects.all()
        serializer = RegionSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = District.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = DistrictSerializer(user)
        return Response(serializer.data)


class DistrictViewSet(viewsets.ModelViewSet):
    serializer_class = DistrictSerializer
    http_method_names = ['retrieve', 'get']
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = District.objects.all()
        serializer = DistrictSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = District.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = DistrictSerializer(user)
        return Response(serializer.data)


class UnitViewSet(viewsets.ModelViewSet):
    serializer_class = UnitSerializer
    http_method_names = ['retrieve', 'get']

    def get_queryset(self):
        return Unit.objects.all()

    def list(self, request):
        queryset = Unit.objects.all()
        serializer = UnitSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Unit.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UnitSerializer(user)
        return Response(serializer.data)


class CountyViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for listing or retrieving Breed.
    """
    serializer_class = CountySerializer
    http_method_names = ['retrieve', 'get']
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = County.objects.all()
        serializer = CountySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = County.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = CountySerializer(user)
        return Response(serializer.data)


class SubCountyViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for listing or retrieving Breed.
    """
    serializer_class = SubCountySerializer
    http_method_names = ['retrieve', 'get']
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = SubCounty.objects.all()
        serializer = SubCountySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = SubCounty.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = SubCountySerializer(user)
        return Response(serializer.data)


class ParishViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for listing or retrieving Breed.
    """
    serializer_class = ParishSerializer
    http_method_names = ['retrieve', 'get']
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = Parish.objects.all()
        serializer = ParishSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Parish.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ParishSerializer(user)
        return Response(serializer.data)


class VillageViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for listing or retrieving Breed.
    """
    serializer_class = VillageSerializer
    http_method_names = ['retrieve', 'get']
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = Village.objects.all()
        serializer = VillageSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Village.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = VillageSerializer(user)
        return Response(serializer.data)


class CropViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for listing or retrieving Breed.
    """
    serializer_class = CropSerializer
    http_method_names = ['retrieve', 'get']
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = Crop.objects.all()
        serializer = CropSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Crop.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = CropSerializer(user)
        return Response(serializer.data)


class ClanViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for listing or retrieving Breed.
    """
    serializer_class = ClanSerializer
    http_method_names = ['retrieve', 'get']
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = Clan.objects.all()
        serializer = ClanSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Clan.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ClanSerializer(user)
        return Response(serializer.data)


class CooperativeViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for listing or retrieving Breed.
    """
    serializer_class = CooperativeSerializer
    http_method_names = ['retrieve', 'get']
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = Cooperative.objects.all()
        serializer = CooperativeSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Cooperative.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = CooperativeSerializer(user)
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ['retrieve', 'get']
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class ProfessionViewSet(viewsets.ModelViewSet):
    queryset = Profession.objects.all()
    http_method_names = ['retrieve', 'get']
    serializer_class = ProfessionSerializer


class ProductVariationViewSet(viewsets.ModelViewSet):
    queryset = ProductVariation.objects.all()
    serializer_class = ProductVariationSerializer


class ProductVariationPriceViewSet(viewsets.ModelViewSet):
    queryset = ProductVariationPrice.objects.all()
    serializer_class = ProductVariationPriceSerializer


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer


class FarmerGroupViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for listing or retrieving Breed.
    """
    serializer_class = FarmerGroupSerializer
    http_method_names = ['retrieve', 'get']
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = FarmerGroup.objects.all()
        serializer = FarmerGroupSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = FarmerGroup.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = FarmerGroupSerializer(user)
        return Response(serializer.data)


class TitleListView(APIView):
    def get(self, request):
        titles = [{'value': key, 'label': value} for key, value in Farmer.TITLE_CHOICES]
        return Response(titles)


class EducationLevelView(APIView):
    def get(self, request):
        titles = [{'value': key, 'label': value} for key, value in Farmer.EducationLevel.choices]
        return Response(titles)


class FarmerViewSet(viewsets.ModelViewSet):
    queryset = Farmer.objects.all()
    serializer_class = FarmerSerializer


class FarmerBulkSyncView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        # Get the farmer JSON part
        farmer_json = request.data.get('farmer')
        image_file = request.FILES.get('image')

        if not farmer_json:
            return Response({"error": "No farmer data provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Load JSON to dict
        farmer_data = json.loads(farmer_json)

        # Attach image if provided
        if image_file:
            farmer_data['image'] = image_file

        # Try to get existing farmer by UUID
        uuid_value = farmer_data.get('uuid')
        try:
            instance = Farmer.objects.get(uuid=uuid_value)
        except Farmer.DoesNotExist:
            instance = None

        # Pass instance to serializer for update/create
        serializer = FarmerSerializer(instance=instance, data=farmer_data)
        if serializer.is_valid():
            farmer = serializer.save()
            farmer.is_synced = True
            farmer.sync_date_time = datetime.datetime.now()
            farmer.save()
            print(farmer.district)
            return Response({"success": True, "member_id": farmer.member_id})
        else:
            return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ThematicAreaViewSet(viewsets.ModelViewSet):
    serializer_class = ThematicAreaSerializer
    http_method_names = ['retrieve', 'get']
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = ThematicArea.objects.all()
        serializer = ThematicAreaSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = ThematicArea.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ThematicAreaSerializer(user)
        return Response(serializer.data)


class TrainingSessionViewSet(viewsets.ModelViewSet):
    serializer_class = TrainingSessionSerializer
    http_method_names = ['retrieve', 'get', 'post']
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = TrainingSession.objects.all()
        serializer = TrainingSessionSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = TrainingSession.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = TrainingSessionSerializer(user)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        try:
            # 🔥 1. Get JSON string safely
            session_json = request.data.get('session')
            if not session_json:
                return Response(
                    {"error": "Session data is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            session_data = json.loads(session_json)

            # 🔥 2. Get image (optional)
            image = request.FILES.get('training_image')

            # 🔥 3. Validate & save
            serializer = self.get_serializer(data=session_data)
            serializer.is_valid(raise_exception=True)

            session = serializer.save(
                training_image=image if image else None
            )

            # 🔥 4. Return response
            return Response(
                self.get_serializer(session).data,
                status=status.HTTP_201_CREATED
            )

        except json.JSONDecodeError:
            return Response(
                {"error": "Invalid JSON format"},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TrainingAttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = TrainingAttendanceSerializer
    http_method_names = ['retrieve', 'get', 'post']
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = TrainingAttendance.objects.all()
        serializer = TrainingAttendanceSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = TrainingAttendance.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = TrainingAttendanceSerializer(user)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data
        is_bulk = isinstance(data, list)

        if not is_bulk:
            data = [data]

        created_objects = []

        for item in data:
            farmer_ref = item.pop('farmer_reference', None)
            training_ref = item.pop('training_reference', None)

            #resolve farmer
            farmer = Farmer.objects.filter(uuid=farmer_ref).first()
            if not farmer:
                return Response(
                    {"error": f"Farmer not found: {farmer_ref}"},
                    status=400
                )

            #resolve training session
            session = TrainingSession.objects.filter(
                training_reference=training_ref
            ).first()

            if not session:
                return Response(
                    {"error": f"Training not found: {training_ref}"},
                    status=400
                )

            item['trainer'] = User.objects.get(pk=item['trainer'])

            #UPSERT (prevents duplicates)
            item.pop("farmer", None)
            item.pop("training_session", None)
            item.pop("id", None)

            obj, created = TrainingAttendance.objects.update_or_create(
                farmer=farmer,
                training_session=session,
                defaults=item
            )

            created_objects.append(obj)

        serializer = self.get_serializer(created_objects, many=True)
        return Response(serializer.data, status=201)


class ExternalTrainerViewSet(viewsets.ModelViewSet):
    serializer_class = ExternalTrainerSerializer
    http_method_names = ['retrieve', 'get']
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = ExternalTrainer.objects.all()
        serializer = ExternalTrainerSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = ExternalTrainer.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ExternalTrainerSerializer(user)
        return Response(serializer.data)


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer



class LatestVersionAPI(APIView):

    def get(self, request):
        latest = AppVersion.objects.filter(is_active=True).order_by("-version_code").first()

        return Response({
            "version_code": latest.version_code,
            "version_name": latest.version_name,
            "force_update": latest.force_update,
            "release_notes": latest.release_notes,
            "apk_url": request.build_absolute_uri(latest.apk_file.url)
        })


def download_apk(request, version_code):
    app = AppVersion.objects.get(version_code=version_code)
    return FileResponse(app.apk_file.open(), as_attachment=True)


class CheckTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token_key = request.data.get("token")

        if not token_key:
            return Response(
                {"valid": False, "message": "No token provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = Token.objects.get(key=token_key)
            user = token.user

            return Response({
                "valid": True,
                "user_id": user.id,
                "username": user.username
            }, status=status.HTTP_200_OK)

        except Token.DoesNotExist:
            return Response(
                {"valid": False, "message": "Invalid token"},
                status=status.HTTP_401_UNAUTHORIZED
            )


class HeartBeatAPIView(APIView):
    def post(self, request):
        data = request.data
        user_id = data.get('user_id')
        device_id = data.get('device_id')

        try:
            # 1. Ensure User and Device exist
            user = User.objects.get(id=user_id)
            
            # Update or Create the Device entry for this user
            device, created = Device.objects.update_or_create(
                device_id=device_id,
                defaults={'user': user, 'is_active': True}
            )

            # 2. Create the Heartbeat
            DeviceHeartBeat.objects.create(
                device=device,
                gps_coodinates=data.get('gps_coodinates'),
                request = data
                # entry_date is auto_now_add in model
            )

            return Response({"status": "success"}, status=status.HTTP_201_CREATED)
        
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)