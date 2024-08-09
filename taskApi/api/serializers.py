from rest_framework import serializers

from .const import EMPTY_STRINGS
from .models import (
    Attribute,
    AttributeName,
    AttributeValue,
    Catalog,
    Image,
    Product,
    ProductAttributes,
    ProductImage,
)


class BaseSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        if self.instance is None:
            self.instance = self.create(**self.validated_data)
        else:
            self.instance = self.update(self.instance, self.validated_data)

        self.instance.save()
        return self.instance

    def to_internal_value(self, data):
        for key, value in data.items():
            if value in EMPTY_STRINGS:
                raise serializers.ValidationError({key: "Invalid value for this field."})

        return super().to_internal_value(data)


class AttributeNameSerializer(BaseSerializer):
    id = serializers.IntegerField(min_value=1)
    nazev = serializers.CharField(source="name", required=False)
    kod = serializers.CharField(source="code", required=False)
    zobrazit = serializers.BooleanField(source="display", default=False)

    class Meta:
        model = AttributeName
        fields = ["id", "nazev", "kod", "zobrazit"]


class AttributeValueSerializer(BaseSerializer):
    id = serializers.IntegerField(min_value=1)
    hodnota = serializers.CharField(source="value")

    class Meta:
        model = AttributeValue
        fields = ["id", "hodnota"]


class AttributeSerializer(BaseSerializer):
    id = serializers.IntegerField(min_value=1)
    nazev_atributu_id = serializers.PrimaryKeyRelatedField(
        queryset=AttributeName.objects.all(), source="attribute_name"
    )
    hodnota_atributu_id = serializers.PrimaryKeyRelatedField(
        queryset=AttributeValue.objects.all(), source="attribute_value"
    )

    class Meta:
        model = Attribute
        fields = ["id", "nazev_atributu_id", "hodnota_atributu_id"]


class AttributeSerializerDetail(AttributeSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["AttributeName"] = AttributeNameSerializer(instance.attribute_name).data
        representation.pop("nazev_atributu_id")
        representation["AttributeValue"] = AttributeValueSerializer(instance.attribute_value).data
        representation.pop("hodnota_atributu_id")
        return representation


class ProductSerializer(BaseSerializer):
    id = serializers.IntegerField(min_value=1)
    nazev = serializers.CharField(source="name", max_length=255, required=False)
    cena = serializers.CharField(source="cost", max_length=255, required=False)
    mena = serializers.CharField(source="currency", required=False, max_length=4)
    description = serializers.CharField(required=False)
    published_on = serializers.DateTimeField(required=False, allow_null=True)
    is_published = serializers.BooleanField(default=False)

    class Meta:
        model = Product
        fields = ["id", "nazev", "description", "cena", "mena", "published_on", "is_published"]


class ProductAttributesSerializer(BaseSerializer):
    id = serializers.IntegerField(min_value=1)
    attribute = serializers.PrimaryKeyRelatedField(queryset=Attribute.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = ProductAttributes
        fields = ["id", "attribute", "product"]


class ProductAttributesSerializerDetail(ProductAttributesSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["Attribute"] = AttributeSerializerDetail(instance.attribute).data
        representation.pop("attribute")
        representation["Product"] = ProductSerializer(instance.product).data
        representation.pop("Product")
        return representation


class ImageSerializer(BaseSerializer):
    id = serializers.IntegerField(min_value=1)
    obrazek = serializers.URLField(required=True, source="image")

    class Meta:
        model = Image
        fields = ["id", "obrazek"]


class ProductImageSerializer(BaseSerializer):
    id = serializers.IntegerField()
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    obrazek_id = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all(), source="image")
    nazev = serializers.CharField(source="name", max_length=255, required=False)

    class Meta:
        model = ProductImage
        fields = ["id", "product", "obrazek_id", "nazev"]


class ProductImageSerializerDetail(ProductImageSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["Image"] = ImageSerializer(instance.image).data
        representation.pop("obrazek_id")
        representation["Product"] = ProductSerializer(instance.product).data
        representation.pop("product")
        return representation


class CatalogSerializer(BaseSerializer):
    id = serializers.IntegerField(min_value=1)
    nazev = serializers.CharField(source="name", max_length=255, required=False)
    obrazek_id = serializers.PrimaryKeyRelatedField(
        queryset=Image.objects.all(), source="image", required=False, allow_null=True
    )
    products_ids = serializers.PrimaryKeyRelatedField(
        source="products", many=True, queryset=Product.objects.all(), required=True
    )
    attributes_ids = serializers.PrimaryKeyRelatedField(
        source="attributes", many=True, queryset=Attribute.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Catalog
        fields = ["id", "nazev", "obrazek_id", "products_ids", "attributes_ids"]


class CatalogSerializerDetail(CatalogSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["Image"] = ImageSerializer(instance.image).data
        representation.pop("obrazek_id")
        representation["Attributes"] = AttributeSerializer(instance.attributes.all(), many=True).data
        representation.pop("attributes_ids")
        representation["Products"] = ProductSerializer(instance.products.all(), many=True).data
        representation.pop("products_ids")
        return representation
