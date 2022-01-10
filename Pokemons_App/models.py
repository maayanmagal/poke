from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, MaxLengthValidator,MinLengthValidator

# Create your models here.


class Pokemons(models.Model):
    Name = models.CharField(max_length=50, primary_key=True)
    Type = models.CharField(max_length=50)
    Generation = models.IntegerField()
    Legendary = models.BooleanField()
    Hp = models.IntegerField()
    Attack=models.IntegerField()
    Defense = models.IntegerField()
    class Meta():
        db_table='Pokemons'