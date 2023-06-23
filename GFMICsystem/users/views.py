from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponse
from .models import Membership, Event, register_event, Certificate
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from datetime import datetime, date, timedelta
import random
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
import base64
from django.db.models import Q
import json
from cryptography.fernet import Fernet
import bcrypt



today = datetime.today()
# key = Fernet.generate_key()


def home(request):
    request.session['session_user_id'] = None
    request.session['session_user_sub'] = None
    request.session['session_user_status'] = None
    request.session['session_fname'] = None
    request.session['seesion_lname'] = None
    return render(request, 'home.html')

def login(request):
    request.session['session_user_id'] = None
    request.session['session_user_sub'] = None
    request.session['session_user_status'] = None
    request.session['session_fname'] = None
    request.session['seesion_lname'] = None
    return render(request, 'login.html')

def logout(request):
    request.session['session_user_id'] = None
    request.session['session_user_sub'] = None
    request.session['session_user_status'] = None
    request.session['session_fname'] = None
    request.session['seesion_lname'] = None
    return render(request, 'login.html')

def forgot_pass(request):
    return render(request, 'forgot_password.html')

def error_404(request):
    return render(request, '404.html')

def about(request):
    return render(request, 'about.html')

def home_event(request):
    return render(request, 'home_event.html')

def membership_conference(request):
    return render(request, 'membership-conference.html')

def national_convention(request):
    return render(request, 'national-convention.html')

def webinar(request):
    return render(request, 'webinar.html')

def faqs(request):
    return render(request, 'faqs.html')

def help_desk(request):
    return render(request, 'help-desk.html')

def ecert(request):
    return render(request, 'ecert.html')

def generator(request):
    return render(request, 'generator.html')

