import os
import urllib2
from urlparse import urlparse
from cStringIO import StringIO
from PIL import Image
import markdown
import datetime
from time import strftime
from hashlib import md5
import uuid
from random import choice

from django.utils.translation import ugettext_lazy as _
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.base import ContentFile
from django.utils.encoding import smart_unicode, smart_str

def create_thumbnail(image_source, thumb_size_x=250, thumb_size_y=2500, content_type=None):
	if not image_source.image:
		return
	THUMBNAIL_SIZE = (thumb_size_x, thumb_size_y)
	DJANGO_TYPE = content_type if content_type else image_source.image.file.content_type
	if DJANGO_TYPE == 'image/jpeg':
		PIL_TYPE = 'jpeg'
		FILE_EXTENSION = 'jpg'
	elif DJANGO_TYPE == 'image/png':
		PIL_TYPE = 'png'
		FILE_EXTENSION = 'png'
	image = Image.open(StringIO(image_source.image.read()))
	image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
	temp_handle = StringIO()
	image.save(temp_handle, PIL_TYPE)
	temp_handle.seek(0)
	suf = SimpleUploadedFile(os.path.split(image_source.image.name)[-1],
			temp_handle.read(), content_type=DJANGO_TYPE)
	image_source.thumbnail.save('%s_thumbnail.%s'%(os.path.splitext(suf.name)[0],FILE_EXTENSION), suf, save=False)

def guid_generator(user_id=None, length=32):
	if user_id:
		guid_base = "%s" % (user_id)
		guid_encode = guid_base.encode('ascii', 'ignore')
		guid = md5(guid_encode).hexdigest()[:12]
	else:
		guid_base = str(uuid.uuid4())
		guid_encoded = guid_base.encode('ascii', 'ignore')
		guid = md5(guid_encoded).hexdigest()[:length]
	return guid


def username_generator(delimiter='-', tokenLength=4, tokenHex=False, tokenChars='0123456789'):
    """
    Generate Heroku-like random names to use in your applications.
    :param delimiter:
    :param tokenLength:
    :param tokenHex:
    :param tokenChars:
    :return: string
    """

    adjs = [
      'autumn', 'hidden', 'bitter', 'misty', 'silent', 'empty', 'dry', 'dark',
      'summer', 'icy', 'delicate', 'quiet', 'white', 'cool', 'spring', 'winter',
      'patient', 'twilight', 'dawn', 'crimson', 'wispy', 'weathered', 'blue',
      'billowing', 'broken', 'cold', 'damp', 'falling', 'frosty', 'green',
      'long', 'late', 'lingering', 'bold', 'little', 'morning', 'muddy', 'old',
      'red', 'rough', 'still', 'small', 'sparkling', 'throbbing', 'shy',
      'wandering', 'withered', 'wild', 'black', 'young', 'holy', 'solitary',
      'fragrant', 'aged', 'snowy', 'proud', 'floral', 'restless', 'divine',
      'polished', 'ancient', 'purple', 'lively', 'nameless', 'lucky', 'odd', 'tiny',
      'free', 'dry', 'yellow', 'orange', 'gentle', 'tight', 'super', 'royal', 'broad',
      'steep', 'flat', 'square', 'round', 'mute', 'noisy', 'hushy', 'raspy', 'soft',
      'shrill', 'rapid', 'sweet', 'curly', 'calm', 'jolly', 'fancy', 'plain', 'shinny'
    ]

    nouns = [
      'waterfall', 'river', 'breeze', 'moon', 'rain', 'wind', 'sea', 'morning',
      'snow', 'lake', 'sunset', 'pine', 'shadow', 'leaf', 'dawn', 'glitter',
      'forest', 'hill', 'cloud', 'meadow', 'sun', 'glade', 'bird', 'brook',
      'butterfly', 'bush', 'dew', 'dust', 'field', 'fire', 'flower', 'firefly',
      'feather', 'grass', 'haze', 'mountain', 'night', 'pond', 'darkness',
      'snowflake', 'silence', 'sound', 'sky', 'shape', 'surf', 'thunder',
      'violet', 'water', 'wildflower', 'wave', 'water', 'resonance', 'sun',
      'wood', 'dream', 'cherry', 'tree', 'fog', 'frost', 'voice', 'paper',
      'frog', 'smoke', 'star', 'atom', 'band', 'bar', 'base', 'block', 'boat',
      'term', 'credit', 'art', 'fashion', 'truth', 'disk', 'math', 'unit', 'cell',
      'scene', 'heart', 'recipe', 'union', 'limit', 'bread', 'toast', 'bonus',
      'lab', 'mud', 'mode', 'poetry', 'tooth', 'hall', 'king', 'queen', 'lion', 'tiger',
      'penguin', 'kiwi', 'cake', 'mouse', 'rice', 'coke', 'hola', 'salad', 'hat'
    ]

    if tokenHex:
        tokenChars = '0123456789abcdef'

    adj = choice(adjs)
    noun = choice(nouns)
    token = ''.join(choice(tokenChars) for _ in range(tokenLength))

    sections = [adj, noun, token]
    return delimiter.join(filter(None, sections))
