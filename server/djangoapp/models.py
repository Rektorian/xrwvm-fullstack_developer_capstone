from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator

class CarMake(models.Model):
    """
    A model representing a car maker.

    Attributes:
        name (CharField): The name of the car make, limited to 200 characters.
        description (TextField): A detailed description of the car make.
    """
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        """
        Return the name of the car make for display purposes.

        Returns:
            str: The name of the car make.
        """
        return self.name
    
class CarModel(models.Model):
    """A model representing a car model."""
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE) # Many-to-one relationship to CarMake model (One car make can have many car models, using a ForeignKey field)
    name = models.CharField(max_length=200)
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
    ]
    type = models.CharField(max_length=20, choices=CAR_TYPES, default='SEDAN')
    year = models.IntegerField(validators=[MinValueValidator(2015), MaxValueValidator(2050)], default=2025)

    def __str__(self):
        return self.name

