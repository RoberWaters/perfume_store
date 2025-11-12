from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Perfume, Category, Brand, Cart, CartItem, Review

def home(request):
    featured_perfumes = Perfume.objects.filter(is_active=True, featured=True)[:6]
    categories = Category.objects.filter(is_active=True)
    return render(request, 'shop/home.html', {
        'featured_perfumes': featured_perfumes,
        'categories': categories
    })

def perfume_list(request):
    perfumes = Perfume.objects.filter(is_active=True)
    category_slug = request.GET.get('category')
    brand_id = request.GET.get('brand')
    gender = request.GET.get('gender')
    
    if category_slug:
        perfumes = perfumes.filter(category__slug=category_slug)
    if brand_id:
        perfumes = perfumes.filter(brand_id=brand_id)
    if gender:
        perfumes = perfumes.filter(gender=gender)
    
    categories = Category.objects.filter(is_active=True)
    brands = Brand.objects.filter(is_active=True)
    
    return render(request, 'shop/perfume_list.html', {
        'perfumes': perfumes,
        'categories': categories,
        'brands': brands
    })

def perfume_detail(request, slug):
    perfume = get_object_or_404(Perfume, slug=slug, is_active=True)
    reviews = perfume.reviews.all().order_by('-created_at')
    
    if request.method == 'POST' and request.user.is_authenticated:
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        Review.objects.create(
            perfume=perfume,
            user=request.user,
            rating=rating,
            comment=comment
        )
        messages.success(request, 'Reseña agregada exitosamente')
        return redirect('shop:perfume_detail', slug=slug)
    
    return render(request, 'shop/perfume_detail.html', {
        'perfume': perfume,
        'reviews': reviews
    })

@login_required
def add_to_cart(request, perfume_id):
    perfume = get_object_or_404(Perfume, id=perfume_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, perfume=perfume)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f'{perfume.name} agregado al carrito')
    return redirect('shop:cart')

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'shop/cart.html', {'cart': cart})

@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    action = request.POST.get('action')
    
    if action == 'increase':
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    elif action == 'remove':
        cart_item.delete()
    
    return redirect('shop:cart')