def process_login(request):
    # f = Fernet(key)
    today = datetime.today()
    email = request.POST.get('useremail')
    password = request.POST.get('password')
    # password = password.encode()
    try:
        m = Membership.objects.get(user_email=email)
        # password_e = m.user_password.split("'")[1]
        # password_e = password_e.encode('utf-8')
        # decoded = f.decrypt(password_e, 720*60*60)
        if m.user_bday is not None:
            m_bday = m.user_bday.strftime("%Y-%m-%d %H:%M:%S")
        else:
            m_bday = ''
        if m.user_password == password:
            if m.user_lock_flag == 2:
                if m.user_lock_time is not None:
                    db = str(m.user_lock_time)
                    new_dt = db[:19]
                    now = str(today)
                    new_dt2 = now[:19]
                    b = datetime.strptime(new_dt, "%Y-%m-%d %H:%M:%S")
                    a = datetime.strptime(new_dt2, "%Y-%m-%d %H:%M:%S")
                    # print(b, a)
                    if b <= a:
                        try:
                            request.session['session_user_id'] = m.user_id
                            request.session['session_user_sub'] = m.user_sub
                            request.session['session_user_status'] = m.user_status
                            request.session['session_fname'] = m.user_fname
                            request.session['session_lname'] = m.user_lname
                            request.session['session_user_bday'] = m_bday
                            request.session['session_user_file'] = json.dumps(str(m.user_file))
                            
                            m.user_lock_time = None
                            m.user_lock_flag = 0
                            m.save()
                            
                            return HttpResponseRedirect('/dashboard', {'member': m})
                        except ObjectDoesNotExist:
                            return render(request, 'login.html', {
                                'error_message': 'Either email or password are incorrect'
                            })
                    else:
                       
                        remaining_time = b - a
                        # print(remaining_time)
                        return render(request, 'login.html', {
                            'error_message': f'Remaining time: {remaining_time}'
                        })
                else:
                    now = today + timedelta(hours = 9)
                    m.user_lock_time = datetime.strftime(now, "%Y-%m-%d %H:%M:%S")
                    # print(today, m.user_lock_time)
                    m.save()
                    return render(request, 'login.html', {
                        'error_message': 'Error! Account Locked!'
                    })
            else:
                m.user_lock_flag = 0
                m.save()
                try:
                    request.session['session_user_id'] = m.user_id
                    request.session['session_user_sub'] = m.user_sub
                    request.session['session_user_status'] = m.user_status
                    request.session['session_fname'] = m.user_fname
                    request.session['session_lname'] = m.user_lname
                    request.session['session_user_bday'] = m_bday
                    request.session['session_user_file'] = json.dumps(str(m.user_file))
                    
                    m.user_lock_time = None
                    m.user_lock_flag = 0
                    m.save()

                    return HttpResponseRedirect('/dashboard', {'member': m})
                except ObjectDoesNotExist:
                    return render(request, 'login.html', {
                        'error_message': 'Either email or password are incorrect'
                    })
        else:
            if m.user_lock_flag == 2:
                if m.user_lock_time is not None:
                    db = str(m.user_lock_time)
                    new_dt = db[:19]
                    now = str(today)
                    new_dt2 = now[:19]
                    b = datetime.strptime(new_dt, "%Y-%m-%d %H:%M:%S")
                    a = datetime.strptime(new_dt2, "%Y-%m-%d %H:%M:%S")
                    if b <= a:
                        try:
                            request.session['session_user_id'] = m.user_id
                            request.session['session_user_sub'] = m.user_sub
                            request.session['session_user_status'] = m.user_status
                            request.session['session_fname'] = m.user_fname
                            request.session['session_lname'] = m.user_lname
                            request.session['session_user_bday'] = m_bday
                            request.session['session_user_file'] = json.dumps(str(m.user_file))
                            
                            m.user_lock_time = None
                            m.user_lock_flag = 0
                            m.save()

                            return HttpResponseRedirect('/dashboard', {'member': m})
                        except ObjectDoesNotExist:
                            return render(request, 'login.html', {
                                'error_message': 'Either email or password are incorrect '
                            })
                    else:
                        remaining_time = b - a
                        # print(remaining_time)
                        return render(request, 'login.html', {
                            'error_message': f'Remaining time: {remaining_time}'
                        })
                else:
                    now = today + timedelta(hours = 9)
                    m.user_lock_time = datetime.strftime(now, "%Y-%m-%d %H:%M:%S")
                    # print(today ,m.user_lock_time)
                    m.save()
                    return render(request, 'login.html', {
                        'error_message': 'Error! Account Locked!'
                    })
            else:
                m.user_lock_flag = m.user_lock_flag + 1
                m.save()
                return render(request, 'login.html', {
                    'error_message': 'Either email or password are incorrect '
                })
    except ObjectDoesNotExist:
        return render(request, 'login.html', {
            'error_message': 'Either email or password are incorrect '
        })
   
    
def dashboard(request):
    try:
        if request.session['session_user_id']:
            m = Membership.objects.get(user_id=request.session['session_user_id'])
            request.session['session_user_sub'] = m.user_sub
            return render(request, 'dashboard.html')
    except:
        return render(request, '404.html')
    

def upload_profile(request):
    user_id = request.POST.get('userid')
    return render(request, 'dashboard.html')

def profile(request):
    user_id = request.POST.get('user_id')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    middle_name = request.POST.get('middle_name')
    contact = request.POST.get('contact')
    bday = request.POST.get('bday')
    address = request.POST.get('address')
    agency = request.POST.get('agency')
    college = request.POST.get('college')
    post_grad = request.POST.get('post_grad')
    date_updated = datetime.now()
    try:
        m = Membership.objects.get(user_id=user_id)
        m.user_fname = first_name
        m.user_mname = middle_name
        m.user_lname = last_name
        m.user_mobile = contact
        m.user_bday = bday
        m.user_address = address
        m.user_agency = agency
        m.user_post = post_grad
        m.user_school = college
        m.user_dateupdated = date_updated
        m.save()
        request.session['session_fname'] = m.user_fname
        request.session['seesion_lname'] = m.user_lname
        request.session['session_user_bday'] = m.user_bday
        data = {'success':True}
        # print(bday)
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)
    
