from django.forms import ModelForm
from .models import Member

class PostMember(ModelForm):
    class Meta:
        model = Member
        fields = ['firstname','lastname', 'phone', 'password', 'email' ]