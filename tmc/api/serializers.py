import datetime

from rest_framework import serializers

from api.services import SBIF_TMC_OPERATION_TYPES


class TMCSerializer(serializers.Serializer):
    credit_amount_uf = serializers.DecimalField(
        max_digits=8, decimal_places=2, min_value=0
    )
    credit_term_days = serializers.IntegerField(min_value=1)
    operation_type = serializers.CharField(default="non_adjustable")
    valid_at = serializers.CharField(max_length=10)
    tmc = serializers.DecimalField(
        max_digits=4, decimal_places=2, required=False, min_value=0
    )

    def validate_valid_at(self, value):
        try:
            datetime.datetime.strptime(value, "%d/%m/%Y")
        except ValueError:
            raise serializers.ValidationError(
                "valid_at field '{}' does not match format '%d/%m/%Y'".format(
                    value
                )
            )
        return value

    def validate_operation_type(self, value):
        value = value.lower().strip()
        if value not in SBIF_TMC_OPERATION_TYPES:
            raise serializers.ValidationError(
                "'{}' is not a valid operation type".format(value)
            )
        return value
