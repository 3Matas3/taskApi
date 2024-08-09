from django.apps import apps
from django.db import transaction
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from taskApi.api.models import (
    Attribute,
    AttributeName,
    AttributeValue,
    Catalog,
    Image,
    Product,
    ProductAttributes,
    ProductImage,
)
from taskApi.api.serializers import (
    AttributeNameSerializer,
    AttributeSerializer,
    AttributeSerializerDetail,
    AttributeValueSerializer,
    CatalogSerializer,
    CatalogSerializerDetail,
    ImageSerializer,
    ProductAttributesSerializer,
    ProductAttributesSerializerDetail,
    ProductImageSerializer,
    ProductImageSerializerDetail,
    ProductSerializer,
)


def get_model_class(model_name: str, detail: bool = False) -> tuple:
    """
    Function to get model class and serializer class based on name.
    Raise exception if model not found. Function will return Detail serializer for detail view

    :param model_name:
    :param detail:
    :return:
    """
    model_classes = {
        "AttributeName": (AttributeName, AttributeNameSerializer),
        "AttributeValue": (AttributeValue, AttributeValueSerializer),
        "Attribute": (Attribute, AttributeSerializerDetail if detail else AttributeSerializer),
        "Product": (Product, ProductSerializer),
        "ProductAttributes": (
            ProductAttributes,
            ProductAttributesSerializerDetail if detail else ProductAttributesSerializer,
        ),
        "Image": (Image, ImageSerializer),
        "ProductImage": (ProductImage, ProductImageSerializerDetail if detail else ProductImageSerializer),
        "Catalog": (Catalog, CatalogSerializerDetail if detail else CatalogSerializer),
    }
    if model_name in model_classes:
        return model_classes[model_name]

    raise ValidationError(detail=f"No model class found with name: {model_name}")


@api_view(["POST"])
def import_data(request):
    data = request.data

    # input must a valid list of json
    if not isinstance(data, list):
        raise ValidationError(detail=f"Please send a valid list of json")

    with transaction.atomic():
        for item in data:
            # input must a valid list of json
            if not isinstance(item, dict) or not item:
                raise ValidationError(detail="Please send a valid list with json data")

            for model_name, fields in item.items():
                model, model_serializer_class = get_model_class(model_name)
                model_serializer_class = model_serializer_class(model(), data=fields)
                if not model_serializer_class.is_valid(raise_exception=True):
                    raise ValidationError(detail="Please send a valid data")
                else:
                    model_serializer_class.save()

    if len(data) == 0:
        status_code = status.HTTP_200_OK
    else:
        status_code = status.HTTP_201_CREATED

    return Response({"success": True, "imported_count": len(data)}, status=status_code)


class ModelListView(generics.ListAPIView):
    def get_queryset(self):
        model_name = self.kwargs["model_name"]
        try:
            model = apps.get_model("api", model_name)
            return model.objects.all()
        except LookupError:
            return []

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        model, serializer_class = get_model_class(self.kwargs["model_name"])
        if serializer_class is None:
            return Response({"error": "Invalid model name"}, status=400)
        serializer = serializer_class(queryset, many=True)

        return Response(serializer.data)


class DetailView(APIView):
    def get(self, request, model_name, pk):
        model_class, model_serializer = get_model_class(model_name, detail=True)
        try:
            record = model_class.objects.get(id=pk)
        except model_class.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = model_serializer(record)

        return Response(serializer.data)