def view_profile(request):
    user_id = request.POST.get('user_id')
    try:
        u = Membership.objects.get(user_id = user_id)
        
        data = {
            'user_id': u.user_id,
            'user_fname': u.user_fname,
            'user_mname':u.user_mname,
            'user_lname': u.user_lname,
            'user_mobile': u.user_mobile,
            'user_bday': u.user_bday,
            'user_address': u.user_address,
            'user_agency': u.user_agency,
            'user_school': u.user_school,
            'user_post': u.user_post,
        }
     
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)
    
def register(request):
    return render(request, 'register.html')

def register_account(request):
    # f = Fernet(key)
    
    email = request.POST.get('useremail')
    password = request.POST.get('password')
    lname = request.POST.get('lname')
    fname = request.POST.get('fname')
    mname = request.POST.get('mname')
    mobile = request.POST.get('mobile')
    # token = password.encode('utf-8')
    # token = f.encrypt(token)

    # hashed = bcrypt.hashpw(password_e, salt)
    # print(token)
    # print(type(hashed))
    # token = f.encrypt(bytes(a, encoding="ascii"))
 
    password1 = request.POST.get('password1')
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    randomstr =''.join((random.choice(chars)) for x in range(5))
    user_no = 'MN-' + randomstr
    if email != None or password != None or password1 != None:
        if password == password1:
            try:
                m = Membership.objects.get(user_email=email)
                return render(request, 'register.html', {
                    'error_message': 'Duplicated email :' + email
                })
            except ObjectDoesNotExist:
                m = Membership.objects.create(
                    user_email=email, 
                    user_password=password, 
                    user_no=user_no,
                    user_lname=lname,
                    user_fname=fname,
                    user_mname=mname,
                    user_mobile=mobile
                    )
                m.save()
                return HttpResponseRedirect('/login')
        else:
            return render(request, 'register.html', {
                'error_message': 'Password does not match.' 
            })
    else:
        return render(request, 'register.html', {
            'error_message': 'Please fill up the required fields.'
        })
        

def membership(request):
    try:
        if request.session['session_user_sub'] == 'ADMIN':
            member_list = Membership.objects.filter(~Q(user_sub='ADMIN')).order_by('-user_dateupdated')
            context = {'member_list': member_list}
            return render(request, 'membership.html', context)
        else:
            member_list = Membership.objects.filter(~Q(user_sub='ASSOCIATE')).order_by('-user_dateupdated')
            context = {'member_list': member_list}
            return render(request, 'membership.html', context)
    except ObjectDoesNotExist:
        return render(request, 'membership.html')

