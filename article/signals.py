from django.db.models.signals import pre_save
from django.dispatch import receiver,Signal
from .models import Tag

self_signal = Signal(providing_args=['self_signal_args'])

@receiver(pre_save,sender=Tag)
def preSaveFun(sender, **kwargs):
    print('pre save fun',sender,kwargs)
    print("============")

