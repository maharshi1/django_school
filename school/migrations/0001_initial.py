# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=45, verbose_name=b'Name')),
            ],
        ),
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=45, verbose_name=b'Name')),
                ('capacity', models.PositiveIntegerField(verbose_name=b'Capacity')),
                ('web_lecture_support', models.BooleanField(default=False, verbose_name=b'Web Lecture Support')),
                ('shape', models.PositiveSmallIntegerField(default=2, verbose_name=b'Shape', choices=[(1, b'oval'), (2, b'rectangular'), (3, b'canopy'), (4, b'elevated')])),
            ],
        ),
        migrations.CreateModel(
            name='Guardian',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=45, verbose_name=b'Name')),
                ('phone', models.PositiveIntegerField(verbose_name=b'Phone', validators=[django.core.validators.MaxValueValidator(10)])),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=45, verbose_name=b'Name')),
                ('doj', models.DateField(verbose_name=b'Date of Joining')),
                ('roll_no', models.PositiveIntegerField(verbose_name=b'Roll No')),
                ('ranking', models.PositiveIntegerField(verbose_name=b'Ranking')),
                ('point_of_contact', models.ManyToManyField(to='school.Guardian', verbose_name=b'Point of Contact')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=45, verbose_name=b'Name')),
                ('total_duration', models.PositiveIntegerField(verbose_name=b'Total Duration')),
                ('per_class_duration', models.PositiveIntegerField(verbose_name=b'Per Class Duration', validators=[django.core.validators.MaxValueValidator(120), django.core.validators.MinValueValidator(30)])),
                ('chapters', models.ManyToManyField(to='school.Chapter', verbose_name=b'Chapters')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=45, verbose_name=b'Name')),
                ('doj', models.DateField(verbose_name=b'Date of Joining')),
                ('salary', models.DecimalField(max_digits=10, decimal_places=2)),
                ('web_lecture_support', models.BooleanField(default=False, verbose_name=b'Web Lecture Support')),
                ('subjects', models.ManyToManyField(to='school.Subject', verbose_name=b'Subjects')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TimeTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dt', models.DateField(verbose_name=b'Date of Joining')),
                ('classroom', models.ForeignKey(related_name='teacher', verbose_name=b'Classroom', to='school.Classroom')),
                ('subject', models.ForeignKey(related_name='subject', verbose_name=b'Subject', to='school.Subject')),
                ('teacher', models.ForeignKey(related_name='teacher', verbose_name=b'Teacher', to='school.Teacher')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='guardian',
            unique_together=set([('phone', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='timetable',
            unique_together=set([('dt', 'subject', 'teacher', 'classroom')]),
        ),
        migrations.AlterUniqueTogether(
            name='student',
            unique_together=set([('roll_no', 'name')]),
        ),
    ]
