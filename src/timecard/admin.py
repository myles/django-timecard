from django import forms
from django.contrib import admin
from django.contrib.contenttypes import generic
from django.contrib.comments.models import Comment

from timecard.models import Manager, Timecard

class ManagerAdmin(admin.ModelAdmin):
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
	inlines = [
		CommentInline,
	]

admin.site.register(Manager, ManagerAdmin)
admin.site.register(Timecard, TimecardAdmin)