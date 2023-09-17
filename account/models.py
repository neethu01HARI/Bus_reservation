from django.db import models

# Create your models here.
class Bus(models.Model):
    bus_name = models.CharField(max_length=30)
    source = models.CharField(max_length=30)
    dest = models.CharField(max_length=30)
    nos = models.DecimalField(decimal_places=0, max_digits=2)
    rem = models.DecimalField(decimal_places=0, max_digits=2)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    date = models.DateField()
    time = models.TimeField()
    


class Book(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=30)
    userid =models.DecimalField(decimal_places=0, max_digits=2)
    busid=models.DecimalField(decimal_places=0, max_digits=2)
    bus_name = models.CharField(max_length=30)
    options=(('Kochi','Kochi'),
             ('Calicut','Calicut'),)
    source = models.CharField(choices=options,default='Kochi',max_length=30)
    dest = models.CharField(choices=options,default='Calicut',max_length=30)
    nos = models.DecimalField(decimal_places=0, max_digits=2)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    date = models.DateField()
    time = models.TimeField()
    TICKET_STATUSES = (('Booked', 'Booked'),
                       ('Cancelled', 'Cancelled'),
                       ('Paid', 'Paid'))
    status = models.CharField(choices=TICKET_STATUSES, default='Booked', max_length=100)
    
    class Meta:
        verbose_name_plural = "List of Books"
    def __str__(self):
        return self.email

class Payment(models.Model):
    user = models.ForeignKey(Book, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)



