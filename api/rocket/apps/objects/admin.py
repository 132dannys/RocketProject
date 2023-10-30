from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from django.utils.translation import ngettext

from rocket.apps.objects.models import ChainObject


@admin.register(ChainObject)
class ChainObjectAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "dept", "supplier_link", "contact")
    list_filter = ("contact__address__city",)
    readonly_fields = ("supplier_link",)
    actions = ("clear_debt",)

    @admin.action(description="Clear selected objects debt")
    def clear_debt(self, request, queryset):
        updated = queryset.update(dept=0.00)
        self.message_user(
            request,
            ngettext("%d Debt was successfully cleaned.", "%d Depts were successfully cleaned.", updated) % updated,
            messages.SUCCESS,
        )

    def supplier_link(self, obj):
        if obj.supplier:
            return mark_safe(
                f"<a href='/admin/objects/chainobject/{obj.supplier.uuid}/change/'>" f"{obj.supplier}" f"</a>"
            )

    supplier_link.short_description = "Supplier"
