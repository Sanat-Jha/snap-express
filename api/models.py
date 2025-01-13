from django.db import models
import os
from django.db.models.signals import pre_save
from django.dispatch import receiver
import shutil
from django.conf import settings



def event_image_upload_to(instance, filename):
    # Use the event name in the file path dynamically
    event_name = instance.event.name
    return os.path.join('gallery', event_name.replace(' ', '_'), filename)
# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=100, unique=True)
    current = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    # Custom delete method
    def delete(self, *args, **kwargs):
        # Construct the folder path based on the event name
        folder_path = os.path.join(settings.MEDIA_ROOT, 'gallery', self.name)
        
        # Check if the folder exists before attempting to delete
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            shutil.rmtree(folder_path)  # Delete the folder and its contents

        # Call the parent class delete method
        super().delete(*args, **kwargs)
@receiver(pre_save, sender=Event)
def ensure_single_current_event(sender, instance, **kwargs):
    if instance.current:
        # Get the current ID of the instance being saved
        current_id = instance.id if instance.id else None
        
        # Update all other events to not be current
        Event.objects.exclude(id=current_id).update(current=False)    
class EventImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=event_image_upload_to)

class TemplateCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Template(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='templates/')
    category = models.ForeignKey(TemplateCategory, on_delete=models.CASCADE)