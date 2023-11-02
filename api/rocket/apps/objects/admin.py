from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from django.utils.translation import ngettext

from rocket.apps.objects.models import ChainObject
from rocket.apps.objects.tasks import clear_debt_action


@admin.register(ChainObject)
class ChainObjectAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "debt", "supplier_link", "contact", "created")
    list_filter = ("contact__city",)
    readonly_fields = ("supplier_link",)
    actions = ("clear_debt",)

    @admin.action(description="Clear selected objects debt")
    def clear_debt(self, request, queryset):
        if len(queryset) >= 20:
            clear_debt_action.delay(list(queryset.values_list("uuid", flat=True)))
            self.message_user(request, "Debts were successfully cleaned.", messages.SUCCESS)
            return
        updated = queryset.update(debt=0.00)
        self.message_user(
            request,
            ngettext("%d Debt was successfully cleaned.", "%d Debts were successfully cleaned.", updated) % updated,
            messages.SUCCESS,
        )

    def supplier_link(self, obj):
        if obj.supplier:
            return mark_safe(
                f"<a href='/admin/objects/chainobject/{obj.supplier.uuid}/change/'>" f"{obj.supplier}" f"</a>"
            )

    supplier_link.short_description = "Supplier"
