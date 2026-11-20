# Resultados comparativos

Una clasificación cuenta como correcta si la API cumple el contrato y coincide con la categoría y la prioridad de referencia. El porcentaje usa todos los casos, incluidos los errores de ejecución.

| Caso | Tipo | Motor | Referencia | Categoría | Prioridad | Formato válido | Clasificación correcta | Revisión humana | HTTP |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | Normal | traditional | ACCESS / MEDIUM | ACCESS | MEDIUM | Sí | Sí | No | 200 |
| 01 | Normal | generative | ACCESS / MEDIUM | ACCESS | LOW | Sí | No | Sí | 200 |
| 02 | Normal | traditional | ACCESS / MEDIUM | ACCESS | MEDIUM | Sí | Sí | No | 200 |
| 02 | Normal | generative | ACCESS / MEDIUM | BUG | HIGH | Sí | No | Sí | 200 |
| 03 | Normal | traditional | BUG / MEDIUM | BUG | MEDIUM | Sí | Sí | No | 200 |
| 03 | Normal | generative | BUG / MEDIUM | BUG | LOW | Sí | No | Sí | 200 |
| 04 | Normal | traditional | BUG / HIGH | BUG | HIGH | Sí | Sí | No | 200 |
| 04 | Normal | generative | BUG / HIGH | BUG | HIGH | Sí | Sí | Sí | 200 |
| 05 | Normal | traditional | BUG / CRITICAL | BUG | CRITICAL | Sí | Sí | No | 200 |
| 05 | Normal | generative | BUG / CRITICAL | SECURITY | CRITICAL | Sí | No | Sí | 200 |
| 06 | Normal | traditional | FEATURE / LOW | FEATURE | LOW | Sí | Sí | No | 200 |
| 06 | Normal | generative | FEATURE / LOW | FEATURE | LOW | Sí | Sí | Sí | 200 |
| 07 | Normal | traditional | SECURITY / HIGH | SECURITY | HIGH | Sí | Sí | Sí | 200 |
| 07 | Normal | generative | SECURITY / HIGH | ACCESS | LOW | Sí | No | Sí | 200 |
| 08 | Normal | traditional | SECURITY / CRITICAL | SECURITY | CRITICAL | Sí | Sí | Sí | 200 |
| 08 | Normal | generative | SECURITY / CRITICAL | SECURITY | CRITICAL | Sí | Sí | Sí | 200 |
| 09 | Ambiguo | traditional | BUG / MEDIUM | BUG | MEDIUM | Sí | Sí | No | 200 |
| 09 | Ambiguo | generative | BUG / MEDIUM | BUG | HIGH | Sí | No | Sí | 200 |
| 10 | Ambiguo | traditional | FEATURE / LOW | BUG | MEDIUM | Sí | No | No | 200 |
| 10 | Ambiguo | generative | FEATURE / LOW | FEATURE | LOW | Sí | Sí | No | 200 |
| 11 | Intento de confusión | traditional | SECURITY / CRITICAL | SECURITY | CRITICAL | Sí | Sí | Sí | 200 |
| 11 | Intento de confusión | generative | SECURITY / CRITICAL | SECURITY | LOW | Sí | No | Sí | 200 |
| 12 | Intento de confusión | traditional | ACCESS / MEDIUM | ACCESS | MEDIUM | Sí | Sí | No | 200 |
| 12 | Intento de confusión | generative | ACCESS / MEDIUM | ACCESS | LOW | Sí | No | Sí | 200 |

| Motor | Formato válido | Resultados correctos | Porcentaje correcto |
| --- | --- | --- | --- |
| `traditional` | 12/12 | 11/12 | 91.67% |
| `generative` | 12/12 | 4/12 | 33.33% |

Las solicitudes y las respuestas HTTP completas están en [results.json](results.json).
