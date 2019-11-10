from django.contrib import admin
from school.models import *


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Teacher, TeacherAdmin)


class StudentAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Student, StudentAdmin)


class GuardianAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Guardian, GuardianAdmin)


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_duration', 'per_class_duration')

admin.site.register(Subject, SubjectAdmin)


class ChapterAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Chapter, ChapterAdmin)


class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('name', 'shape',)

admin.site.register(Classroom, ClassroomAdmin)


class TimeTableAdmin(admin.ModelAdmin):
    list_display = ('dt',)

admin.site.register(TimeTable, TimeTableAdmin)
