# API de Scoring de Crédito

Esta API predice el riesgo crediticio de un cliente usando variables financieras y de comportamiento.

## Endpoints
- `/` → Verifica si la API está activa.
- `/predict` → Recibe un JSON con los datos del cliente y devuelve el score.

## Ejemplo de Request:
```json
{
  "edad": 35,
  "ingresos_mensual": 1500,
  "gastos_mensual": 400,
  "antiguedad_laboral": 24,
  "num_referencias": 3,
  "cuota_mensual": 250,
  "rcd": 0.2,
  "monto_ingreso_ratio": 0.5
}
