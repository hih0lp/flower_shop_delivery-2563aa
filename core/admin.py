from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category, Product, Order, OrderItem


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('phone', 'address')}),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'available', 'created')
    list_filter = ('available', 'category', 'created')
    list_editable = ('price', 'available')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    raw_id_fields = ('category',)
    date_hierarchy = 'created'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',)
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'status', 'first_name', 'last_name', 
                    'total_amount', 'created')
    list_filter = ('status', 'created')
    search_fields = ('order_number', 'first_name', 'last_name', 'email')
    inlines = [OrderItemInline]
    readonly_fields = ('created', 'updated')
    fieldsets = (
        ('Основная информация', {
            'fields': ('order_number', 'status', 'user', 'total_amount', 'stripe_payment_id')
        }),
        ('Информация о клиенте', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'address')
        }),
        ('Доставка', {
            'fields': ('delivery_date', 'delivery_time', 'comment')
        }),
        ('Даты', {
            'fields': ('created', 'updated')
        }),
    )