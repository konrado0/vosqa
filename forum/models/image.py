from django.db import models
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
from resized_image_field import ResizableImageField
from node import Node

from django.conf import settings as djsettings

class Image(models.Model):
    image       = ResizableImageField(upload_to=djsettings.UPFILES_ALIAS, max_width=435, max_height=435, 
                                height_field="height", width_field="width")
    upload_url  = models.CharField(max_length=2048, blank=True, null=True)
    nodes       = models.ManyToManyField(Node)
    height      = models.PositiveIntegerField(null=True, blank=True, editable=False)
    width       = models.PositiveIntegerField(null=True, blank=True, editable=False)
    
    @property
    def url(self):
        """ Returns original url if possible, if not ulr on local serer. """
        if self.upload_url:
            return self.upload_url
        return self.image.url

@receiver(post_delete, sender=Image)
def mymodel_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    if instance.image:
        instance.image.delete(False)
