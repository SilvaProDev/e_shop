from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

# Register your models here.
from product.models import Category, Produit, Image, Comment


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['titre', 'parent', 'status']
    list_filter = ['status']

class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "titre"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count', 'status')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('titre',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
            qs,
            Produit,
            'categorie',
            'products_cumulative_count',
            cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
            Produit,
            'categorie',
            'products_count',
            cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'


class ProduitImageInline(admin.TabularInline):
    model = Image
    extra = 5

class ProduitAdmin(admin.ModelAdmin):
    list_display = ['titre', 'categorie', 'status']
    list_filter = ['status']
    prepopulated_fields = {'slug': ('titre',)}
    # readonly_fields = (
    #     'image_tag',
    # )
    inlines = [ProduitImageInline]


class Commentdmin(admin.ModelAdmin):
    list_display = ['subject', 'comment', 'date_add', 'status']
    list_filter = ['status']
    readonly_fields = (
        'subject',
        'comment',
        'ip',
        'user',
        'produit',
        'rate',
    )
    
    

admin.site.register(Category, CategoryAdmin2)
admin.site.register(Produit, ProduitAdmin)
admin.site.register(Image)
admin.site.register(Comment, Commentdmin)
