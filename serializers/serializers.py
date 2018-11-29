from rest_framework import serializers


class DataManipulationSerializer(serializers.ModelSerializer):
    """
    :to_representation: to get represented/modified data during GET operation

    :example: here without 'to_representation' if we call serializer.data -
    created_at field will return default datetime format
    but we have converted created_at in timestamp.

    :UseCase: suppose we have passed the serializer in ListAPIView, so we don't have to
    manipulate data in our views after its being serialized .

    n.b: 'instance' in 'to_representation' will refer to a TestModel object.
    """

    class Meta:
        fields = (
            'field1',
            'field2',
            'created_at'
        )
        model = TestModel

    def to_representation(self, instance):
        data = {
            "id": instance.id,
            "field1": instance.field1,
            "field2": instance.field2,
            "created_at": int(instance.created_at.strftime("%s"))
        }
        return data


class AddExtraParameterSerializer(serializers.ModelSerializer):
    """
    :SerializerMethodField: To add extra field in serializer.

    :get_not_existed_field: 'self' contains a dictionary of input data

    :UseCase: suppose we have to accept a field during POST request but the field
    is not registered in model .And we will use the same serializer for both GET and POST request.
    1) we have to add the 'field name' of the extra field in 'fields' tuple
    2) in 'get_not_existed_field'(same as field name prefixed with get) we has to manage
    what to receive for requests.
    As here for POST request we will return the value to the view , but for GET request we will send None,
    as the field is not enlisted in model/database

    """
    id = serializers.IntegerField(required=True)
    not_existed_field = serializers.SerializerMethodField(default=None)  # serializers.CharField(required=True)

    class Meta:
        model = TestModel
        fields = ('id', 'field1', 'field2', 'not_existed_field')

    def get_not_existed_field(self, obj):
        try:
            print(self.initial_data['not_existed_field'])
            return self.initial_data['not_existed_field']
        except:
            return None
