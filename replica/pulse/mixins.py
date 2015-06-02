from coreExtend.models import Account
from replica import settings as r_settings
from .models import Topic, Entry

class PulseViewMixin(object):

    date_field = 'pub_date'
    paginate_by = 25
    month_format = "%m"

    def get_allow_future(self):
        return self.request.user.is_staff

    def get_queryset(self):
        if r_settings.DECK_ENTS:
            if self.request.user.is_staff:
                return Entry.objects.posts().exclude(post_type__slug='linked', deck__exact='')
            else:
                return Entry.objects.published().exclude(post_type__slug='linked', deck__exact='')
        else:
            if self.request.user.is_staff:
                return Entry.objects.posts()
            else:
                return Entry.objects.published()

class LinkedViewMixin(object):

    date_field = 'pub_date'
    paginate_by = 25
    month_format = "%m"

    def get_allow_future(self):
        return self.request.user.is_staff

    def get_queryset(self):
        if self.request.user.is_staff:
            return Entry.objects.posts().filter(post_type='linked')
        else:
            return Entry.objects.published().filter(post_type='linked')
