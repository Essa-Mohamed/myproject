from django.http import HttpResponse
from django.utils import timezone
from decimal import Decimal
from .models import Customer, Payment

def do_get(request):
    # قراءة معلمة uid وتنظيفها
    uid = request.GET.get('uid', '').strip().replace('"', '')
    if not uid:
        return HttpResponse('Missing_UID', content_type="text/plain")
    
    try:
        customer = Customer.objects.get(uid=uid)
    except Customer.DoesNotExist:
        return HttpResponse('Not_Registered', content_type="text/plain")
    
    fare = Decimal('5')
    new_balance = customer.balance - fare

    if new_balance < 0:
        return HttpResponse('Insufficient_Balance', content_type="text/plain")
    
    # تحديث رصيد العميل
    customer.balance = new_balance
    customer.save()
    
    # الحصول على التاريخ والوقت الحالي بصيغة dd/mm/yyyy و HH:mm:ss
    now = timezone.localtime()  # تأكد أن إعدادات التوقيت في settings.py تناسب توقيتك
    date_str = now.strftime('%d/%m/%Y')
    time_str = now.strftime('%H:%M:%S')
    
    # تسجيل العملية
    Payment.objects.create(
        customer=customer,
        fare=fare,
        new_balance=new_balance,
        date=date_str,
        time=time_str
    )
    
    return HttpResponse('OK', content_type="text/plain")
