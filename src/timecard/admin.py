from django import forms
from django.contrib import admin
from django.contrib.contenttypes import generic
from django.contrib.comments.models import Comment

from timecard.models import Employee, Timecard

class EmployeeAdmin(admin.ModelAdmin):
	list_display = ('__unicode__',)

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('site', 'comment', 'user')

class CommentInline(generic.GenericStackedInline):
	model = Comment
	ct_fk_field = 'object_pk'
	extra = 1
	form = CommentForm

class TimecardAdmin(admin.ModelAdmin):
	list_display = ('user', 'date')
	inlines = [
		CommentInline,
	]

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Timecard, TimecardAdmin)