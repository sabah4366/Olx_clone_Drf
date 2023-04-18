from django.db import models
from user.models import CustomUser
from django.utils import timezone

class Category(models.Model):
    #for product category
    category_name=models.CharField(max_length=200)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.category_name

   
class Products(models.Model):
    #for products

    CONDITION_TYPE=(
        ('Used','Used'),
        ('New',('New'))
    )

    OPTIONAL=(
        ('for-sale','for-sale'),
        ('exchnage','exchnage'),
        ('sold','sold')

    )
    name=models.CharField(max_length=200)
    owner=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='forowner')
    brand=models.CharField(max_length=200,blank=True,null=True)
    description=models.TextField(max_length=500)
    price=models.FloatField()
    category=models.ForeignKey(Category,null=False,blank=False,on_delete=models.CASCADE)
    state=models.CharField(max_length=200)
    city=models.CharField(max_length=150)
    condition=models.CharField(max_length=200,choices=CONDITION_TYPE)
    image_1=models.ImageField(upload_to='main_product',blank=False,null=False)
    status=models.CharField(max_length=200,choices=OPTIONAL,default='for-sale')
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)

    def two_month_register(self):
        two_month=timezone.now()-timezone.timedelta(days=60)
        if self.created == None:
            return False
        return self.created < two_month

    
    
    def save(self,*args,**kwargs):
        
        
        if self.two_month_register():
            self.is_active=False
        return super(Products,self).save(*args,**kwargs)

    
    class Meta:
        ordering=['-created']


    def __str__(self) -> str:
        return self.name

class Inquiry(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    message=models.TextField(blank=False,null=False)
    created_at=models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return self.message
