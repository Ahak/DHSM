from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICE=[
        ('admin' ,'admin'),
        ('seller','seller'),
        ('buyer' ,'buyer'),
    ]
    image = models.ImageField(upload_to='upload/user', null=True, blank=True)
    phone=models.CharField(max_length=14)
    role = models.CharField(max_length=13 ,choices=ROLE_CHOICE, default='buyer')

    def __str__(self):
        return self.username
    

class Property(models.Model):
    CHOICE_STATUS= [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Sold', 'Sold'),
    ]
    title =models.CharField(max_length=50)
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=15, default=0)
    room = models.IntegerField()
    bathroom =models.IntegerField()
    location =models.CharField(max_length=50)
    image1= models.ImageField(upload_to='upload/property')
    image2= models.ImageField(upload_to='upload/property')
    image3= models.ImageField(upload_to='upload/property')
    image4= models.ImageField(upload_to='upload/property')
    description =models.CharField(max_length=250)
    status =models.CharField(choices=CHOICE_STATUS, max_length=12, default='Pending')
    date = models.DateTimeField(default=datetime.datetime.today)

    def __str__(self):
        return f'{self.title} - {self.seller.username}'
    
class Payment(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    date = models.DateTimeField(default=datetime.datetime.today)

    def __str__(self):
        return f'Payment of {self.amount} by {self.buyer.username} for {self.property.title}'
