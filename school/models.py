from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Base(models.Model):
    name = models.CharField('Name', max_length=45, blank=False, null=False, unique=True)
    doj = models.DateField('Date of Joining', blank=False, null=False)


    class Meta:
        abstract = True


class Chapter(models.Model):
    name = models.CharField('Name', max_length=45, blank=False, null=False, unique=True)

    def __str__(self):
        return "{}".format(self.name)


class Subject(models.Model):
    name = models.CharField('Name', max_length=45, blank=False, null=False, unique=True)
    chapters = models.ManyToManyField(
        Chapter, verbose_name='Chapters', null=False)
    total_duration = models.PositiveIntegerField('Total Duration', blank=False, null=False)
    per_class_duration = models.PositiveIntegerField(
        'Per Class Duration', blank=False, null=False,
        validators=[MaxValueValidator(120), MinValueValidator(30)])

    def __str__(self):
        return "{}".format(self.name)

class Teacher(Base):
    subjects = models.ManyToManyField(
        Subject, verbose_name='Subjects', null=False, related_name='subjects')
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    web_lecture_support = models.BooleanField(
        'Web Lecture Support', blank=True, null=False, default=False)

    def __str__(self):
        return "{}".format(self.name)


class Guardian(models.Model):
    name = models.CharField('Name', max_length=45, blank=False, null=False)
    phone = models.PositiveIntegerField(
        'Phone', blank=False, null=False, validators=[MaxValueValidator(10)])

    def __str__(self):
        return "{}".format(self.name)


    class Meta:
        unique_together = ('phone', 'name')


class Student(Base):
    roll_no = models.PositiveIntegerField('Roll No', blank=False, null=False)
    ranking = models.PositiveIntegerField('Ranking', blank=False, null=False)
    point_of_contact = models.ManyToManyField(
        Guardian, verbose_name='Point of Contact',
        null=False)

    def __str__(self):
        return "{}".format(self.name)


    class Meta:
        unique_together = ('roll_no', 'name')


class Classroom(models.Model):
    SHAPES = (
        (1, 'oval'),
        (2, 'rectangular'),
        (3, 'canopy'),
        (4, 'elevated'),
    )

    name = models.CharField(
        'Name', max_length=45, blank=False, null=False, unique=True)
    capacity = models.PositiveIntegerField('Capacity', blank=False, null=False)
    web_lecture_support = models.BooleanField(
        'Web Lecture Support', blank=True, null=False, default=False)
    shape = models.PositiveSmallIntegerField('Shape', choices=SHAPES, default=2)

    def __str__(self):
        return "{}".format(self.shape)


class TimeTable(models.Model):
    subject = models.ForeignKey(
        Subject, verbose_name='Subject', null=False, blank=False, related_name='subject')
    teacher = models.ForeignKey(
        Teacher, verbose_name='Teacher', null=False, blank=False, related_name='teacher')
    classroom = models.ForeignKey(
        Classroom, verbose_name='Classroom', null=False, blank=False, related_name='teacher')
    dt = models.DateField('Date of Joining', blank=False, null=False)

    class Meta:
        unique_together = ('dt', 'subject', 'teacher', 'classroom')

