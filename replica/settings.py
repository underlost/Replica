from django.conf import settings

#Site Settings
SITE_NAME = getattr(settings, 'SITE_NAME', 'Replica')
SITE_DESC = getattr(settings, 'SITE_DESC', 'Just another blog.')
SITE_URL = getattr(settings, 'SITE_URL', 'http://localhost')
SITE_AUTHOR = getattr(settings, 'SITE_AUTHOR', 'Tyler')

DECK_ENTS = getattr(settings, 'REPLICA_DECK_ENTS', False)
PAGINATE = getattr(settings, 'REPLICA_PAGINATE', 25)
PAGINATE_TOPICS = getattr(settings, 'REPLICA_PAGINATE_TOPICS', 25)

#Enable plugins
ENABLE_BLIP = getattr(settings, 'REPLICA_ENABLE_BLIP', False)
ENABLE_WHISPER = getattr(settings, 'REPLICA_ENABLE_WHISPER', False)
ENABLE_MZINE = getattr(settings, 'REPLICA_ENABLE_MZINE', False)
