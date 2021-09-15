from django.db import models
from django.urls import reverse_lazy

class CategoryModel(models.Model):

    name = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, allow_unicode=True, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='category_images', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        pass
        # return reverse_lazy('', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class ProductModel(models.Model):
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    dsecription = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='product_images', null=True, blank=True)
    price = models.IntegerField( null=True, blank=True)
    sale = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    liked = models.IntegerField(default=0, blank=True, null=True)
    in_stock = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        pass
        # return reverse_lazy('', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


