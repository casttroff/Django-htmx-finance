from django.contrib import admin
from tracker.models import Category, Transaction, Order, Product, LogisticsAgent
from django.contrib.auth.models import User, Group
from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm, SelectableFieldsExportForm
from unfold.contrib.filters.admin import (
    RangeDateFilter,
    RangeDateTimeFilter,
)
from unfold.contrib.filters.admin import ChoicesDropdownFilter, RelatedDropdownFilter, DropdownFilter
from modeltranslation.admin import TabbedTranslationAdmin

admin.site.unregister(User)
admin.site.unregister(Group)

@register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

@register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass
    

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = [f.name for f in Product._meta.fields]
    search_fields = ['name']
    list_filter = ['name', 'category']


# admin.site.register(User)
admin.site.register(Transaction)
admin.site.register(Category)
admin.site.register(LogisticsAgent)

@admin.register(Order)
class OrderAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ['id', 'user', 'get_products', 'total_amount', 'order_status', 'created_at']
    actions = ["order_shipped_action", "order_delivered_action"]
    import_form_class = ImportForm
    export_form_class = ExportForm
    selectable_fields_export_form_class = SelectableFieldsExportForm
    list_filter = [
        'user', ('order_status', ChoicesDropdownFilter), ('products', RelatedDropdownFilter), ('created_at', RangeDateFilter)
    ]
    list_filter_submit = True

    @admin.action(description="Marcar como 'enviado'")
    def order_shipped_action(self, request, queryset):
        orders_to_ship = queryset.exclude(order_status=Order.OrderChoices.SHIPPED)
        for order in orders_to_ship:
            try:
                user = order.user
                user.email_user(
                    'Tu pedido ha sido enviado',
                    f'Estimado {user.username}, tu pedido con id {order.id} ha sido enviado',
                    'admin@example.com',
                    fail_silently=False
                )
                order.order_status = Order.OrderChoices.SHIPPED
                order.save()
                self.message_user(
                    request,
                    f'El pedido {order.id} ha sido marcado como enviado y se ha notificado al usuario',
                )
            except Exception as e:
                self.message_user(
                    request,
                    f'Error al enviar el correo electrónico para el pedido {order.id}: {e}',
                    level='error'
                )

    @admin.action(description="Marcar como 'entregado'")
    def order_delivered_action(self, request, queryset):
        orders_to_deliver = queryset.exclude(order_status=Order.OrderChoices.DELIVERED)
        for order in orders_to_deliver:
            try:
                user = order.user
                user.email_user(
                    'Tu pedido ha sido entregado',
                    f'Estimado {user.username}, tu pedido con id {order.id} ha sido entregado.',
                    'admin@example.com',
                    fail_silently=False
                )
                order.order_status = Order.OrderChoices.DELIVERED
                order.save()
                self.message_user(
                    request,
                    f'El pedido {order.id} ha sido marcado como entregado y se ha notificado al usuario',
                )
            except Exception as e:
                self.message_user(
                    request,
                    f'Error al enviar el correo electrónico para el pedido {order.id}: {e}',
                    level='error'
                )