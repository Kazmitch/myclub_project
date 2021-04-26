from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from datetime import date
import calendar
from calendar import HTMLCalendar
from .models import Event
from .forms import VenueForm


def index(request, year=date.today().year, month=date.today().month):
    year = int(year)
    month = int(month)
    if year < 2020 or year > 2099: year = date.today().year
    month_name = calendar.month_name[month]
    title = 'MyClub Event Calendar - %s %s' % (month_name, year)
    cal = HTMLCalendar().formatmonth(year, month)
    announcements = [
        {
            'date': '22-4-2021',
            'announcement': "Barcelona - Getafe"
        },
        {
            'date': '25-4-2021',
            'announcement': "Barcelona - Villarreal"
        }
    ]
    # return HttpResponse('<h1>%s</h1><p>%s</p>' % (title, cal))
    return render(request,
                  'events/calendar_base.html',
                  {'title': title, 'cal': cal, 'announcements': announcements}
                  )


def all_events(request):
    event_list = Event.objects.all()
    return render(request,
                  'events/event_list.html',
                  {'event_list': event_list}
                  )


def add_venue(request):
    submitted = False
    if request.method == 'POST':
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_venue/?submitted=True')
    else:
        form = VenueForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request,
                  'events/add_venue.html',
                  {'form': form, 'submitted': submitted}
                  )
