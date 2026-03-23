from decimal import Decimal
from django.conf import settings
from .models import Product


class Cart:
    """Класс для работы с сессионной корзиной"""
    
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    
    def add(self, product, quantity=1, override_quantity=False):
        """Добавить товар в корзину или обновить количество"""
        product_id = str(product.id)
        
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        
        self.save()
    
    def save(self):
        """Сохранить корзину в сессии"""
        self.session.modified = True
    
    def remove(self, product):
        """Удалить товар из корзины"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def __iter__(self):
        """Итерация по товарам в корзине"""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        
        for product in products:
            cart[str(product.id)]['product'] = product
        
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
    
    def __len__(self):
        """Общее количество товаров в корзине"""
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        """Общая стоимость корзины"""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    def clear(self):
        """Очистить корзину"""
        del self.session[settings.CART_SESSION_ID]
        self.save()
    
    def get_cart_items(self):
        """Получить список товаров в корзине для создания OrderItem"""
        cart_items = []
        for product_id, item in self.cart.items():
            try:
                product = Product.objects.get(id=product_id)
                cart_items.append({
                    'product': product,
                    'quantity': item['quantity'],
                    'price': Decimal(item['price'])
                })
            except Product.DoesNotExist:
                continue
        return cart_items