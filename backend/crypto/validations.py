from jsonschema import validate
from jsonschema.exceptions import ValidationError
from rest_framework import serializers


class JsonSchemaValidator:
    @staticmethod
    def validate(data, schema):
        try:
            validate(data, schema)
        except ValidationError as e:
            serializers.ValidationError('Schema error', e.message)