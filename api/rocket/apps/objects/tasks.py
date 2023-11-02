import os
from email.mime.image import MIMEImage
from random import uniform

from celery import shared_task
from django.core.mail import EmailMessage
from django.db.models import F

from rocket.apps.objects.models import ChainObject
from rocket.settings import MEDIA_ROOT


@shared_task
def increase_debt():
    """
    Increase debt by random value in range from 5 to 500.
    """
    qs = ChainObject.objects.exclude(type=0).update(debt=F("debt") + round(uniform(5, 500), 2))


@shared_task
def decrease_debt():
    """
    Decrease debt by random value in range from 100 to 10000.
    """
    qs = ChainObject.objects.exclude(type=0).update(debt=F("debt") - round(uniform(100, 10000), 2))
    qs = ChainObject.objects.filter(debt__lt=0).update(debt=0)


@shared_task
def clear_debt_action(uuids: list):
    """
    Clear debt from admin panel.
    """
    for uuid in uuids:
        obj = ChainObject.objects.filter(uuid=uuid).update(debt=0.00)


@shared_task
def send_qrcode_email(receiver: str, uuid: str):
    """
    Send QRCode with Contact information to User email.
    """
    email = EmailMessage(
        subject="QRCode of Object", body="Here you QR Code with Object Contact information!", to=(receiver,)
    )
    with open(os.path.join(MEDIA_ROOT, f"object_qrcode_{uuid}.png"), mode="rb") as img:
        image = MIMEImage(img.read())
        email.attach(image)
    email.send()
