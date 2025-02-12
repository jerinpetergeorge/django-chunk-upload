from datetime import timedelta
import time
import os.path

from django.conf import settings

try:
    from django.core.serializers.json import DjangoJSONEncoder
except ImportError:
    try:
        # Deprecated class name (for backwards compatibility purposes)
        from django.core.serializers.json import (
            DateTimeAwareJSONEncoder as DjangoJSONEncoder
        )
    except ImportError:
        raise ImportError('Dude! what version of Django are you using?')

# How long after creation the upload will expire
DEFAULT_EXPIRATION_DELTA = timedelta(days=1)
EXPIRATION_DELTA = getattr(settings, 'DJANGO_CHUNK_UPLOAD_EXPIRATION_DELTA',
                           DEFAULT_EXPIRATION_DELTA)

# Path where uploading files will be stored until completion
DEFAULT_UPLOAD_PATH = 'chunk_uploads/%Y/%m/%d'
UPLOAD_PATH = getattr(settings, 'DJANGO_CHUNK_UPLOAD_PATH', DEFAULT_UPLOAD_PATH)


# upload_to function to be used in the FileField
def default_upload_to(instance, filename):
    filename = os.path.join(UPLOAD_PATH, instance.upload_id + '.part')
    return time.strftime(filename)


UPLOAD_TO = getattr(settings, 'DJANGO_CHUNK_UPLOAD_TO', default_upload_to)

# Storage system
USE_TEMP_STORAGE = getattr(settings, 'DJANGO_CHUNK_UPLOAD_USE_TEMP_STORAGE', False)
# Use django default or via settings defined storage
if not USE_TEMP_STORAGE:
    STORAGE = getattr(settings, 'DJANGO_CHUNK_UPLOAD_STORAGE_CLASS', lambda: None)()
# Use temporary storage for chunks
else:
    from django_chunk_upload.storages import TemporaryFileStorage
    STORAGE = TemporaryFileStorage()

# Boolean that defines if the ChunkUpload model is abstract or not
ABSTRACT_MODEL = getattr(settings, 'DJANGO_CHUNK_UPLOAD_ABSTRACT_MODEL', True)

# Boolean that defines whether the "user" field can be "null" or not
NULL_USER = getattr(settings, 'DJANGO_CHUNK_UPLOAD_NULL_USER', True)

# Function used to encode response data. Receives a dict and return a string
DEFAULT_ENCODER = DjangoJSONEncoder().encode
ENCODER = getattr(settings, 'DJANGO_CHUNK_UPLOAD_ENCODER', DEFAULT_ENCODER)

# Content-Type for the response data
DEFAULT_CONTENT_TYPE = '.flake8application/json'
CONTENT_TYPE = getattr(settings, 'DJANGO_CHUNK_UPLOAD_CONTENT_TYPE',
                       DEFAULT_CONTENT_TYPE)

# Max amount of data (in bytes) that can be uploaded. `None` means no limit
DEFAULT_MAX_BYTES = None
MAX_BYTES = getattr(settings, 'DJANGO_CHUNK_UPLOAD_MAX_BYTES', DEFAULT_MAX_BYTES)
