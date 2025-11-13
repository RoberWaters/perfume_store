from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Sum, Q
from .decorators import admin_required
from .models import Perfume, Category, Brand
from orders.models import Order, OrderItem
from .forms import PerfumeForm

@admin_required
def admin_dashboard(request):
    """Panel principal del administrador"""
    # Estadísticas generales
    total_perfumes = Perfume.objects.count()
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='Pendiente').count()
    total_revenue = Order.objects.filter(status__in=['Pagado', 'Enviado', 'Entregado']).aggregate(
        total=Sum('total_amount')
    )['total'] or 0

    # Órdenes recientes
    recent_orders = Order.objects.all()[:10]

    # Productos con bajo stock
    low_stock_perfumes = Perfume.objects.filter(stock_quantity__lt=10).order_by('stock_quantity')[:10]

    context = {
        'total_perfumes': total_perfumes,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
        'low_stock_perfumes': low_stock_perfumes,
    }
    return render(request, 'shop/admin/dashboard.html', context)

@admin_required
def admin_perfumes_list(request):
    """Listado de todos los perfumes"""
    query = request.GET.get('q', '')
    perfumes = Perfume.objects.all().select_related('category', 'brand').order_by('-created_at')

    if query:
        perfumes = perfumes.filter(
            Q(name__icontains=query) |
            Q(brand__name__icontains=query) |
            Q(category__name__icontains=query)
        )

    context = {
        'perfumes': perfumes,
        'query': query,
    }
    return render(request, 'shop/admin/perfumes_list.html', context)

@admin_required
def admin_perfume_add(request):
    """Agregar nuevo perfume"""
    if request.method == 'POST':
        form = PerfumeForm(request.POST, request.FILES)
        if form.is_valid():
            perfume = form.save()
            messages.success(request, f'Perfume "{perfume.name}" agregado exitosamente.')
            return redirect('shop:admin_perfumes_list')
    else:
        form = PerfumeForm()

    context = {'form': form}
    return render(request, 'shop/admin/perfume_form.html', context)

@admin_required
def admin_perfume_edit(request, pk):
    """Editar perfume existente"""
    perfume = get_object_or_404(Perfume, pk=pk)

    if request.method == 'POST':
        form = PerfumeForm(request.POST, request.FILES, instance=perfume)
        if form.is_valid():
            perfume = form.save()
            messages.success(request, f'Perfume "{perfume.name}" actualizado exitosamente.')
            return redirect('shop:admin_perfumes_list')
    else:
        form = PerfumeForm(instance=perfume)

    context = {'form': form, 'perfume': perfume}
    return render(request, 'shop/admin/perfume_form.html', context)

@admin_required
def admin_perfume_delete(request, pk):
    """Eliminar perfume"""
    perfume = get_object_or_404(Perfume, pk=pk)

    if request.method == 'POST':
        perfume_name = perfume.name
        perfume.delete()
        messages.success(request, f'Perfume "{perfume_name}" eliminado exitosamente.')
        return redirect('shop:admin_perfumes_list')

    context = {'perfume': perfume}
    return render(request, 'shop/admin/perfume_confirm_delete.html', context)

@admin_required
def admin_orders_list(request):
    """Listado de todas las órdenes"""
    status_filter = request.GET.get('status', '')
    query = request.GET.get('q', '')

    orders = Order.objects.all().select_related('user').prefetch_related('items__perfume')

    if status_filter:
        orders = orders.filter(status=status_filter)

    if query:
        orders = orders.filter(
            Q(order_number__icontains=query) |
            Q(user__username__icontains=query) |
            Q(user__email__icontains=query)
        )

    context = {
        'orders': orders,
        'status_filter': status_filter,
        'query': query,
        'status_choices': Order.STATUS_CHOICES,
    }
    return render(request, 'shop/admin/orders_list.html', context)

@admin_required
def admin_order_detail(request, pk):
    """Detalle de una orden específica"""
    order = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        new_status = request.POST.get('status')

        # Validar que la orden no esté ya cancelada
        if order.status == 'Cancelado':
            messages.error(request, '❌ No se puede cambiar el estado de una orden cancelada.')
            return redirect('shop:admin_order_detail', pk=pk)

        if new_status and new_status in dict(Order.STATUS_CHOICES):
            old_status = order.status

            # Si se está cancelando la orden, devolver el stock
            if new_status == 'Cancelado':
                for item in order.items.all():
                    perfume = item.perfume
                    perfume.stock_quantity += item.quantity
                    perfume.save()
                    messages.info(request, f'✅ Stock de "{perfume.name}" actualizado: +{item.quantity} unidades')

            order.status = new_status
            order.save()

            # Registrar cambio en historial
            from orders.models import OrderStatusHistory
            OrderStatusHistory.objects.create(
                order=order,
                old_status=old_status,
                new_status=new_status,
                changed_by=request.user
            )

            if new_status == 'Cancelado':
                messages.warning(request, f'⚠️ Orden {order.order_number} cancelada. El stock ha sido restaurado.')
            else:
                messages.success(request, f'Estado de la orden actualizado a "{new_status}".')

            return redirect('shop:admin_order_detail', pk=pk)

    context = {
        'order': order,
        'status_choices': Order.STATUS_CHOICES,
    }
    return render(request, 'shop/admin/order_detail.html', context)