def add_membership(request):
    m_no = request.POST.get('m_no')
    m_name = request.POST.get('m_name')
    m_mobile = request.POST.get('m_mobile')
    m_satus = request.POST.get('m_satus')
    m_sub = request.POST.get('m_sub')
    email = request.POST.get('email')
    pass1 = request.POST.get('pass')
    try:
        c = Membership.objects.get(user_email=email)
        data = {'error': True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        member = Membership(
            user_no=m_no,
            user_email=email,
            user_password=pass1,
            user_sub=m_sub,
            user_status = m_satus,
            user_fname = m_name,
            user_mobile = m_mobile
        )
        member.save()
        data = {'success': True}
        return JsonResponse(data, safe=False)

# def edit_account(request):
#     acc_id = request.POST.get('acc_id') 
#     account_sub = request.POST.get('account_sub')
#     try:
#         c = Account.objects.get(account_id=acc_id)
#         c.account_subscription = account_sub
#         c.account_dateupdated = today
#         c.save()
#         data = {'success': True}
#         return JsonResponse(data, safe=False)
#     except ObjectDoesNotExist:
#         data = {'error': True}
#         return JsonResponse(data, safe=False)

def view_membership(request):
    user_id = request.POST.get('user_id')
    # print(user_id)
    try:
        a = Membership.objects.get(user_id=user_id)
        data = {
            'member_proof': str(a.user_file),
            'membership_no':a.user_no,
            'payment_amount':a.user_amount,
            'mode_of_payment':a.user_pmode,
            'm_start':a.user_validity,
            'm_end':a.user_expire,
            'm_status':a.user_status,
        }
        # print(a.user_expire)
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

# def delete_account(request):
#     acc_id = request.POST.get('acc_id') 
#     try:
#         c = Account.objects.get(account_id=acc_id)
#         if c.account_status == 'ACTIVE':
#             c.account_status = 'INACTIVE'
#         else:
#             c.account_status = 'ACTIVE'
#             c.account_dateupdated = today
#         c.account_dateupdated = today
#         c.save()
#         data = {'success': True}
#         return JsonResponse(data, safe=False)
#     except ObjectDoesNotExist:
#         data = {'error': True}
#         return JsonResponse(data, safe=False)
   
def payment(request):
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    randomstr =''.join((random.choice(chars)) for x in range(5))
    receipt_no = 'MR-' + randomstr
    userid = request.POST.get('payment_id')
    img = request.FILES.get("file")
    mode_of_payment = request.POST.get('mode_of_payment')
    m_start = request.POST.get('m_start')
    if m_start:
       
        # m_start = m_start + ' ' + '00:00:00'
        mstart = datetime.strptime(m_start, "%m/%d/%Y")
        # mstart = datetime.strptime(m_start, "%d/%m/%Y").strftime('%Y-%m-%d %H:%M:%S')
    
        # m_start = datetime.strftime(m_start, "%Y-%m-%d %H:%M:%S")
    
        # m_start = datetime.strptime(m_start, "YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]")
        
        m_end = request.POST.get('m_end')
        mend = datetime.strptime(m_end, "%m/%d/%Y")
        # mend = datetime.strptime(m_start, "%d/%m/%Y").strftime('%Y-%m-%d %H:%M:%S')
        # print(m_start, m_end)
    payment_amount = request.POST.get('payment_amount')
  
    try: 
        m = Membership.objects.get(user_id=userid)
        m.user_amount = payment_amount
        m.user_pmode = mode_of_payment
        m.user_validity = mstart
        m.user_expire = mend
        m.user_file = img
        m.user_receipt = receipt_no
        m.save()
        request.session['session_user_sub'] = m.user_sub
        return HttpResponseRedirect('dashboard')
    except ObjectDoesNotExist:
        return HttpResponseRedirect('dashboard', {
            'error_message': 'failed'
        })

def approve_membership(request):
    userid = request.POST.get('user_id')
    approver_id = request.POST.get('approver_id')
    # print(approver_id, userid)
    try: 
        m = Membership.objects.get(user_id=userid)
        m.user_sub = 'PREMIUM'
        a = Membership.objects.get(user_id = approver_id)
        s = a.user_fname + ' ' + a.user_lname
        # print(s)
        m.user_approver = s
        # print(str(a.user_fname + ' ' + a.user_lname ))
        m.save()
        data = {'success': True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error': True}
        return JsonResponse(data, safe=False)
    
def approve_associate(request):
    userid = request.POST.get('user_id')
    # print(userid)
    try: 
        m = Membership.objects.get(user_id=userid)
        m.user_sub = 'ASSOCIATE'
        m.save()
        data = {'success': True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error': True}
        return JsonResponse(data, safe=False)

def disapprove_membership(request):
    userid = request.POST.get('user_id')
    try: 
        m = Membership.objects.get(user_id=userid)
        m.user_pmode = None
        # print(m.user_pmode)
        m.user_amount = None
        m.user_validity = None
        m.user_expire = None
        m.user_file = None
        
        m.save()
        data = {'success': True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error': True}
        return JsonResponse(data, safe=False)

def info(request):
    try:
        account_list = Account.objects.order_by('account_id')
        context = {'account_list': account_list}
        return render(request, 'info.html', context)
    except ObjectDoesNotExist:
        return render(request, 'info.html')

def events(request):
    event_list = Event.objects.order_by('-event_datecreated')
    # context = {'event_list': event_list}
    event_list_status = register_event.objects.values()
    # context2 = {'event_list_status':event_list_status}
    return render(request, 'events.html', {'event_list': event_list, 'event_list_status':event_list_status})

def event(request):
    try:
        event_list = Event.objects.order_by('-event_datecreated')
        context = {'event_list': event_list}
        return render(request, 'event.html', context)
    except ObjectDoesNotExist:
        return render(request, 'event.html')

def add_event(request):
    associate_id = request.POST.get('user_id')
    event_title = request.POST.get('event_title')
    event_slot = request.POST.get('event_slot')
    event_e_date = request.POST.get('event_e_date')
    sched_time_start = request.POST.get('sched_time_start')
    sched_time_end = request.POST.get('sched_time_end')
    sched_date = request.POST.get('sched_date')
    event_amount = request.POST.get('event_amount')
    event_link = request.POST.get('event_link')
    # print(sched_date)
    event_desc = request.POST.get('event_desc')
    event_speaker = request.POST.get('event_speaker')
    event_category = request.POST.get('event_category')
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    randomstr =''.join((random.choice(chars)) for x in range(5))
    event_no = 'EN-' + randomstr
    # sched_date = datetime.strptime(sched_date, '%m-%d-%Y' )
    try:
        # print(event_title, associate_id, event_title, sched_time, sched_date, event_desc, event_speaker, event_category)
        e = Event.objects.create(
            event_no = event_no,
            event_title = event_title,
            event_slot = event_slot,
            event_reg_expire = event_e_date,
            event_associate = Membership.objects.get(user_id = associate_id),
            event_date = sched_date,
            event_time_start = str(sched_time_start), 
            event_time_end = str(sched_time_end), 
            event_amount = event_amount,
            event_link = event_link,
            event_desc = event_desc,
            event_category = event_category,
            event_speaker = event_speaker
        )
        e.save()
        data = {'success': True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error': True}
        return JsonResponse(data, safe=False)

def add_event_picture(request):
    event_id = request.POST.get('event_id')
    event_img = request.FILES.get("event_file")
    try:
        e = Event.objects.get(event_id = event_id)
        e.event_image = event_img
        e.save()
        return HttpResponseRedirect('event/')
    except ObjectDoesNotExist:
        return HttpResponseRedirect('event/', {
            'error_message': 'failed'
        })

def view_event(request):
    e_id = request.POST.get('e_id')
    user_id = request.POST.get('user_id')
    # print(e_id, user_id)
    try:
        e = Event.objects.get(event_id = e_id)
        if e.event_join == e.event_slot:
            avail = 1
        else:
            avail = 0

        now = date.today()
        if e.event_reg_expire < now:
            expire = 1
        else:
            expire = 0
       
        try:
            r = register_event.objects.get(reg_ev_id = Event.objects.get(event_id=e_id), reg_member_id = Membership.objects.get(user_id = user_id))
            joined = 1
            status = r.reg_payment_status
            data = {
                'event_id': e.event_id,
                'event_title': e.event_title,
                'event_desc': e.event_desc,
                'event_time_start': e.event_time_start,
                'event_time_end': e.event_time_end,
                'event_date': e.event_date,
                'event_speaker': e.event_speaker,
                'event_amount': e.event_amount,
                'event_link': e.event_link,
                'status':status,
                'event_reg_expire':e.event_reg_expire,
                'flag':joined,
                'slot_avail':avail,
                'expire':expire
            }
            # print(status)
        except ObjectDoesNotExist:
            joined = 0
            data = {
                'event_id': e.event_id,
                'event_title': e.event_title,
                'event_desc': e.event_desc,
                'event_time_start': e.event_time_start,
                'event_time_end': e.event_time_end,
                'event_date': e.event_date,
                'event_speaker': e.event_speaker,
                'event_amount': e.event_amount,
                'event_link': e.event_link,
                'event_reg_expire':e.event_reg_expire,
                'flag':joined,
                'slot_avail':avail,
                'expire':expire
            }
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)
    
def event_admin_view(request):
    e_id = request.POST.get('e_id')
    try:
        
        event_student = list(register_event.objects.all().filter(reg_ev_id = Event.objects.get(event_id=e_id)).values())
        return JsonResponse({'data': event_student})
    except ObjectDoesNotExist:
        data = {'error':"error"}
        return JsonResponse(data, safe=False)
    
def member_view_data(request):
    event_id = request.POST.get('event_id')
    member_id = request.POST.get('member_id')
    # print(event_id, member_id)
    try:
       
        e = Membership.objects.get(user_id = member_id)
        r = register_event.objects.get(reg_ev_id = Event.objects.get(event_id=event_id), reg_member_id = Membership.objects.get(user_id = member_id))
        # print(r.reg_attendance)
        if r.reg_attendance == 0:
            stat = 'Registered'
        else:
            stat = 'Attended'
        data = {
            'user_number':e.user_no,
            'user_name': e.user_fname + ' ' + e.user_lname,
            'user_contact': e.user_mobile,
            'user_email': e.user_email,
            'status': stat
        }
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        pass

def event_view_data(request):
    e_id = request.POST.get('event_id')
    try:
        e = Event.objects.get(event_id = e_id)
        data = {
            'event_title': e.event_title,
            'event_desc': e.event_desc,
            'event_time_start': e.event_time_start,
            'event_time_end': e.event_time_end,
            'event_date': e.event_date,
            'event_speaker': e.event_speaker,
        }
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}

def view_or(request):
    user_id = request.POST.get('user_id')
    try:
        e = Membership.objects.get(user_id = user_id)
        data = {
            'user_no': e.user_no,
            'user_name': e.user_lname + ', ' + e.user_fname + ' ' + e.user_mname,
            'user_amount': e.user_amount,
            'user_approver': str(e.user_approver),
        }
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)
    
def join_event_payment_proof(request):
    userid = request.POST.get('payment_id')
    img = request.FILES.get("file")
    mode_of_payment = request.POST.get('mode_of_payment')
    m_start = request.POST.get('m_start')
    if m_start:
       
        # m_start = m_start + ' ' + '00:00:00'
        mstart = datetime.strptime(m_start, "%m/%d/%Y")
        # mstart = datetime.strptime(m_start, "%d/%m/%Y").strftime('%Y-%m-%d %H:%M:%S')
    
        # m_start = datetime.strftime(m_start, "%Y-%m-%d %H:%M:%S")
    
        # m_start = datetime.strptime(m_start, "YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]")
        
        m_end = request.POST.get('m_end')
        mend = datetime.strptime(m_start, "%m/%d/%Y")
        # mend = datetime.strptime(m_start, "%d/%m/%Y").strftime('%Y-%m-%d %H:%M:%S')
        # print(m_start, m_end)
    payment_amount = request.POST.get('payment_amount')
  
    try: 
        m = Membership.objects.get(user_id=userid)
        m.user_amount = payment_amount
        m.user_pmode = mode_of_payment
        m.user_validity = mstart
        m.user_expire = mend
        m.user_file = img
        m.save()
        request.session['session_user_sub'] = m.user_sub
        return HttpResponseRedirect('dashboard')
    except ObjectDoesNotExist:
        return HttpResponseRedirect('dashboard', {
            'error_message': 'failed'
        })

def join_event_payment(request):
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    randomstr =''.join((random.choice(chars)) for x in range(5))
    event_payment_no = 'EP-' + randomstr
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    randomstr =''.join((random.choice(chars)) for x in range(5))
    event_ecert_no = 'EC-' + randomstr
    ev_id = request.POST.get('ev_id')
    ev_id = ev_id.replace(' ', '')
    m_id = request.POST.get('member_id')
    m_id = m_id.replace(' ', '')
    img = request.FILES.get("file")
    mode_of_payment = request.POST.get('mode_of_payment')
    payment_amount = request.POST.get('pay_amount')
    
    try:
        e = register_event.objects.get(reg_ev_id = Event.objects.get(event_id=ev_id), reg_member_id = Membership.objects.get(user_id = m_id))
        e.reg_payment_status = 'PENDING'
        e.reg_pmode = mode_of_payment
        e.reg_proof_payment = img
        e.save()
        return HttpResponseRedirect('/events')
    except ObjectDoesNotExist:
        try: 
            a = Event.objects.get(event_id=ev_id)
            if a.event_join is None:
                a.event_join = 1
            else:
                a.event_join = a.event_join + 1
            a.save()
            # print(ev_id, m_id)
            e = register_event.objects.create(
            reg_event_no = event_payment_no,
            reg_ecert_no = event_ecert_no,
            reg_ev_id = Event.objects.get(event_id=ev_id),
            reg_member_id = Membership.objects.get(user_id = m_id),
            reg_payment_amount = payment_amount,
            reg_pmode = mode_of_payment,
            reg_proof_payment = img,
            )
            e.save()
            return HttpResponseRedirect('/events')
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/events')
        
def event_zoomlink_flag(request):
    event_id = request.POST.get('event_id')
    user_id = request.POST.get('user_id')
    try:
        e = register_event.objects.get(reg_ev_id = Event.objects.get(event_id=event_id), reg_member_id = Membership.objects.get(user_id = user_id))
        e.reg_attendance = 1
        e.save()
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)
    
def event_payment(request):
    try:
        event_payment_list = register_event.objects.order_by('-reg_payment_status')
        context = {'event_payment_list': event_payment_list}
        return render(request, 'event_payment.html', context)
    except ObjectDoesNotExist:
        return render(request, 'event_payment.html')
    
def view_payment(request):
    # reg_id = request.POST.get('reg_id')
    member_id = request.POST.get('member_id')
    event_id = request.POST.get('event_id')
    # print(member_id, event_id)
    try:
        # a = register_event.objects.get(reg_ev_id = reg_id )
        a = register_event.objects.get( reg_ev_id = Event.objects.get(event_id = event_id) , reg_member_id = Membership.objects.get(user_id=member_id))

        b = a.reg_payment_date.strftime("%b-%d-%Y %H:%M:%S")
        # print(b)
        new_dt = b[:11]
        # print(new_dt,)

        data = {
            'reg_proof_payment': str(a.reg_proof_payment),
            'reg_event_no':a.reg_event_no,
            'reg_ecert_no':a.reg_ecert_no,
            'reg_payment_amount':a.reg_payment_amount,
            'reg_pmode':a.reg_pmode,
            'reg_payment_status':a.reg_payment_status,
            'reg_name':a.reg_member_id.user_fname + ' ' + a.reg_member_id.user_lname,
            'reg_event_creator': a.reg_ev_id.event_associate.user_fname + ' ' + a.reg_ev_id.event_associate.user_lname,
            'reg_date':new_dt,
            'e_title':a.reg_ev_id.event_title,
            'e_desc':a.reg_ev_id.event_desc,
            'e_date':a.reg_ev_id.event_date,
        }
        # print(a.reg_ev_id.event_associate.user_lname)
        # print(a.reg_member_id.user_fname, a.reg_member_id.user_lname)
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)
    
