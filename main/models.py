from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
    def user_validator(self, post_data):
        errors = {}

        email_checker = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(post_data['first_name']) < 3:
            errors['first_name'] = 'The first name must be more than 3 character'

        if len(post_data['last_name']) < 3:
            errors['last_name'] = 'The last name must be more than 3 character'

        if not email_checker.match(post_data['email']):
            errors['email'] = 'Invalid email address!'

        if post_data['password'] != post_data['cf_password']:
            errors['password'] = 'passwords do not match '

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    password = models.CharField(max_length=450)
    ballance = models.IntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()


class Stock(models.Model):
    stock = models.CharField(max_length=175)
    price = models.FloatField()
    difference = models.FloatField()
    user = models.ForeignKey(User, related_name="portfolio", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)