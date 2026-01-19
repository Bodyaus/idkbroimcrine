from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q

class Hotel(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    price = models.IntegerField()


    def __str__(self):
        return self.title

# Create your models here.



class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey('Hotel', on_delete=models.CASCADE, verbose_name="Номер/Готель")
    start_date = models.DateField(verbose_name="Дата заїзду")
    end_date   = models.DateField(verbose_name="Дата виїзду")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} → {self.room.title} ({self.start_date} – {self.end_date})"

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("Дата виїзду має бути пізніше дати заїзду")

        overlapping = Booking.objects.filter(
            room=self.room,
            start_date__lte=self.end_date,
            end_date__gte=self.start_date
        ).exclude(pk=self.pk)

        if overlapping.exists():
            raise ValidationError("Цей номер вже зайнятий на вибрані дати")