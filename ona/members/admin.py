from django.contrib import admin
from .models import Member, Sub, Payment

# Register your models here.
# admin.site.register(Member)

class MemberAdmin(admin.ModelAdmin):
    list_display = ("firstname", "lastname", "joined_date", "phone")
    
class SubAdmin(admin.ModelAdmin):
    list_display = ("sub_type", "sub_amount", "sub_status", "sub_date")

class PaymentAdmin(admin.ModelAdmin):
    list_display = ("pay_amount", "pay_refno", "pay_status", "pay_date")
    
admin.site.register(Member, MemberAdmin)
admin.site.register(Sub)
admin.site.register(Payment)

