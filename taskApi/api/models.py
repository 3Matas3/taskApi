from django.db import models


class AttributeName(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, blank=True, null=True)
    display = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'attribute_name'


class AttributeValue(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.value

    class Meta:
        managed = True
        db_table = 'attribute_value'


class Attribute(models.Model):
    id = models.IntegerField(primary_key=True)
    attribute_name = models.ForeignKey(AttributeName, on_delete=models.CASCADE)
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'attribute'


class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    cost = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3)
    published_on = models.DateTimeField(blank=True, null=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'product'


class ProductAttributes(models.Model):
    id = models.IntegerField(primary_key=True)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product} - {self.attribute}"

    class Meta:
        managed = True
        db_table = 'product_attributes'


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.URLField()
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.image

    class Meta:
        managed = True
        db_table = 'image'


class ProductImage(models.Model):
    id = models.IntegerField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.product} - {self.name}"

    class Meta:
        managed = True
        db_table = 'product_image'


class Catalog(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True, blank=True)
    products = models.ManyToManyField(Product)
    attributes = models.ManyToManyField(Attribute)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'catalog'
