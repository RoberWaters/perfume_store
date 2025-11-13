from django import forms
from .models import Perfume, Category, Brand

class PerfumeForm(forms.ModelForm):
    class Meta:
        model = Perfume
        fields = [
            'name', 'description', 'price', 'stock_quantity', 'image',
            'category', 'brand', 'volume_ml', 'gender', 'fragrance_family',
            'is_active', 'featured'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del perfume'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descripción detallada'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'brand': forms.Select(attrs={'class': 'form-control'}),
            'volume_ml': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '100'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'fragrance_family': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Floral, Amaderado, Cítrico'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': 'Nombre',
            'description': 'Descripción',
            'price': 'Precio',
            'stock_quantity': 'Cantidad en Stock',
            'image': 'Imagen',
            'category': 'Categoría',
            'brand': 'Marca',
            'volume_ml': 'Volumen (ml)',
            'gender': 'Género',
            'fragrance_family': 'Familia Olfativa',
            'is_active': 'Activo',
            'featured': 'Destacado',
        }
