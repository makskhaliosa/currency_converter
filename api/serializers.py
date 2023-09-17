from rest_framework import serializers

from .core.utils import get_currency_rate, validate_query
from .models import Rate


class RatesSerializer(serializers.Serializer):
    """Сериализатор для конвертации валют."""
    from_currency = serializers.CharField(required=True)
    to_currency = serializers.CharField(required=True)
    value = serializers.IntegerField(required=True)

    def to_representation(self, instance: Rate):
        from_cur = instance.from_currency.upper()
        to_cur = instance.to_currency.upper()
        value = int(instance.value) if instance.value else None
        validate_query(from_cur, to_cur, value)
        result = get_currency_rate(
            from_currency=from_cur,
            to_currency=to_cur,
            value=value)
        return {
            'result': result
        }
