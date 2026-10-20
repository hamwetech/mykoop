import uuid

from django.db import models
from datetime import date
from django.urls import reverse
from django.contrib.auth.models import User

from conf.models import District, County, Profession, SubCounty, Parish, Crop, ProductVariation
from system.models.modelmixin import TimeStampMixin


class Clan(TimeStampMixin):
    name = models.CharField(max_length=150, unique=True)
    totem = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'clan'

    def __str__(self):
        return self.name

    @property
    def farmer_count(self):
        return Farmer.objects.filter(clan=self).count()


class Cooperative(TimeStampMixin):
    name = models.CharField(max_length=150, unique=True)
    code = models.CharField(max_length=255, null=True, blank=True)
    district = models.ForeignKey(District, null=True, blank=True, on_delete=models.SET_NULL)
    county = models.ForeignKey(County, null=True, blank=True, on_delete=models.SET_NULL)
    sub_county = models.ForeignKey(SubCounty, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'cooperative'

    def __str__(self):
        return self.name

    @property
    def farmer_count(self):
        return Farmer.objects.filter(cooperative=self).count()


class FarmerGroup(TimeStampMixin):
    name = models.CharField(max_length=150, unique=True)
    cooperative = models.ForeignKey(Cooperative, null=True, blank=True, on_delete=models.SET_NULL)
    district = models.ForeignKey(District, null=True, blank=True, on_delete=models.SET_NULL)
    county = models.ForeignKey(County, null=True, blank=True, on_delete=models.SET_NULL)
    sub_county = models.ForeignKey(SubCounty, null=True, blank=True, on_delete=models.SET_NULL)
    parish = models.ForeignKey(Parish, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'farmer_group'
        verbose_name = 'VLSA'
        verbose_name_plural = 'VLSA'

    def __str__(self):
        return self.name

    @property
    def farmer_count(self):
        return Farmer.objects.filter(farmer_group=self).count()


class Farmer(models.Model):

    LAND_TENURE_CHOICES = [
        ("Customary", "Customary"),
        ("Freehold", "Freehold"),
        ("Mailo", "Mailo"),
        ("Leasehold", "Leasehold"),
    ]

    class EducationLevel(models.TextChoices):
        NONE = "no_education", "No Formal Education"
        PRIMARY = "primary", "Primary"
        O_LEVEL = "o_level", "O-Level (UCE)"
        A_LEVEL = "a_level", "A-Level (UACE)"
        CERTIFICATE = "certificate", "Certificate"
        DIPLOMA = "diploma", "Diploma"
        DEGREE = "degree", "Bachelor's Degree"
        POSTGRAD_DIPLOMA = "pgd", "Postgraduate Diploma"
        MASTERS = "masters", "Master's Degree"
        PHD = "phd", "PhD / Doctorate"

    TITLE_CHOICES = (
        ('Mr', 'Mr'),
        ('Miss', 'Miss'),
        ('Mrs', 'Mrs'),
        ('Dr', 'Dr'),
        ('Prof', 'Prof'),
        ('Hon', 'Hon'),
        ('Fr', 'Fr'),
    )
    image = models.ImageField(upload_to='member/', null=True, blank=True)
    uuid = models.CharField(max_length=150, unique=True, null=True, blank=True)
    member_id = models.CharField(max_length=150, unique=True, null=True, blank=True)
    title = models.CharField(max_length=25, choices=TITLE_CHOICES, null=True, blank=True)
    surname = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    other_name = models.CharField(max_length=150, null=True, blank=True)
    clan = models.ForeignKey(Clan, null=True, blank=True, on_delete=models.SET_NULL)
    cooperative = models.ForeignKey(Cooperative, null=True, blank=True, on_delete=models.SET_NULL)
    farmer_group = models.ForeignKey(FarmerGroup, verbose_name="VSLA", null=True, blank=True, on_delete=models.SET_NULL)
    is_refugee = models.BooleanField(default=False)
    is_handicap = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField('Sex', max_length=10, choices=(('Male', 'Male'), ('Female', 'Female')), null=True,
                              blank=True)
    marital_status = models.CharField(max_length=10, null=True, blank=True,
                                       choices=(('Single', 'Single'), ('Married', 'Married'),
                                                ('Widowed', 'Widow'), ('Divorced', 'Divorced')))
    id_number = models.CharField(max_length=150, null=True, blank=True, unique=True)
    id_type = models.CharField(max_length=150, null=True, blank=True,
                                   choices=(('nin', 'National ID'), ('dl', 'Driving Permit'),
                                        ('pp', 'Passport'), ('o', 'Other')))
    phone_number = models.CharField(max_length=16, null=True, blank=True)
    other_phone_number = models.CharField(max_length=12, null=True, blank=True)
    own_phone = models.BooleanField(default=False)
    has_mobile_money = models.BooleanField(default=False)
    email = models.EmailField(max_length=254, null=True, blank=True)
    district = models.ForeignKey(District, null=True, blank=True, on_delete=models.SET_NULL)
    county = models.ForeignKey(County, null=True, blank=True, on_delete=models.SET_NULL)
    sub_county = models.ForeignKey(SubCounty, null=True, blank=True, on_delete=models.SET_NULL)
    parish = models.ForeignKey(Parish, null=True, blank=True, on_delete=models.SET_NULL)
    village = models.CharField(max_length=150, null=True, blank=True)
    address = models.CharField(max_length=150, null=True, blank=True)
    gps_coordinates = models.CharField(max_length=150, null=True, blank=True)
    land_acreage = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    crop = models.ManyToManyField(Crop, null=True, blank=True)
    savings_balance = models.DecimalField(max_digits=32, decimal_places=2, default=0, blank=True)
    account_balance = models.DecimalField(max_digits=32, decimal_places=2, default=0, blank=True)
    shares_balance = models.DecimalField(max_digits=32, decimal_places=2, default=0, blank=True)
    is_active = models.BooleanField(default=1)
    is_synced = models.BooleanField(default=0)
    sync_date_time = models.DateTimeField(null=True, blank=True)
    qrcode = models.ImageField(upload_to='qrcode', blank=True, null=True)
    card_number = models.CharField(max_length=255, null=True, blank=True)
    create_wallet = models.BooleanField(default=False)
    education_level = models.CharField(max_length=120, null=True, blank=True, choices=EducationLevel.choices)
    children_number = models.IntegerField(null=True, blank=True)
    land_ownership = models.CharField(max_length=120, null=True, blank=True, choices=LAND_TENURE_CHOICES)
    profession = models.ForeignKey(Profession, null=True, blank=True, on_delete=models.SET_NULL)
    has_flexipay = models.BooleanField(default=0)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'farmer'

    def __str__(self):
        return "{} {}".format(self.surname, self.first_name)

    def save(self, *args, **kwargs):
        if not self.member_id:
            self.member_id = self.generate_member_id()
        super().save(*args, **kwargs)

    def generate_member_id(self):
        last_farmer = Farmer.objects.order_by('-id').first()
        if last_farmer and last_farmer.member_id:
            last_number = int(last_farmer.member_id.split('-')[-1])
            new_number = last_number + 1
        else:
            new_number = 1

        return f"MBR-{str(new_number).zfill(5)}"

    @property
    def get_name(self):
        return "%s %s" % (self.surname, self.first_name)

    def get_absolute_url(self):
        return reverse('events.views.details', args=[str(self.id)])

    def age(self, obj):
        m = date.today() - obj.date_of_birth
        return m.days / 365

    @property
    def age_(self):
        m = date.today() - self.date_of_birth
        return m.days / 365


class Collection(TimeStampMixin):
    collection_date = models.DateTimeField()
    cooperative = models.ForeignKey(Cooperative, null=True, blank=True, on_delete=models.CASCADE)
    farmer = models.ForeignKey(Farmer, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    collection_reference = models.CharField(max_length=255, blank=True)
    product = models.ForeignKey(ProductVariation, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=20, decimal_places=2)
    unit_price = models.DecimalField(max_digits=20, decimal_places=2)
    total_price = models.DecimalField(max_digits=20, decimal_places=2)
    repay_loan = models.BooleanField(default=False)
    gps_coordinates =  models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.collection_reference:
            self.collection_reference = f"COL-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'collection'

    def __str__(self):
        return self.collection_reference


class Meeting(TimeStampMixin):
    STATUS = (
        ("Planned", "Planned"),
        ("Ongoing", "Ongoing"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    )

    meeting_date = models.DateField()
    meeting_number = models.PositiveIntegerField()
    venue = models.CharField(max_length=200)
    chaired_by = models.ForeignKey(
        Farmer,
        on_delete=models.SET_NULL,
        null=True,
        related_name="chaired_meetings"
    )
    secretary = models.ForeignKey(
        Farmer,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="recorded_meetings"
    )

    agenda = models.TextField(blank=True)
    minutes = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="Planned"
    )
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Meeting {self.meeting_number}"


class Attendance(TimeStampMixin):
    STATUS = (
        ("Present", "Present"),
        ("Absent", "Absent"),
        ("Excused", "Excused"),
        ("Late", "Late"),
    )
    meeting = models.ForeignKey(
        Meeting,
        on_delete=models.CASCADE
    )
    farmer = models.ForeignKey(
        Farmer,
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="Present"
    )
    present = models.BooleanField(default=True)
    remarks = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ("meeting", "farmer")
