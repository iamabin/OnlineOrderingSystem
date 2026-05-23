from django.contrib import admin
from .models import Restaurant, MenuCategory, MenuItem, Table, Order, OrderItem, Menu

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "created_at")
    search_fields = ("name",)

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("name", "restaurant")
    list_filter = ("restaurant",)
@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "menu")
    list_filter = ("menu__restaurant",)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "category")
    list_filter = ("category","category__menu", "category__menu__restaurant",)

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("number", "restaurant")
    list_filter = ("restaurant",)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("table", "created_at", "status")
    list_filter = ("status", "table__restaurant")

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "item", "quantity", "restaurant_name")
    list_filter = ("order__table__restaurant",)

    @admin.display(description="Restaurant")
    def restaurant_name(self, obj):
        return obj.order.table.restaurant.name
