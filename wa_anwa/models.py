from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ServiceUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='user/')
    point = models.IntegerField(default=500)

    def __str__(self):
        return self.name


class Betting(models.Model):
    date = models.DateField()
    time = models.IntegerField()
    region = models.CharField(max_length=10)

    def __str__(self):
        return self.region + ' ' + self.date + ' ' + self.time

    # https://docs.djangoproject.com/en/4.0/ref/models/constraints/#uniqueconstraint
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['date', 'time', 'region'],
                name='unique_betting'
            )
        ]


class Participate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="participates")
    betting = models.ForeignKey(Betting, on_delete=models.CASCADE, related_name="participates")
    choice = models.BooleanField()
    point = models.IntegerField()



class Answer(models.Model):
    betting = models.OneToOneField(Betting, on_delete=models.CASCADE, related_name="answer")
    answer = models.BooleanField()


class Result(models.Model):
    participation = models.OneToOneField(Participate, on_delete=models.CASCADE, related_name="result")
    point = models.IntegerField()
    win = models.BooleanField()
    checked = models.BooleanField()