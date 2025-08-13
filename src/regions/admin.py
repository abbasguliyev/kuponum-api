from django.contrib import admin

from django.contrib import admin
from regions.models import Region

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
	list_display = ("id", "name", "parent")
	list_filter = ("parent",)
	search_fields = ("name",)
	ordering = ("parent__name", "name")
	autocomplete_fields = ("parent",)
