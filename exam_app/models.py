from django.db import models
from login_app.models import User
from datetime import datetime

# Create your models here.

class TripManager(models.Manager):
    def trip_validator(self, postData):
        errors = {}
        if len(postData['destination']) < 3:
            errors['destination'] = "Trip destination must be at least 3 characters long!"
        if len(postData['plan']) < 3:
            errors['plan'] = "Trip plan must be at least 3 characters long!"
        if len(postData['start_date']) != 10:
            errors['start_date'] = "Please enter a valid start date!"
        if len(postData['end_date']) != 10:
            errors['end_date'] = "Please enter a valid end date!"
        else:
            form_start_date = datetime.strptime(postData['start_date'], "%Y-%m-%d")
            form_end_date = datetime.strptime(postData['end_date'], "%Y-%m-%d")
            if form_start_date < datetime.now():
                errors['start_date'] = "Start date must be in the future!"
            if form_end_date <= form_start_date:
                errors['end_date'] = "End date must be after start date, users cannot time travel!"
        return errors

class Trip(models.Model):
    destination = models.CharField(max_length = 255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    plan = models.TextField()
    creator = models.ForeignKey(User, related_name = "trips_created", on_delete = models.CASCADE)
    attendees = models.ManyToManyField(User, related_name = "trips_attending")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = TripManager()
    