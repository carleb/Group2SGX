from django.db import models


from django.urls import reverse


class Category(models.Model):

    name = models.CharField(max_length=250, db_index=True)

    slug = models.SlugField(max_length=250, unique=True)


    class Meta:

        verbose_name_plural = 'categories'


    def __str__(self):

        return self.name


    def get_absolute_url(self):

        return reverse('list-category', args=[self.slug])



class Product(models.Model):

    #FK

    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE, null=True)

    title = models.CharField(max_length=250)

    brand = models.CharField(max_length=250, default='un-branded')

    description = models.TextField(blank=True)

    slug = models.SlugField(max_length=255)

    price = models.DecimalField(max_digits=5, decimal_places=2)

    quantity = models.IntegerField(default=0)

    seller = models.CharField(max_length=250)

    image = models.FileField(upload_to='images/')


    class Meta:

        verbose_name_plural = 'products'

    def save(self, *args, **kwargs):
        # Ensure the slug is set before saving

        if not self.slug:
            self.slug = slugify(self.title)

        super(Product, self).save(*args, **kwargs)

    def __str__(self):

        return self.title



    def get_absolute_url(self):

        return reverse('product-info', args=[self.slug])



