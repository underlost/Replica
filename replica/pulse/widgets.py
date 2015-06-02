from django.forms import forms, widgets

__author__ = 'Alfredo Saglimbeni'
import re
import uuid
from datetime import datetime

from django.forms.widgets import Widget, Select, MultiWidget, to_current_timezone, DateTimeInput
from django.forms.extras.widgets import SelectDateWidget
from django.utils.formats import get_format, get_language
from django.utils.safestring import mark_safe

__all__ = ('SelectTimeWidget', 'SplitSelectDateTimeWidget')

I18N = """
$.fn.datetimepicker.dates['en'] = {
    days: %s,
    daysShort: %s,
    daysMin: %s,
    months: %s,
    monthsShort: %s,
    meridiem: %s,
    suffix: %s,
    today: %s
};
"""

datetimepicker_options = """
    format : '%s',
    startDate : '%s',
    endDate : '%s',
    weekStart : %s,
    daysOfWeekDisabled : %s,
    autoclose : %s,
    startView : %s,
    minView : %s,
    maxView : %s,
    todayBtn : %s,
    todayHighlight : %s,
    minuteStep : %s,
    pickerPosition : '%s',
    showMeridian : %s,
    clearBtn : %s,
    language : '%s',
"""

dateConversiontoPython = {
    'P': '%p',
    'ss': '%S',
    'ii': '%M',
    'hh': '%H',
    'HH': '%I',
    'dd': '%d',
    'mm': '%m',
    #'M':  '%b',
    #'MM': '%B',
    'yy': '%y',
    'yyyy': '%Y',
}

dateConversiontoJavascript = {
    '%M': 'ii',
    '%m': 'mm',
    '%I': 'HH',
    '%H': 'hh',
    '%d': 'dd',
    '%Y': 'yyyy',
    '%y': 'yy',
    '%p': 'P',
    '%S': 'ss'
}

time_pattern = r'(\d\d?):(\d\d)(:(\d\d))? *([aApP]\.?[mM]\.?)?$'

RE_TIME = re.compile(time_pattern)
# The following are just more readable ways to access re.matched groups:
HOURS = 0
MINUTES = 1
SECONDS = 3
MERIDIEM = 4

