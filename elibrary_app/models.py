##from turtle import mode
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    def  __str__(self):
        return self.name

class Book(models.Model):
    book_status = [
        ('avaliable' ,'avaliable' ),
         ('rental' ,'rental' ),
          ('sold' ,'sold' )
    ]

    title = models.CharField(max_length=250)
    author = models.CharField(max_length=250, null=True, blank=True)
    photo_book = models.ImageField(upload_to='photos', null=True, blank=True)
    photo_author = models.ImageField(upload_to='photos', null=True, blank=True)
    pages = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=5 , decimal_places=2, null=True, blank=True)
    rental_price_day = models.DecimalField(max_digits=5 , decimal_places=2, null=True, blank=True)
    rental_period = models.IntegerField(null=True, blank=True)
    total_rental = models.DecimalField(max_digits=5 , decimal_places=2, null=True, blank=True)
    active = models.BooleanField(default=True)
    state = models.CharField(max_length=50, choices=book_status, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete = models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.title

class Massage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)  # take snapshote everytime we save item
    created = models.DateTimeField(auto_now_add=True)  # take just for the first time we create item

    def __str__(self):
        return self.body[0:50]   

        
          

    
  

