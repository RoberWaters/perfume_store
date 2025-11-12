from django.shortcuts import render

def about_page(request):
    return render(request, 'about/about.html')

def faq_page(request):
    return render(request, 'about/faq.html')

def blog_page(request):
    return render(request, 'about/blog.html')

def contact_page(request):
    return render(request, 'about/contact.html')