class SelectTimeWidget(Widget):
    """
    A Widget that splits time input into <select> elements.
    Allows form to show as 24hr: <hour>:<minute>:<second>, (default)
    or as 12hr: <hour>:<minute>:<second> <am|pm>

    Also allows user-defined increments for minutes/seconds
    """
    hour_field = '%s_hour'
    minute_field = '%s_minute'
    second_field = '%s_second'
    meridiem_field = '%s_meridiem'
    twelve_hr = False # Default to 24hr.

    def __init__(self, attrs=None, hour_step=None, minute_step=None, second_step=None, twelve_hr=False):
        """
        hour_step, minute_step, second_step are optional step values for
        for the range of values for the associated select element
        twelve_hr: If True, forces the output to be in 12-hr format (rather than 24-hr)
        """
        self.attrs = attrs or {}

        if twelve_hr:
            self.twelve_hr = True # Do 12hr (rather than 24hr)
            self.meridiem_val = 'a.m.' # Default to Morning (A.M.)

        if hour_step and twelve_hr:
            self.hours = range(1,13,hour_step)
        elif hour_step: # 24hr, with stepping.
            self.hours = range(0,24,hour_step)
        elif twelve_hr: # 12hr, no stepping
            self.hours = range(1,13)
        else: # 24hr, no stepping
            self.hours = range(0,24)

        if minute_step:
            self.minutes = range(0,60,minute_step)
        else:
            self.minutes = range(0,60)

        if second_step:
            self.seconds = range(0,60,second_step)
        else:
            self.seconds = range(0,60)

    def render(self, name, value, attrs=None):
        try: # try to get time values from a datetime.time object (value)
            hour_val, minute_val, second_val = value.hour, value.minute, value.second
            if self.twelve_hr:
                if hour_val >= 12:
                    self.meridiem_val = 'p.m.'
                else:
                    self.meridiem_val = 'a.m.'
        except AttributeError:
            hour_val = minute_val = second_val = 0
            if isinstance(value, basestring):
                match = RE_TIME.match(value)
                if match:
                    time_groups = match.groups();
                    hour_val = int(time_groups[HOURS]) % 24 # force to range(0-24)
                    minute_val = int(time_groups[MINUTES])
                    if time_groups[SECONDS] is None:
                        second_val = 0
                    else:
                        second_val = int(time_groups[SECONDS])

                    # check to see if meridiem was passed in
                    if time_groups[MERIDIEM] is not None:
                        self.meridiem_val = time_groups[MERIDIEM]
                    else: # otherwise, set the meridiem based on the time
                        if self.twelve_hr:
                            if hour_val >= 12:
                                self.meridiem_val = 'p.m.'
                            else:
                                self.meridiem_val = 'a.m.'
                        else:
                            self.meridiem_val = None


        # If we're doing a 12-hr clock, there will be a meridiem value, so make sure the
        # hours get printed correctly
        if self.twelve_hr and self.meridiem_val:
            if self.meridiem_val.lower().startswith('p') and hour_val > 12 and hour_val < 24:
                hour_val = hour_val % 12
        elif hour_val == 0:
            hour_val = 12

        output = []
        if 'id' in self.attrs:
            id_ = self.attrs['id']
        else:
            id_ = 'id_%s' % name

        # For times to get displayed correctly, the values MUST be converted to unicode
        # When Select builds a list of options, it checks against Unicode values
        hour_val = u"%.2d" % hour_val
        minute_val = u"%.2d" % minute_val
        second_val = u"%.2d" % second_val

        hour_choices = [("%.2d"%i, "%.2d"%i) for i in self.hours]
        local_attrs = self.build_attrs(id=self.hour_field % id_)
        select_html = Select(choices=hour_choices).render(self.hour_field % name, hour_val, local_attrs)
        output.append(select_html)

        minute_choices = [("%.2d"%i, "%.2d"%i) for i in self.minutes]
        local_attrs['id'] = self.minute_field % id_
        select_html = Select(choices=minute_choices).render(self.minute_field % name, minute_val, local_attrs)
        output.append(select_html)

        second_choices = [("%.2d"%i, "%.2d"%i) for i in self.seconds]
        local_attrs['id'] = self.second_field % id_
        select_html = Select(choices=second_choices).render(self.second_field % name, second_val, local_attrs)
        output.append(select_html)

        if self.twelve_hr:
            #  If we were given an initial value, make sure the correct meridiem gets selected.
            if self.meridiem_val is not None and  self.meridiem_val.startswith('p'):
                    meridiem_choices = [('p.m.','p.m.'), ('a.m.','a.m.')]
            else:
                meridiem_choices = [('a.m.','a.m.'), ('p.m.','p.m.')]

            local_attrs['id'] = local_attrs['id'] = self.meridiem_field % id_
            select_html = Select(choices=meridiem_choices).render(self.meridiem_field % name, self.meridiem_val, local_attrs)
            output.append(select_html)

        return mark_safe(u'\n'.join(output))

    def id_for_label(self, id_):
        return '%s_hour' % id_
    id_for_label = classmethod(id_for_label)

    def value_from_datadict(self, data, files, name):
        # if there's not h:m:s data, assume zero:
        h = data.get(self.hour_field % name, 0) # hour
        m = data.get(self.minute_field % name, 0) # minute
        s = data.get(self.second_field % name, 0) # second

        meridiem = data.get(self.meridiem_field % name, None)

        #NOTE: if meridiem is None, assume 24-hr
        if meridiem is not None:
            if meridiem.lower().startswith('p') and int(h) != 12:
                h = (int(h)+12)%24
            elif meridiem.lower().startswith('a') and int(h) == 12:
                h = 0

        if (int(h) == 0 or h) and m and s:
            return '%s:%s:%s' % (h, m, s)

        return data.get(name, None)

class SplitSelectDateTimeWidget(MultiWidget):
    """
    MultiWidget = A widget that is composed of multiple widgets.

    This class combines SelectTimeWidget and SelectDateWidget so we have something
    like SpliteDateTimeWidget (in django.forms.widgets), but with Select elements.
    """
    def __init__(self, attrs=None, hour_step=None, minute_step=None, second_step=None, twelve_hr=None, years=None):
        """ pass all these parameters to their respective widget constructors..."""
        widgets = (SelectDateWidget(attrs=attrs, years=years), SelectTimeWidget(attrs=attrs, hour_step=hour_step, minute_step=minute_step, second_step=second_step, twelve_hr=twelve_hr))
        super(SplitSelectDateTimeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.date(), value.time().replace(microsecond=0)]
        return [None, None]

    def format_output(self, rendered_widgets):
        """
        Given a list of rendered widgets (as strings), it inserts an HTML
        linebreak between them.

        Returns a Unicode string representing the HTML for the whole lot.
        """
        rendered_widgets.insert(-1, ' at ')
        return u''.join(rendered_widgets)


