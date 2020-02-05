from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from api import serializers, services


class ServiceUnavailableException(APIException):
    status_code = 503
    default_detail = "Service temporarily unavailable, try again later."
    default_code = "service_unavailable"


class TMCView(APIView):
    """
    View to get the TMC (tasa maxima convencional) from the SBIF.
    """

    def get(self, request, format=None):
        """
        Return the TMC of a specific date from the SBIF.
        """
        serializer = serializers.TMCSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            tmc = services.get_sbif_tmc(
                credit_amount_uf=data["credit_amount_uf"],
                credit_term_days=data["credit_term_days"],
                valid_at=data["valid_at"],
                operation_type=data["operation_type"],
            )
        except services.ExternalServiceError:
            error_msg = (
                "It seems that SBIF service is unavailable,"
                " try again later or see the logs."
            )
            raise ServiceUnavailableException(detail=error_msg)
        data["tmc"] = tmc
        return Response(data=data)
