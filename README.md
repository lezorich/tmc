# API para obtener la tasa máxima convencional

Dado un monto en UF y el plazo en días de un crédito, esta API devuelve la tasa
máxima convencional (TMC) para una determinada fecha.

La API está implementada en [Django](https://www.djangoproject.com/) usando
la librería [Django REST Framework](https://www.django-rest-framework.org/).
Además tiene un frontend en Javascript.

## Documentación

### Autorización

La API no es pública y requiere de una API Key en los *headers* para se
autoricen las llamadas:

```
Authorization: Api-Key *****
```

Donde `*****` es la API Key.

En caso de que se haga una llamda y no se pueda autorizar, la API devuelve un
error `HTTP 403 Forbidden`.

### Obtener TMC

Para obtener la TMC, se hace un `GET` al endpoint `/api/v1/tmc/` con los
siguientes parámetros:

* `credit-amount-uf`: el monto del crédito en uf.
* `credit-term-days`: el plazo del crédito en días.
* `valid-at`: la fecha para la que se quiere obtener la TMC.
* `operation-type` (opcional): puede ser `adjustable` o `non_adjustable`
dependiendo si el crédito es una operación ajustable o no.

La respuesta es un objeto `JSON` con los parámetros de consulta (monto y plazo
del crédito, y fecha de consulta) y la TMC como un `float`:

* `credit_amount_uf`: `float`.
* `credit_term_days`: `int`.
* `valid_at`: `string` que representa la fecha en formato `dd/mm/yyyy`.
* `tmc`: `float`.

### Errores

* `HTTP 403 Forbidden`: en caso de que la API Key no sea válida.
* `HTTP 400 Bad Request`: en caso de que algún parámetro no corresponda al
formato que la API espera. Por ejemplo, en `credit-amount-uf` se entrega un
`string`.
* `HTTP 503 Service Unavailable`: en caso que la página del SBIF esté caída
o tenga problemas.

## Demo

### API

La API está alojada en Heroku en el `dyno` gratis.

**Importante**: La primera llamada puede demorarse hasta 30 segundos en
responder debido a que Heroku duerme las máquinas que no están siendo ocupadas
y tienen el `dyno` gratis.

Obtener TMC :

```
curl -X GET \
-H "Content-Type: application/json" \
-H "Authorization: Api-Key SWvVO8RF.ZoqHc8jCYel6FIZPtqUiTieJ829fRAVn" \
https://cumplo-challenge.herokuapp.com/api/v1/tmc/?credit-amount-uf=1000&credit-term-days=366&valid-at=1/1/2020&operation-type=non_adjustable
```

Respuesta:

```
{
    "credit_amount_uf": 1000.0,
    "credit_term_days": 366,
    "operation_type": "non_adjustable",
    "valid_at": "1/1/2020",
    "tmc": 19.23
}
```

Error en el formato de la fecha:

```
curl -X GET \
-H "Content-Type: application/json" \
-H "Authorization: Api-Key SWvVO8RF.ZoqHc8jCYel6FIZPtqUiTieJ829fRAVn" \
https://cumplo-challenge.herokuapp.com/api/v1/tmc/?credit-amount-uf=1000&credit-term-days=366&valid-at=1/1/20203&operation-type=non_adjustable
```

Respuesta:

```
{
    "valid_at": ["valid_at field '1/1/20203' does not match format '%d/%m/%Y'"]
}
```

### Frontend

Hay un frontend también para probar la API de forma más fácil:

[](https://cumplo-challenge.herokuapp.com)
