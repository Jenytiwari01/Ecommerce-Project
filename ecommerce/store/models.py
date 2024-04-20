from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name=models.CharField(max_length=200, null=True)
    email=models.CharField(max_length=200)

    def __str__(self):
        return self.name if self.name else "Unnamed Customer"

    

class Product(models.Model):
        name=models.CharField(max_length=200)
        price=models.DecimalField(max_digits=7,decimal_places=2)
        digital=models.BooleanField(default=False,null=True,blank=True)#if false its a physicall product needed to be deliverd or shipped
        image = models.ImageField(null=True, blank=True)
        #yespachi matra media root define garmne ho
        #mediaroot le panel bata haleko lai tyo directory ma pyuraucha

        def __str__(self):
             return self.name
        
        @property
        def imageURL(self):
             try:
                  url = self.image.url
             except:
                  url= ''
             return url
          #to solve image problem of not adding one

class Order(models.Model):
     customer= models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank= True) 
    #  many to one relation that is a customer can have more order
     date_ordered=models.DateTimeField(auto_now_add=True)
     complete=models.BooleanField(default=False)
     transaction_id=models.CharField(max_length=100, null=True)

     def __str__(self):
          return str(self.id)
     
     @property
     def shipping(self):
          shipping= False
          # query orderitem
          orderitems=self.orderitem_set.all()
          for i in orderitems:
               if i.product.digital== False:
                    shipping=True
          return shipping

     @property
     def get_cart_total(self):
          orderitems= self.orderitem_set.all()
          total= sum([item.get_total for item in orderitems])
          return total
     
     @property
     def get_cart_items(self):
          orderitems= self.orderitem_set.all()
          total= sum([item.quantity for item in orderitems])
          return total
     
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
         total=self.product.price * self.quantity
         return total

     
class ShippingAddress(models.Model):
     customer=models.ForeignKey(Customer,on_delete=models.SET_NULL, null=True)
     #even if the order is deleted we can still have shipping adress
     order=models.ForeignKey(Order , on_delete=models.SET_NULL, null=True)
     address=models.CharField(max_length=200, null=False)
     city=models.CharField(max_length=200, null=False)
     state=models.CharField(max_length=200, null=False)
     zipcode=models.CharField(max_length=200, null=False)
     date_added=models.DateTimeField(auto_now_add=True)

     def __str__(self):
          return self.address
