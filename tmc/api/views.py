from rest_framework.response import Response
from rest_framework.views import APIView

from api import serializers, services


class TMCView(APIView):
    """
    View to get the TMC (tasa maxima convencional) from the SBIF.
    """

    def get(self, request, format=None):
        """
        Return the TMC of a specific date from the SBIF.

        TODO(lukas): document the fields.
        """
        serializer = serializers.TMCSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        tmc = services.get_sbif_tmc(
            credit_amount_uf=data["credit_amount_uf"],
            credit_term_days=data["credit_term_days"],
            valid_at=data["valid_at"],
            operation_type=data["operation_type"],
        )
        data["tmc"] = tmc
        return Response(data=data)
