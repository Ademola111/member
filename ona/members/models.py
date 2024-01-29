from django.db import models

# Create your models here.
class Member(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    phone = models.IntegerField(null=True)
    joined_date = models.DateField(null=True)
    email = models.CharField(max_length=225, null=True)
    password = models.CharField(max_length=225, null=True)
    pic = models.CharField(max_length=225, null=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class Sub(models.Model):
    sub_refno = models.CharField(max_length=100, null=True)
    sub_type = models.CharField(max_length=100, null=True)
    sub_amount = models.CharField(max_length=100, null=True)
    sub_status = models.CharField(max_length=30, default='pending')
    sub_memberId = models.ForeignKey(Member, on_delete=models.CASCADE)
    sub_date = models.DateField(null=True)
    
    def __str__(self):
        return f"{self.sub_type} {self.sub_amount} {self.sub_status} {self.sub_date}"

class Payment(models.Model):
    pay_refno = models.CharField(max_length=100, null=True)
    pay_amount = models.CharField(max_length=10, null=True)
    pay_date = models.DateField(null=True)
    pay_status = models.CharField(max_length=30, default='pending')
    pay_memberId = models.ForeignKey(Member, on_delete=models.CASCADE)
    pay_subId = models.ForeignKey(Sub, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.pay_amount} {self.pay_refno} {self.pay_status} {self.pay_date}"
    
    
    
    
    