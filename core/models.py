from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Расширенная модель пользователя"""
    phone = models.CharField(_('Телефон'), max_length=20, blank=True)
    address = models.TextField(_('Адрес доставки'), blank=True)
    
    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def __str__(self):
        return self.username


class Category(models.Model):
    """Категория товаров"""
    name = models.CharField(_('Название'), max_length=100)
    slug = models.SlugField(_('Slug'), max_length=100, unique=True)
    
    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """Товар/Букет"""
    name = models.CharField(_('Название'), max_length=200)
    slug = models.SlugField(_('Slug'), max_length=200, unique=True)
    description = models.TextField(_('Описание'), blank=True)
    price = models.DecimalField(_('Цена'), max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, 
                                 verbose_name=_('Категория'), related_name='products')
    image = models.ImageField(_('Изображение'), upload_to='products/', blank=True)
    available = models.BooleanField(_('В наличии'), default=True)
    created = models.DateTimeField(_('Создан'), auto_now_add=True)
    updated = models.DateTimeField(_('Обновлен'), auto_now=True)
    
    class Meta:
        verbose_name = _('Товар')
        verbose_name_plural = _('Товары')
        ordering = ['-created']
    
    def __str__(self):
        return self.name


class Order(models.Model):
    """Заказ"""
    class Status(models.TextChoices):
        NEW = 'new', _('Новый')
        PAID = 'paid', _('Оплачен')
        DELIVERING = 'delivering', _('В доставке')
        COMPLETED = 'completed', _('Завершен')
    
    order_number = models.CharField(_('Номер заказа'), max_length=20, unique=True)
    status = models.CharField(_('Статус'), max_length=20, choices=Status.choices, default=Status.NEW)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                             verbose_name=_('Пользователь'), related_name='orders')
    first_name = models.CharField(_('Имя'), max_length=100)
    last_name = models.CharField(_('Фамилия'), max_length=100)
    email = models.EmailField(_('Email'))
    phone = models.CharField(_('Телефон'), max_length=20)
    address = models.TextField(_('Адрес доставки'))
    delivery_date = models.DateField(_('Дата доставки'))
    delivery_time = models.TimeField(_('Время доставки'))
    comment = models.TextField(_('Комментарий'), blank=True)
    total_amount = models.DecimalField(_('Итоговая сумма'), max_digits=10, decimal_places=2)
    stripe_payment_id = models.CharField(_('ID платежа Stripe'), max_length=100, blank=True)
    created = models.DateTimeField(_('Создан'), auto_now_add=True)
    updated = models.DateTimeField(_('Обновлен'), auto_now=True)
    
    class Meta:
        verbose_name = _('Заказ')
        verbose_name_plural = _('Заказы')
        ordering = ['-created']
    
    def __str__(self):
        return f'Заказ #{self.order_number}'


class OrderItem(models.Model):
    """Позиция заказа"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, 
                              verbose_name=_('Заказ'), related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, 
                                verbose_name=_('Товар'))
    quantity = models.PositiveIntegerField(_('Количество'), default=1)
    price = models.DecimalField(_('Цена'), max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = _('Позиция заказа')
        verbose_name_plural = _('Позиции заказа')
    
    def __str__(self):
        return f'{self.product.name} x {self.quantity}'
    
    def get_cost(self):
        return self.price * self.quantity