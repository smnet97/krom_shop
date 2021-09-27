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
    sale = models.BooleanField(default=False)
    liked = models.BooleanField(default=False)
    in_stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        pass
        # return reverse_lazy('', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class CartModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)

    def __str__(self):
        return self.product.name

    @property
    def get_total_price(self):
        return self.product.price * self.amount

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Cart List'


class FavoritesModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name


    class Meta:
        verbose_name = 'Favorite product'
        verbose_name_plural = 'Favorite Products'


class ShippingAddressModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=13)
    company = models.CharField(max_length=100, blank=True)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'Shipping Address'
        verbose_name_plural = 'Shipping Addresses'


class DeliveryCostModel(models.Model):
    delivery = models.IntegerField()

    def __str__(self):
        return str(self.delivery)

    class Meta:
        verbose_name = 'Delivery cost'
        verbose_name_plural = 'Delivery cost'


PAYMENT_TYPES = (
    (1, 'Оплата при доставке'),
    (2, 'Кредитная карта'),
    (3, 'Прямой банковский перевод'),
)

PAYMENT_STATUS = (
    (1, 'В ожидании'),
    (2, 'Ошибка'),
    (3, 'Завершено'),
    (4, 'Отменен'),
    (5, 'Истёк'),
    (6, 'Возвращен'),
)

DELIVERY_STATUS = (
    (1, 'В ожидании'),
    (2, 'На доставке'),
    (3, 'Доставлен'),
    (4, 'Возвращен'),
)


class OrderModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.BigIntegerField(default=0)
    amount = models.IntegerField(null=True)
    phone = models.CharField(max_length=13)
    email = models.EmailField()
    payment_type = models.PositiveSmallIntegerField(choices=PAYMENT_TYPES)
    payment_status = models.PositiveSmallIntegerField(choices=PAYMENT_STATUS)
    delivery_status = models.PositiveSmallIntegerField(choices=DELIVERY_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def get_absolute_url(self):
        return reverse_lazy('shop:order-detail', kwargs={'pk': self.pk})


@receiver(pre_save, sender=CategoryModel)
def create_slug_from_name(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)
    