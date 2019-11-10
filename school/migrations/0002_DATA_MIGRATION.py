# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime, random
from collections import defaultdict


def forward_operation(apps, schema_editor):
    Chapter = apps.get_model('school', 'Chapter')
    Subject = apps.get_model('school', 'Subject')
    Teacher = apps.get_model('school', 'Teacher')
    Classroom = apps.get_model('school', 'Classroom')
    TimeTable = apps.get_model('school', 'TimeTable')

    c, _ = Chapter.objects.get_or_create(name='test')

    ss = [
        'Math',
        'English',
        'Sports',
        'Health Science',
        'Music',
        'Botany',
        'Zoology',
        'Science',
        'Political Science',
        'Business Administration',
        'Foreign Affairs',
        'Negotiations',
        'Philosophy',
        'Moral Science',
    ]
    m = dict()
    for s in ss:
        o, j = Subject.objects.get_or_create(
            name=s,
            total_duration=1800,
            per_class_duration=60,
        )
        if j:
            o.chapters.add(c)
        m[o.name] = o

    l = 100000
    ts = [
        {'name': 'Turing', 'doj': '2017-08-22',
            'subjects': [m['Math'], m['English']], 'salary': 18 * l, 'web_lecture_support': True},
        {'name':' Dinho', 'doj': '2016-01-01',
            'subjects': [m['Sports'], m['Health Science']], 'salary': 25 * l},
        {'name': 'Adele', 'doj': '2015-03-01',
            'subjects': [m['English']], 'salary': 10},
        {'name': 'Freddie', 'doj': '2017-08-01',
            'subjects': [m['Music'], m['English']], 'salary': 20 * l, 'web_lecture_support': True},
        {'name': 'Dalton', 'doj': '2017-03-01',
            'subjects': [m['Botany'], m['Zoology']], 'salary': 9 * l, 'web_lecture_support': True},
        {'name': 'Harish', 'doj': '2017-02-01',
            'subjects': [m['Math'], m['Science']], 'salary': 18 * l},
        {'name': 'Trump', 'doj': '2017-08-01',
            'subjects': [m['Political Science'], m['Business Administration'], m['Foreign Affairs']], 'salary': 8 * l},
        {'name': 'Swaraj', 'doj': '2019-09-01',
            'subjects': [m['Foreign Affairs'], m['Negotiations']], 'salary': 28 * l, 'web_lecture_support': True},
        {'name': 'Socrates', 'doj': '2015-06-01',
            'subjects': [m['Philosophy'], m['Moral Science'], m['Negotiations']], 'salary': 11.5 * l, 'web_lecture_support': True}
    ]

    tsm = defaultdict(list)
    for t in ts:
        subs = t.pop('subjects')
        o, j = Teacher.objects.get_or_create(**t)
        if j:
            o.subjects.add(*subs)

        for sub in subs:
            tsm[sub.name].append(o)


    SHAPES = (1, 2, 3, 4)
    cm = dict()
    for i in range(len(ss)):
        o, _ = Classroom.objects.get_or_create(
            name='CR-{}'.format(i + 1),
            capacity=35,
            web_lecture_support=random.choice([True, False]),
            shape=random.choice(SHAPES)
        )
        cm[o.name] = o

    aa = list()
    for d in range(1, 31):
        cdt = datetime.date(2019, 12, d)
        random.SystemRandom().shuffle(ss)
        for i in range(len(ss)):
            s = ss[i]
            so = m[s]
            co = cm[random.choice(cm.keys())]
            to = random.choice(tsm[s])
            uid = '{}-{}-{}-{}'.format(
                cdt.strftime('%Y%m%d'), so.pk, to.pk, co.pk)

            while uid in aa:
                co = cm[random.choice(cm.keys())]
                to = random.choice(tsm[s])
                uid = '{}-{}-{}-{}'.format(
                    cdt.strftime('%Y%m%d'), so.pk, to.pk, co.pk)

            TimeTable.objects.create(
                dt=cdt,
                teacher=to,
                subject=so,
                classroom=co
            )

            aa.append(uid)


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forward_operation),
    ]
