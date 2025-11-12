from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem
from shop.models import Cart

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    
    if not cart.items.exists():
        messages.warning(request, 'Tu carrito está vacío')
        return redirect('shop:cart')
    
    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            total_amount=cart.get_total(),
            shipping_address=request.POST.get('address'),
            shipping_city=request.POST.get('city'),
            shipping_state=request.POST.get('state'),
            shipping_postal_code=request.POST.get('postal_code'),
            payment_method=request.POST.get('payment_method', 'Efectivo'),
            notes=request.POST.get('notes', '')
        )
        
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                perfume=item.perfume,
                quantity=item.quantity,
                price=item.perfume.price,
                subtotal=item.get_subtotal()
            )
            
            # Actualizar inventario
            item.perfume.stock_quantity -= item.quantity
            item.perfume.save()
        
        cart.items.all().delete()
        messages.success(request, f'Pedido {order.order_number} creado exitosamente')
        return redirect('orders:order_detail', order_number=order.order_number)
    
    return render(request, 'orders/checkout.html', {'cart': cart})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})
