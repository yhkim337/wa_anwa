from django.db import models
from accounts.models import User

# Create your models here.

class Betting(models.Model):
    date = models.CharField(max_length=11)
    time = models.CharField(max_length=6)
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
    point = models.IntegerField(default=0)



class Answer(models.Model):
    betting = models.OneToOneField(Betting, on_delete=models.CASCADE, related_name="answer")
    answer = models.BooleanField() #True:와, False:안와


class Result(models.Model):
    participation = models.OneToOneField(Participate, on_delete=models.CASCADE, related_name="result")
    point = models.IntegerField()
    win = models.BooleanField()
    checked = models.BooleanField()
