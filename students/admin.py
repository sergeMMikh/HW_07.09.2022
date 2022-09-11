from django.contrib import admin

from students.models import Student, Course


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    ...

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    ...
