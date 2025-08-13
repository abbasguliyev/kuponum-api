from django.db import models
from django.utils.translation import gettext_lazy as _

class Region(models.Model):
    name = models.CharField(_("Ad"), max_length=100)
    parent = models.ForeignKey('self', verbose_name=_("Ana Region"), on_delete=models.CASCADE, null=True, blank=True, related_name='subregions')

    class Meta:
        verbose_name = _("Region")
        verbose_name_plural = _("Regionlar")
        indexes = [
            models.Index(fields=['name'], name='region_name_idx'),
        ]

    def __str__(self) -> str:
        if self.parent:
            return f"{self.parent} > {self.name}"
        return self.name
    