class DateTimeWidget(MultiWidget):

    def to_local(self):
        """
        This method have to be called on every request call, because adapt the datetime format to the user.
        !!! It work only if USE_L10N is set TRUE and localize middleware is active.!!!
        otherwise get_format use the server format.
        """
        pattern = re.compile(r'(?<!\w)(' + '|'.join(dateConversiontoJavascript.keys()) + r')\b')
        self.format = get_format('DATETIME_INPUT_FORMATS')[0]
        if hasattr(self, 'widgets') and self.widgets[0]:
            self.widgets[0].format = self.format
        self.option = (pattern.sub(lambda x: dateConversiontoJavascript[x.group()], self.format),) + self.option[1:]
        self.language = get_language()

    def __init__(self, attrs=None, options=None, usel10n = None):
        if attrs is None:
            attrs = {'readonly':''}

        if options is None:
            options = {}

        self.option = ()
        if usel10n is True:
            self.is_localized = True
            #Use local datetime format Only if USE_L10N is true and middleware localize is active
            self.to_local()
        else:
            pattern = re.compile(r'\b(' + '|'.join(dateConversiontoPython.keys()) + r')\b')
            self.option += (options.get('format','dd/mm/yyyy hh:ii'),)
            self.format = pattern.sub(lambda x: dateConversiontoPython[x.group()], self.option[0])

        self.option += (options.get('startDate',''),)
        self.option += (options.get('endDate',''),)
        self.option += (options.get('weekStart','0'),)
        self.option += (options.get('daysOfWeekDisabled','[]'),)
        self.option += (options.get('autoclose','true'),)
        self.option += (options.get('startView','2'),)
        self.option += (options.get('minView','0'),)
        self.option += (options.get('maxView','4'),)
        self.option += (options.get('todayBtn','false'),)
        self.option += (options.get('todayHighlight','false'),)
        self.option += (options.get('minuteStep','5'),)
        self.option += (options.get('pickerPosition','bottom-right'),)
        self.option += (options.get('showMeridian','false'),)
        self.option += (options.get('clearBtn','true'),)

        self.language = options.get('language', 'en')
        self.option += (self.language,)

        widgets = (DateTimeInput(attrs=attrs, format=self.format),)

        super(DateTimeWidget, self).__init__(widgets, attrs)

    def value_from_datadict(self, data, files, name):

        if self.is_localized:
            #Adapt the format to the user.
            self.to_local()

        date_time = [
            widget.value_from_datadict(data, files, name + '_%s' % i)
            for i, widget in enumerate(self.widgets)
        ]
        try:
            D = to_current_timezone(datetime.strptime(date_time[0], self.format))
        except (ValueError, TypeError), e:
            return ''
        else:
            return D

    def decompress(self, value):

        if self.is_localized:
            #Adapt the format to the user.
            self.to_local()

        if value:
            value = to_current_timezone(value).strftime(self.format)
            return (value,)
        return (None,)

    def format_output(self, rendered_widgets):
        """
        Given a list of rendered widgets (as strings), it inserts an HTML
        linebreak between them.

        Returns a Unicode string representing the HTML for the whole lot.
        """

        if self.is_localized:
            #Adapt the format to the user.
            self.to_local()

        js_options = datetimepicker_options % self.option

        id = uuid.uuid4().hex
        return '<div id="%s"  class="input-group date form_datetime">'\
               '%s'\
               '<span class="input-group-addon"><span class="glyphicon glyphicon-th"></span></span>'\
               '</div>'\
               '<script type="text/javascript">'\
               '$("#%s").datetimepicker({%s});'\
               '</script>  ' % (id, rendered_widgets[0], id, js_options)




    def _media(self):
        js = ["js/bootstrap-datetimepicker.js"]
        if self.language != 'en':
            js.append("js/locales/bootstrap-datetimepicker.%s.js" % self.language)

        return widgets.Media(
            css={
                'all': ('css/datetimepicker.css',)
            },
            js=js
        )
    media = property(_media)
