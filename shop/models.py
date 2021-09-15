from django.db import models
from django.urls import reverse_lazy
from django.template.defaultfilters import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
User = get_user_model()

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
    sale = models.BooleanField(default=False, null=True, blank=True)
    liked = models.BooleanField(default=False, blank=True, null=True)
    in_stock = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        pass
        # return reverse_lazy('', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class CartModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.OneToOneField(ProductModel, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)

    def __str__(self):
        return self.product.name

    def get_total_price(self):
        return self.product.price * self.amount

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Cart List'


@receiver(pre_save, sender=CategoryModel)
def create_slug_from_name(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)
    