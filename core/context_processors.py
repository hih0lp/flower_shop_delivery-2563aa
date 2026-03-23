from .cart import Cart


def cart_count(request):
    """Контекстный процессор для количества товаров в корзине"""
    cart = Cart(request)
    return {'cart_count': len(cart)}