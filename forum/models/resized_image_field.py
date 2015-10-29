import os
try:
    from PIL import Image, ImageChops
except ImportError:
    import Image, ImageChops
from cStringIO import StringIO

from django.conf import settings
from django.core.files.base import ContentFile

from django.db.models import ImageField
from django.utils.deconstruct import deconstructible
from sorl.thumbnail import default
from django.db.models import Q
import uuid


DEFAULT_SIZE = getattr(settings, 'DJANGORESIZED_DEFAULT_SIZE', [1280, 1024])
# DEFAULT_COLOR = (255, 255, 255, 0)

__all__ = ('ResizableImageField', 'ResizedImageFormField', 'ResizableImageFieldFile')

class ResizableImageFieldFile(ImageField.attr_class):
    """ 
    Extends Djangos ImageFileField with ability to resize to large images during save.
    Also incorporates methods added by sorl-thumbnail (which inherits from Django's FileField).
    """
    
    def save(self, name, content, save=True):
        content.file.seek(0)
        image = Image.open(content.file)
        w, h = image.size
        file_format = image.format
        if not file_format:
            file_format = 'JPEG'
        
        if self.field.exact_size and (w != self.field.max_width or h != self.field.max_height):
            # Make image exactly size with padding if aspects is not matched
            new_content = StringIO()
            if w < self.field.max_width and h < self.field.max_height:
                #image is smaller then desired size
                factor = min(self.field.max_width / float(w), self.field.max_height / float(h))                
                image = image.resize((int(w*factor), int(h*factor)), Image.ANTIALIAS)                
            else:
                image.thumbnail((self.field.max_width, self.field.max_height), Image.ANTIALIAS)
            
            image_size = image.size
            
            # Fill empty space with choosen color
            if max(self.field.max_width - image_size[0], self.field.max_height - image_size[1]) > 0:
                offset = (max( (self.field.max_width - image_size[0]) / 2, 0 ), max( (self.field.max_height - image_size[1]) / 2, 0 ))            
                final_thumb = Image.new(mode='RGBA',size=(self.field.max_width, self.field.max_height), color=self.field.fill_color)
                final_thumb.paste(image, offset)                
                image = final_thumb
            
            image.save(new_content, format=file_format)                            
            content = ContentFile(new_content.getvalue())
        elif w > self.field.max_width or h > self.field.max_height:
            # simple resize
            new_content = StringIO()
            image.thumbnail((self.field.max_width, self.field.max_height), Image.ANTIALIAS)        
            image.save(new_content, format=file_format)#, **img.info)
            content = ContentFile(new_content.getvalue())
        else:
            content.file.seek(0)

        super(ResizableImageFieldFile, self).save(name, content, save)

@deconstructible
class GetName(object):
    """ Replaces file name with random strings. """
    
    def __init__(self, sub_path):
        self.prefix = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return os.path.join(self.prefix, filename[:2], filename[2:4], filename)

class ResizableImageField(ImageField):
    """
    Extension of Djangos ImageField that provides automatic resizing of large images 
    and replacing filenames with random strings.
    Also incorporates methods added by sorl-thumbnail (which inherits from Django's FileField).
    """
    
    attr_class = ResizableImageFieldFile

    def __init__(self, verbose_name=None, name=None, **kwargs):
        self.max_width = kwargs.pop('max_width', DEFAULT_SIZE[0])
        self.max_height = kwargs.pop('max_height', DEFAULT_SIZE[1])
        self.exact_size = kwargs.pop('exact_size', False)
        self.fill_color = kwargs.pop('fill_color', (220,220,220,0))
        
        upload_to = kwargs.get('upload_to', '')
        if not callable(upload_to):
            kwargs['upload_to'] = GetName(kwargs.get('upload_to', ''))
#         self.use_thumbnail_aspect_ratio = kwargs.pop('use_thumbnail_aspect_ratio', False)
#         self.background_color = kwargs.pop('background_color', DEFAULT_COLOR)
        super(ResizableImageField, self).__init__(verbose_name, name, **kwargs)
        
    def delete_file(self, instance, sender, **kwargs):
        """
        Adds deletion of thumbnails and key kalue store references to the
        parent class implementation. Only called in Django < 1.2.5
        """
        file_ = getattr(instance, self.attname)
        # If no other object of this type references the file, and it's not the
        # default value for future objects, delete it from the backend.
        query = Q(**{self.name: file_.name}) & ~Q(pk=instance.pk)
        qs = sender._default_manager.filter(query)
        if (file_ and file_.name != self.default and not qs):
            default.backend.delete(file_)
        elif file_:
            # Otherwise, just close the file, so it doesn't tie up resources.
            file_.close()

    def save_form_data(self, instance, data):
        if data is not None:
            setattr(instance, self.name, data or '')

    def south_field_triple(self):
        from south.modelsinspector import introspector
        cls_name = '%s.%s' % (self.__class__.__module__ , self.__class__.__name__)
        args, kwargs = introspector(self)
        return (cls_name, args, kwargs)

# try:
#     from south.modelsinspector import add_introspection_rules
#     rules = [
#         (
#             (ResizableImageField,),
#             [],
#             {
#                 "max_width": ["max_width", {'default': DEFAULT_SIZE[0]}],
#                 "max_height": ["max_height", {'default': DEFAULT_SIZE[1]}],
# #                 "use_thumbnail_aspect_ratio": ["use_thumbnail_aspect_ratio", {'default': False}],
# #                 "background_color": ["background_color", {'default': DEFAULT_COLOR}],
#             },
#         )
#     ]
#     add_introspection_rules(rules, ["^django_resized\.forms\.ResizableImageField"])
# except ImportError:
#     pass