def event_payment_approve(request):
    member_id = request.POST.get('member_id')
    event_id = request.POST.get('event_id')
    approver_id = request.POST.get('approver_id')
    try: 
        m = register_event.objects.get( reg_ev_id = Event.objects.get(event_id = event_id) , reg_member_id = Membership.objects.get(user_id=member_id))
        m.reg_payment_status = 'APPROVED'
        a = Membership.objects.get(user_id = approver_id)
        m.reg_event_approver = str(a.user_fname + ' ' + a.user_lname + ' ' + '(' + a.user_sub + ')')
        m.save()
        data = {'success': True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error': True}
        return JsonResponse(data, safe=False)
    
def event_payment_denied(request):
    member_id = request.POST.get('member_id')
    event_id = request.POST.get('event_id')
    approver_id = request.POST.get('approver_id')
    try: 
        m = register_event.objects.get( reg_ev_id = Event.objects.get(event_id = event_id) , reg_member_id = Membership.objects.get(user_id=member_id))
        m.reg_payment_status = 'DENIED'
        a = Membership.objects.get(user_id = approver_id)
        m.reg_event_approver = str(a.user_fname + ' ' + a.user_lname + ' ' + '(' + a.user_sub + ')')
        m.save()
        data = {'success': True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error': True}
        return JsonResponse(data, safe=False)

def add_event_picture(request):
    event_id = request.POST.get('event_id')
    event_img = request.FILES.get("event_file")
    try:
        e = Event.objects.get(event_id = event_id)
        e.event_image = event_img
        e.save()
        return HttpResponseRedirect('event/')
    except ObjectDoesNotExist:
        return HttpResponseRedirect('event/', {
            'error_message': 'failed'
        })
# Event Approve
def approve_event(request):
    event_id = request.POST.get('event_id')
    # print(event_id)
    try: 
        m = Event.objects.get(event_id=event_id)
        m.event_status = 'ON GOING'
        m.save()
        data = {'success': True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error': True}
        return JsonResponse(data, safe=False)
# Event Reject
def disapprove_event(request):
    event_id = request.POST.get('event_id')
    # print(event_id)
    try: 
        m = Event.objects.get(event_id=event_id)
        m.event_status = 'DENIED'
        m.save()
        data = {'success': True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error': True}
        return JsonResponse(data, safe=False)
# Event Delete
def delete_event(request):
    event_id = request.POST.get('event_id')
    # print(event_id)
    try: 
        m = Event.objects.get(event_id=event_id)
        m.event_status = 'DELETED'
        m.save()
        data = {'success': True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error': True}
        return JsonResponse(data, safe=False)
# dating view sa event approve, reject, and delete
def event_remove(request):
    event_id = request.POST.get('event_id')
    event_choice =  request.POST.get('status')
    try:
        e = Event.objects.get(event_id = event_id)
        if event_choice == 'approve':
            e.event_status = 'ON GOING'
            e.save()
        elif event_choice == 'remove':
            e.delete()

        data = {'success':True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error': True}
        return JsonResponse(data, safe=False)
    
    # m_start = request.POST.get('m_start')
    # m_start = m_start + ' ' + '00:00:00'
    # mstart = datetime. strptime(m_start, '%m/%d/%Y %H:%M:%S')
    # m_end = request.POST.get('m_end')
    # m_end = m_end + ' ' + '00:00:00'
    # estart = datetime. strptime(m_end, '%m/%d/%Y %H:%M:%S')
    # payment_amount = request.POST.get('payment_amount')

def OR(request):
    member_list = Membership.objects.order_by('-user_dateupdated')
    context = {'member_list': member_list}
    return render(request, 'or.html', context)

def member_gen_receipt(request):
    user_id = request.POST.get('member_id')

    try:
        e = Membership.objects.get(user_id = user_id)
        # db = str(e.user_validity)
        # new_dt = db[:10]
        # db2 = str(e.user_expire)
        # new_dt2 = db2[:10]
        # b = datetime.strptime(new_dt, "%m-%d-%Y")
        # a = datetime.strptime(new_dt2, "%m-%d-%Y")
        # b = datetime.strptime(new_dt, "%Y-%m-%d")
        # a = datetime.strptime(new_dt2, "%Y-%m-%d")

        b = e.user_validity.strftime("%b-%d-%Y %H:%M:%S")
        a = e.user_expire.strftime("%b-%d-%Y %H:%M:%S")
        # print(b,a)
        new_dt = b[:11]
        new_dt2 = a[:11]
        # print(new_dt, new_dt2)

        # print(new_dt, new_dt2)
        # print(b,a)
        
        data = {
            'user_id': e.user_id,
            'user_no': e.user_no,
            'user_sub': e.user_sub,
            'user_amount': e.user_amount,
            'user_validity': new_dt,
            'user_expire': new_dt2,
            'user_name': e.user_fname + ' ' + e.user_lname,
            'user_approver': e.user_approver,
            'user_receipt_no': e.user_receipt,
        }
        # print(e.user_fname + ' ' + e.user_lname)
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def add_ecert(request):
    cert_no = request.POST.get('cert_no')
    cert_status = request.POST.get('cert_status')
    cert_member_id = request.POST.get('cert_member_id')
    cert_event_id = request.POST.get('cert_event_id')
    try:
        e = Certificate.objects.create(
            event_no = cert_no,
            event_title = cert_status,
            event_member = Membership.objects.get(user_id = cert_member_id),
            event_event = Event.objects.get(event_id = cert_event_id)
        )
        e.save()
        data = {'success': True}
        return JsonResponse(data, safe=False)

    except ObjectDoesNotExist:
        data = {'error': True}
        return JsonResponse(data, safe=False)

