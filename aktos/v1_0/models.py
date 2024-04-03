from django.db import models
from django.core.validators import MinLengthValidator
from uuid import uuid4
from django.utils.timezone import now

class StatusChoises(models.IntegerChoices):
    """List of balance allowed status"""
    INACTIVE = 0
    PAID_IN_FULL = 1
    IN_COLLECTION = 2

class Consumer(models.Model):
    """Consumer info"""
    ssn = models.CharField(max_length=11, primary_key=True, editable=True, validators=[MinLengthValidator(11)])
    name = models.TextField()
    address = models.TextField()
    created = models.DateTimeField(unique=True, default=now, editable=False)

    class Meta:
        indexes = [
            models.Index(fields=["created"], name="consumer_created_idx")
        ]

class ConsumerBalance(models.Model):
    """Consumer balance info"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    client_reference_no = models.UUIDField(default=uuid4, editable=True)
    balance = models.FloatField()
    status = models.IntegerField(choices=StatusChoises.choices)
    consumer = models.ForeignKey(
        Consumer,
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(unique=True, default=now, editable=False)
    class Meta:
        indexes = [
            models.Index(fields=["created"], name="account_created_idx"),
        ]
