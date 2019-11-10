from django.shortcuts import render
from django.views.generic.edit import FormView
from django import forms
from django.utils import timezone
from school.models import *
from django.db.models import Q, Sum, Count


class timetableBuildForm(forms.Form):
    date = forms.DateField(
        widget=forms.TextInput(attrs={'class':'datepicker'}))
    month = forms.BooleanField(label='Show data for selected month', required=False)

    def clean(self):
        data = self.cleaned_data
        date = data.get('date')
        today = timezone.localtime(timezone.now())
        if date and date < today.date():
            raise forms.ValidationError('Timetable cannot be set for the past!')
        return data


class timetableView(FormView):
    template_name = 'timetable.html'
    form_class = timetableBuildForm

    def get(self, request):
        context = dict()
        context['form'] = self.form_class
        return render(request, self.template_name, context)


    def post(self, request):
        context = dict()
        form = self.form_class(request.POST)
        context['form'] = form

        if not form.is_valid():
            return render(request, self.template_name, context)

        data = form.cleaned_data
        dt = data['date']
        month = data['month']
        context['dt'] = dt
        context['month'] = month

        qs = Q(dt=dt)
        if month:
            qs = Q(dt__year=dt.year, dt__month=dt.month)

        #  dt, classroom, subjects , teachers .
        tt = TimeTable.objects.filter(qs).select_related(
            'classroom', 'subject', 'teacher').only(
                'dt',
                'classroom__name',
                'subject__name',
                'teacher__name',
                'classroom__web_lecture_support',
                'teacher__web_lecture_support').order_by('dt')
        if tt.exists():
            context['tt'] = list(tt)

        else:
            context['message'] = 'No data for {}'.format(dt)

        return render(request, self.template_name, context)

def insights(request, year, month, day=None):
    context = dict()
    template_name = 'insights.html'
    qs = Q(dt__year=year) & Q(dt__month=month)
    if day:
        qs &= Q(dt__day=day)

    basett = TimeTable.objects.filter(qs)
    # teachers earning more than 1 Lac per month and the sum of their salaries.
    lpagt12 = 1200000
    i1 = basett.select_related('teacher').filter(
        teacher__salary__gt=lpagt12).values_list(
            'teacher_id').distinct().aggregate(
                total_salary=Sum('teacher__salary'), count=Count('teacher_id'))

    # No of students, No of teachers, and total hours required for subjects that are taught by more than 1 teacher.
    i2 = Subject.objects.annotate(
        t=Count('subjects')).filter(t__gt=1).aggregate(
            total_hours=Sum('total_duration') / 60, tot_teachers_more_subs=Sum('t'))

    i1.update(i2)
    context.update(i1)

    context['dt'] = '{}-{}{}'.format(year, month, '-{}'.format(day) if day else '')

    return render(request, template_name, context)

