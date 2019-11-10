from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^timetable/$', views.timetableView.as_view(), name='timetable'),
    url(r'^insights/(?P<year>[\d]+)/(?P<month>[\d]+)/$', views.insights, name='insights'),
    url(r'^insights/(?P<year>[\d]+)/(?P<month>[\d]+)/(?P<day>[\d]+)/$', views.insights, name='insights'),
]
