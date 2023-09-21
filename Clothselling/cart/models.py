from django.db import models
from admin_auth.models import *

# Create your models here.


class Cart(models.Model):
    
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank=True,null=True)
    products=models.ForeignKey(ProductVariant,on_delete=models.SET_NULL,null=True)
    quantity=models.PositiveBigIntegerField(default=0)
    created_date=models.DateField(default=timezone.now)

    

