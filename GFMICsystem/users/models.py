from django.db import models
from datetime import datetime
import os, random
from django.utils.html import mark_safe
from django.utils import timezone
from django.urls import reverse

  
now = timezone.now()

def image_path(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    randomstr =''.join((random.choice(chars)) for x in range(5))
    _now = datetime.now()

    return 'proof_pic/{year}-{month}-{day}-{basename}-{randomstring}{ext}'.format(basename = basefilename, randomstring=randomstr, ext=file_extension, year=_now.strftime('%Y'), month=_now.strftime('%m'), day=_now.strftime('%d'))

def event_image_path(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    randomstr =''.join((random.choice(chars)) for x in range(5))
    _now = datetime.now()

    return 'event_img/{year}-{month}-{day}-{basename}-{randomstring}{ext}'.format(basename = basefilename, randomstring=randomstr, ext=file_extension, year=_now.strftime('%Y'), month=_now.strftime('%m'), day=_now.strftime('%d'))


class Membership(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_no = models.CharField(unique=True, max_length=15, verbose_name='User Number')
    user_email = models.EmailField(unique=True, max_length=200, verbose_name='Email Address')
    user_e_password = models.BinaryField(null=True)
    user_password = models.CharField(max_length=200, verbose_name="Password")
    user_sub = models.CharField(max_length=16, verbose_name='Subscription', default="GUEST")
    user_status = models.CharField(max_length=16, verbose_name='Status', default="ACTIVE")
    user_application = models.CharField(max_length=16, verbose_name='User Application', null = True)
    user_pmode = models.CharField(max_length=16, verbose_name='User Payment', null = True)
    user_amount = models.IntegerField(null=True)
    user_validity = models.DateTimeField(max_length=50, null=True)
    user_expire = models.DateTimeField(max_length=50, null=True)
    user_lname = models.CharField(max_length=50, verbose_name='Last Name', null = True)
    user_fname = models.CharField(max_length=50, verbose_name='First Name', null = True)
    user_mname = models.CharField(max_length=50, verbose_name='Middle Name', null = True)
    user_sname = models.CharField(max_length=50,  null=True, verbose_name='Suffix Name')
    user_mobile = models.BigIntegerField(null=True, verbose_name='Mobile Number')
    user_bday = models.DateField(null=True)
    user_file = models.FileField(upload_to=image_path, blank=True, null=True)
    user_dateupdated = models.DateTimeField(default=now)
    user_datecreated = models.DateTimeField(default=now)
    user_address = models.CharField(max_length=50, verbose_name='Address', null=True)
    user_agency = models.CharField(max_length=50, verbose_name='Agency', null=True)
    user_post = models.CharField(max_length=50, verbose_name='Educational', null=True)
    user_school = models.CharField(max_length=50, verbose_name='School Name', null=True)
    user_approver = models.CharField(max_length=50, verbose_name='Approver Name', null=True)
    user_lock_flag = models.IntegerField(null = True, default= 0)
    user_lock_time = models.DateTimeField(null=True)
    user_receipt = models.CharField(unique=True, max_length=15, verbose_name='Official Receipt Number', null=True)
    def image_tag(self):
        return mark_safe('<img src="/media/%s" width = "50" height="50" />'%(self.user_file))

    def __str__(self):
        return self.user_no

class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_no = models.CharField(unique=True, max_length=15, verbose_name='Event Number')
    event_title = models.CharField(max_length=200, verbose_name='Event Title')
    event_slot = models.IntegerField(null = True, default=0)
    event_join = models.IntegerField(null = True)
    event_reg_expire = models.DateField(null=True)
    event_associate = models.ForeignKey(Membership, on_delete=models.CASCADE)
    event_desc = models.CharField(max_length=200, verbose_name='Event Descriptions')
    event_time_start = models.CharField(max_length=20, verbose_name='Event Time Start')
    event_time_end = models.CharField(max_length=20, verbose_name='Event Time End')
    event_date = models.DateField()
    event_amount = models.IntegerField(null = True, default= 0)
    event_link = models.CharField(max_length=200, verbose_name='Zoom link', null=True)
    event_evaluate = models.CharField(max_length=200, verbose_name='Evaluate')
    event_category = models.CharField(max_length=200, verbose_name='Event Category')
    event_image = models.FileField(upload_to=event_image_path)
    event_speaker = models.CharField(max_length=200, verbose_name='Event Speaker')
    event_status = models.CharField(max_length=16, verbose_name='Status', default="PENDING")
    event_datecreated = models.DateTimeField(default=now)
    event_dateupdated = models.DateTimeField(default=now)

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width = "50" height="50" />'%(self.event_image))

    def __str__(self):
        return self.event_id

class register_event(models.Model):
    reg_event_id = models.AutoField(primary_key=True)
    reg_event_no = models.CharField(unique=True, max_length=15, verbose_name='Event Payment Number', null=True)
    reg_ecert_no = models.CharField(unique=True, max_length=15, verbose_name='Event eCertificate Number', null=True)
    reg_event_approver = models.CharField(max_length=200, verbose_name='Event Payment Approver', null=True)
    reg_ev_id = models.ForeignKey(Event, on_delete=models.CASCADE) #prev reg_event_id 
    reg_member_id = models.ForeignKey(Membership, on_delete=models.CASCADE)
    reg_payment_amount = models.IntegerField(null = True, default= 0)
    reg_proof_payment = models.FileField(upload_to = event_image_path, null = True)
    reg_pmode = models.CharField(max_length=16, verbose_name='Event Payment', null = True)
    reg_attendance = models.IntegerField(null = True, default= 0)
    reg_payment_status = models.CharField(max_length=16, verbose_name='Event Payment', default="PENDING")
    reg_payment_date = models.DateTimeField(default=now)

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width = "50" height="50" />'%(self.event_image))

    def __str__(self):
        return self.event_id

class Certificate(models.Model):
    cert_id = models.AutoField(primary_key=True)
    cert_no = models.CharField(max_length=200, verbose_name='Certificate Number')
    cert_status = models.CharField(max_length=16, verbose_name='Status', default="PENDING")
    cert_event = models.ForeignKey(Event, on_delete=models.CASCADE)
    cert_member = models.ForeignKey(Membership, on_delete=models.CASCADE)
    cert_datecreated = models.DateTimeField(default=now)
    cert_dateupdated = models.DateTimeField(default=now)

    def __str__(self):
        return self.cert_id