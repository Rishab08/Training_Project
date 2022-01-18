from django.urls import path
from tablib import Dataset
from django.contrib import admin, messages
from django.shortcuts import render

from Test.models import Test


class TestAdmin(admin.ModelAdmin):
    change_list_template = "admin/Test/change.html"


admin.site.register(Test, TestAdmin)
