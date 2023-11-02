import os
import qrcode
from typing import OrderedDict

from rocket.settings import MEDIA_ROOT


def generate_qr(contact: OrderedDict, uuid: str):
    """
    Function which generate QRCode from Contact information.
    """
    data_string: str = f" Email — {contact['email']},\n Country — {contact['country']},\n City — {contact['city']},\n Street — {contact['street']},\n Building — {contact['building']}."
    img = qrcode.make(data_string)
    img.save(os.path.join(MEDIA_ROOT, f"object_qrcode_{uuid}.png"))
