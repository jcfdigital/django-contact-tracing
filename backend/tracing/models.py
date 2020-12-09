import pytz

from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.deletion import CASCADE, RESTRICT
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.conf import settings

User = get_user_model()

def make_qr_code(ccc, local_tz=settings.TIME_ZONE):

        allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        local_date = pytz.timezone(local_tz).normalize(timezone.now()).date()
        mm=local_date.month
        dd=local_date.day
        yy=local_date.year-2000
        str=get_random_string(8, allowed_chars)
        return (f'QRC{mm:02d}{dd:02d}{yy:02d}'+str+f'{ccc:03d}')

class UserProfileModel(models.Model):

    GENDER_CHOICES = [
        ('M', 'Male'), 
        ('F', 'Female')
    ]

    SUFFIX_CHOICES = [
        ('JR', 'JR'),
        ('SR', 'SR'),
        ('I', 'I'),
        ('II', 'II'),
        ('III', 'III'),
        ('IV', 'IV'),
        ('V', 'V'),
        ('VI', 'VI'),
        ('VII', 'VII'),
        ('VIII', 'VIII'),
        ('IX', 'IX'),
        ('X', 'X'),
        ('XI', 'XI'),
        ('XII', 'XII'),
    ]

    email = models.OneToOneField(User, on_delete=RESTRICT, verbose_name='Email Address')
    fname = models.CharField('First Name', max_length=256)
    mname = models.CharField('Middle Name', max_length=256, null=True, blank=True)
    lname = models.CharField('Last Name', max_length=256)
    ename = models.CharField('Suffix',  max_length=4, choices=SUFFIX_CHOICES, null=True, blank=True)
    gender = models.CharField('Gender', max_length=1, choices=GENDER_CHOICES)
    birthdate = models.DateField('Date of Birth')
    mobile1 = models.CharField('Primary Mobile No.', max_length=11)
    mobile1_confirmed = models.BooleanField('Confirmed', default=False)
    mobile2 = models.CharField('Alternative Mobile No.', max_length=11, null=True, blank=True)
    mobile2_confirmed = models.BooleanField('Confirmed', default=False)

    current_street = models.CharField('Street ', max_length=256)
    current_town = models.CharField('Barangay/Town', max_length=256)
    current_city = models.CharField('City/Municipality', max_length=256)
    current_region = models.CharField(' State/Province', max_length=256)

    perm_street = models.CharField('Street', max_length=256)
    perm_town = models.CharField('Barangay/Town', max_length=256)
    perm_city = models.CharField('City/Municipality', max_length=256)
    perm_region = models.CharField('State/Province', max_length=256)

    face_photo = models.ImageField('Photo', upload_to='face')
    id_photo = models.ImageField('ID Photo', upload_to='id')

    qr_code_text = models.CharField('QR Code Text', max_length=20, blank=True)

    time_created = models.DateTimeField('Time Created',auto_now_add=True)
    time_updated = models.DateTimeField('Time Updated',auto_now=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        if not self.mname:
            if not self.ename:
                full_name = (f'{self.lname}, {self.fname}')
            else:
                full_name = (f'{self.lname}, {self.fname} {self.ename}')
        else:
            if not self.ename:
                full_name = (f'{self.lname}, {self.fname} {self.mname[0]}.')
            else:
                full_name = (f'{self.lname}, {self.fname} {self.ename} {self.mname[0]}.')
        return full_name.strip()

    def save(self, *args, **kwargs):

        if not UserProfileModel.objects.filter(email=self.email, qr_code_text__startswith="QRC"):
            ccc = int(UserProfileModel.objects.all().count()+1)

            # reset ccc to 0
            if ccc >= 1000:
                ccc = ccc - 1000

            # Check if generated qr_code_text exists, increment by 1 until false
            for user in UserProfileModel.objects.filter(qr_code_text=make_qr_code(ccc)):
                ccc += 1

            self.qr_code_text = make_qr_code(ccc)

        super(UserProfileModel, self).save(*args, **kwargs)

class EstablishmentProfileModel(models.Model):

    email = models.OneToOneField(User, on_delete=RESTRICT, verbose_name='Email Address')
    establishment_name = models.CharField('Establishment Name', max_length=256)
    street = models.CharField('Street', max_length=256)
    town = models.CharField('Barangay/Town', max_length=256)
    city = models.CharField('City/Municipality', max_length=256)
    region = models.CharField('State/Province', max_length=256)

    mobile1 = models.CharField('Primary Mobile No.', max_length=11)
    mobile1_confirmed = models.BooleanField('Confirmed', default=False)
    mobile2 = models.CharField('Alternative Mobile No.', max_length=11, null=True, blank=True)
    mobile2_confirmed = models.BooleanField('Confirmed', default=False)
    landline = models.CharField('Landline No.', max_length=11)
    landline_confirmed = models.BooleanField('Confirmed', default=False)

    time_created = models.DateTimeField('Time Created', auto_now_add=True)
    time_updated = models.DateTimeField('Time Updated', auto_now=True)

    class Meta:
        verbose_name = 'Establishment Profile'
        verbose_name_plural = 'Establishment Profiles'

    def __str__(self):
        return self.establishment_name

class TracingModel(models.Model):

    TRANSACT_CHOICES = [
        ('EN', 'Entry'),
        ('EX', 'Exit')
    ]

    user_profile = models.ForeignKey(UserProfileModel, on_delete=models.RESTRICT, verbose_name="Person")
    establishment_profile = models.ForeignKey(UserProfileModel, on_delete=models.RESTRICT, verbose_name="Establishment")
    transact = models.CharField('Transaction', max_length=2, choices=TRANSACT_CHOICES)
    transact_time = models.DateTimeField('Transaction Time', auto_now=True)

    class Meta:
        verbose_name = 'Trace'
        verbose_name_plural = 'Traces'

    def __str__(self):
        return self.transact + ' of ' + self.user_profile + ' at ' + self.establishment_profile