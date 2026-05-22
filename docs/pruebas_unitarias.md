# Pruebas unitarias de `regulon_summary`

Este documento describe las **35 pruebas unitarias** implementadas con `pytest` para los módulos del paquete `src/`. Cada prueba se ejecuta de forma aislada con datos pequeños y verifica un comportamiento específico de una función.

## Ejecutar las pruebas

Desde la raíz del proyecto:

```bash
uv run pytest
```

Resultado esperado:

```text
35 passed
```

## Configuración necesaria

El archivo [`pyproject.toml`](../pyproject.toml) incluye:

```toml
[dependency-groups]
dev = ["pytest>=9.0.3"]

[tool.pytest.ini_options]
pythonpath = ["."]
```

La línea `pythonpath = ["."]` permite que pytest resuelva los imports del tipo `from src.<modulo> import ...` desde la raíz del proyecto. Todos los módulos en `src/` usan imports relativos (`from .core import ...`) para que el paquete sea consistente.

## Resumen por módulo

| Módulo probado | Archivo de pruebas | Nº de pruebas |
|---|---|---:|
| `src/core.py` | [`tests/test_core.py`](../tests/test_core.py) | 6 |
| `src/filters.py` | [`tests/test_filters.py`](../tests/test_filters.py) | 13 |
| `src/io_utils.py` | [`tests/test_io_utils.py`](../tests/test_io_utils.py) | 9 |
| `src/exporters.py` | [`tests/test_exporters.py`](../tests/test_exporters.py) | 7 |
| **Total** | | **35** |

---

## 1. `tests/test_core.py` (6 pruebas)

Pruebas para las funciones de lógica central: clasificación de reguladores y construcción del regulón.

### 1.1 `test_get_regulator_type_returns_activador`

- **Función probada:** `get_regulator_type()`.
- **Idea:** un regulador con `activados > 0` y `reprimidos == 0` debe clasificarse como `"activador"`.
- **Entrada:** `{"genes": ["lacZ", "araB"], "activados": 2, "reprimidos": 0}`.
- **Resultado esperado:** `"activador"`.

### 1.2 `test_get_regulator_type_returns_represor`

- **Función probada:** `get_regulator_type()`.
- **Idea:** un regulador con `activados == 0` y `reprimidos > 0` debe clasificarse como `"represor"`.
- **Entrada:** `{"genes": ["lacZ", "araB"], "activados": 0, "reprimidos": 2}`.
- **Resultado esperado:** `"represor"`.

### 1.3 `test_get_regulator_type_returns_dual`

- **Función probada:** `get_regulator_type()`.
- **Idea:** un regulador con `activados > 0` y `reprimidos > 0` debe clasificarse como `"dual"`.
- **Entrada:** `{"genes": ["lacZ", "araB"], "activados": 1, "reprimidos": 1}`.
- **Resultado esperado:** `"dual"`.

### 1.4 `test_build_regulon`

- **Función probada:** `build_regulon()`.
- **Idea:** dada una lista de interacciones, el regulón debe agrupar genes por TF y contar correctamente activaciones y represiones.
- **Entrada:**
  ```python
  [("CRP", "lacZ", "+"), ("CRP", "cyaA", "-"), ("FNR", "narG", "-")]
  ```
- **Resultado esperado:** `CRP` con `["lacZ", "cyaA"]`, `1` activado y `1` reprimido; `FNR` con `["narG"]`, `0` activados y `1` reprimido.

### 1.5 `test_build_regulon_with_duplicates`

- **Función probada:** `build_regulon()`.
- **Idea:** verifica el conteo correcto de activación y represión para un mismo TF con varios genes distintos.
- **Entrada:** `[("CRP", "lacZ", "+"), ("CRP", "cyaA", "-")]`.
- **Resultado esperado:** `CRP` con dos genes (`["lacZ", "cyaA"]`), `1` activado y `1` reprimido.
- **Nota:** el nombre del test menciona "duplicates", pero los genes de la entrada no están duplicados. Para cubrir genes repetidos del mismo TF (caso mencionado en la guía), conviene agregar un test adicional, por ejemplo con `[("CRP", "lacZ", "+"), ("CRP", "lacZ", "+")]`.

### 1.6 `test_build_regulon_with_dual_effect`

- **Función probada:** `build_regulon()`.
- **Idea:** una interacción con efecto `"+-"` debe contar simultáneamente como activación y represión.
- **Entrada:** `[("AraC", "araB", "+-")]`.
- **Resultado esperado:** `AraC` con `["araB"]`, `1` activado y `1` reprimido.

---

## 2. `tests/test_filters.py` (13 pruebas)

Pruebas para `filter_by_min_genes()` y `filter_by_type()`. Todas usan reguladores pequeños construidos a mano para que el resultado esperado sea verificable directamente.

### 2.1 `test_filter_by_min_genes`

- **Función:** `filter_by_min_genes()`.
- **Idea:** sólo permanecen los reguladores con al menos `min_genes` genes.
- **Entrada:** regulón con `CRP` (2 genes) y `FNR` (1 gen); `min_genes=2`.
- **Esperado:** `CRP` se conserva, `FNR` se descarta.

### 2.2 `test_filter_by_type_dual`

- **Función:** `filter_by_type()`.
- **Idea:** sólo permanecen los reguladores cuyo tipo computado coincide con `"dual"`.
- **Entrada:** `CRP` (dual) y `FNR` (represor); tipo `"dual"`.
- **Esperado:** `CRP` se conserva, `FNR` se descarta.

### 2.3 `test_filter_by_min_genes_and_type`

- **Funciones:** `filter_by_min_genes()` seguido de `filter_by_type()`.
- **Idea:** combinar ambos filtros produce un regulón que cumple las dos condiciones.
- **Entrada:** regulón con `CRP` (dual, 2 genes), `FNR` (represor, 1 gen), `ArcA` (represor, 1 gen); `min_genes=2` y tipo `"dual"`.
- **Esperado:** sólo queda `CRP`.

### 2.4 `test_filter_by_min_genes_zero`

- **Función:** `filter_by_min_genes()`.
- **Idea:** `min_genes=0` no descarta a nadie.
- **Esperado:** ambos reguladores se conservan.

### 2.5 `test_filter_by_min_genes_negative`

- **Función:** `filter_by_min_genes()`.
- **Idea:** un umbral negativo (`-1`) se comporta como `0`: tampoco descarta a nadie.
- **Esperado:** ambos reguladores se conservan.
- **Nota:** la guía de uso indica que `min_genes < 0` debería ser tratado como error en la capa de CLI. Esta prueba documenta que `filter_by_min_genes()` por sí misma no valida el signo.

### 2.6 `test_filter_by_min_genes_no_regulons`

- **Función:** `filter_by_min_genes()`.
- **Idea:** filtrar un regulón vacío devuelve un diccionario vacío.

### 2.7 `test_filter_by_type_no_regulons`

- **Función:** `filter_by_type()`.
- **Idea:** filtrar un regulón vacío devuelve un diccionario vacío.

### 2.8 `test_filter_by_type_no_matches`

- **Función:** `filter_by_type()`.
- **Idea:** si ningún regulador coincide con el tipo solicitado, se devuelve `{}`.
- **Entrada:** `CRP` (dual) y `FNR` (represor); tipo `"activator"` (cadena que no existe en el dominio: los tipos válidos son `"activador"`, `"represor"`, `"dual"`).
- **Esperado:** `{}`.

### 2.9 `test_filter_by_type_invalid_type`

- **Función:** `filter_by_type()`.
- **Idea:** si se pasa un tipo desconocido, se devuelve `{}` sin lanzar excepción.
- **Entrada:** mismo regulón; tipo `"invalid_type"`.
- **Esperado:** `{}`.
- **Nota:** esta prueba y la 2.8 cubren esencialmente el mismo comportamiento (tipo no válido → `{}`). Se mantienen separadas para distinguir "tipo plausible pero erróneo" (`"activator"` en lugar de `"activador"`) y "tipo claramente inválido".

### 2.10 `test_filter_by_min_genes_and_type_no_matches`

- **Funciones:** ambas, en cadena.
- **Idea:** si el filtro por `min_genes` ya elimina al único regulador dual, el filtrado posterior por tipo devuelve `{}`.
- **Entrada:** `CRP` (dual, 2 genes), `FNR` (represor, 1 gen); `min_genes=3` y tipo `"dual"`.
- **Esperado:** `{}`.

### 2.11 `test_filter_by_min_genes_and_type_all_matches`

- **Funciones:** ambas, en cadena.
- **Idea:** umbral bajo seguido del filtro de tipo deja sólo a los del tipo solicitado.
- **Entrada:** `CRP` (dual, 2 genes), `FNR` (represor, 1 gen); `min_genes=1` y tipo `"dual"`.
- **Esperado:** sólo `CRP`.

### 2.12 `test_filter_by_min_genes_keeps_only_regulators_with_enough_genes`

- **Función:** `filter_by_min_genes()`.
- **Idea:** versión con tres reguladores; sólo el de 2 genes se conserva con `min_genes=2`.
- **Esperado:** `CRP` se conserva; `FNR` y `ArcA` se descartan.

### 2.13 `test_filter_by_type_keeps_only_regulators_of_specified_type`

- **Función:** `filter_by_type()`.
- **Idea:** versión con tres reguladores; sólo el `dual` se conserva.
- **Esperado:** `CRP` se conserva; `FNR` y `ArcA` se descartan.

---

## 3. `tests/test_io_utils.py` (9 pruebas)

Pruebas para `load_interactions()`. Todas usan el fixture `tmp_path` de pytest para crear archivos TSV temporales que se eliminan automáticamente al terminar la prueba. El formato esperado por la función es de 7 columnas: `id, TF, x, x, gene, effect, x`.

### 3.1 `test_load_interactions_happy_path`

- **Idea:** dos líneas válidas producen dos tuplas `(TF, gen, efecto)` en el orden de aparición.
- **Esperado:** `[("CRP", "lacZ", "+"), ("FNR", "narG", "-")]`.

### 3.2 `test_load_interactions_keeps_dual_effect`

- **Idea:** el efecto `"+-"` (regulación dual) es válido y se conserva.
- **Esperado:** `("AraC", "araB", "+-")` aparece en el resultado.

### 3.3 `test_load_interactions_ignores_invalid_effect`

- **Idea:** los efectos fuera de `{"+", "-", "+-"}` (por ejemplo `"?"`) se descartan.
- **Esperado:** sólo la línea válida queda en la lista.

### 3.4 `test_load_interactions_ignores_empty_lines`

- **Idea:** las líneas en blanco no producen interacciones.
- **Esperado:** sólo la línea con datos queda en la lista.

### 3.5 `test_load_interactions_ignores_comments`

- **Idea:** las líneas que comienzan con `#` se ignoran.
- **Esperado:** sólo la línea con datos queda en la lista.

### 3.6 `test_load_interactions_ignores_header`

- **Idea:** la línea de encabezado de RegulonDB (`1)regulatorId\t...`) se descarta.
- **Esperado:** sólo la línea de datos queda en la lista.

### 3.7 `test_load_interactions_ignores_short_lines`

- **Idea:** una línea con menos de 7 columnas se descarta porque no contiene todos los campos esperados.
- **Entrada:** una línea de 5 columnas y otra de 7.
- **Esperado:** sólo la línea de 7 columnas produce una tupla.

### 3.8 `test_load_interactions_empty_filename_raises_value_error`

- **Idea:** llamar a `load_interactions("")` lanza `ValueError`.
- **Esperado:** la prueba pasa si se eleva la excepción dentro del `with pytest.raises(ValueError)`.

### 3.9 `test_load_interactions_does_not_validate_empty_tf_or_gene`

- **Idea (HALLAZGO):** la implementación actual de `load_interactions()` sólo valida la columna `effect`. No descarta líneas con TF o gene vacíos.
- **Entrada:** una línea con TF vacío y otra con gene vacío.
- **Esperado:** ambas tuplas `("", "someGene", "+")` y `("CRP", "", "+")` aparecen en el resultado.
- **Importante:** esta prueba **documenta la conducta actual**, no la valida como correcta. Si en el futuro se considera un bug, hay que:
  1. Agregar validación en `src/io_utils.py` (descartar TF/gene vacío).
  2. Reemplazar este test por aserciones de tipo `assert ("", ..., "+") not in interactions`.

---

## 4. `tests/test_exporters.py` (7 pruebas)

Pruebas para `write_summary()` y `write_sif()`. Todas usan `tmp_path` para escribir en archivos temporales y luego releer el contenido para verificarlo.

### 4.1 `test_write_summary`

- **Función:** `write_summary()`.
- **Idea:** el archivo TSV generado tiene el encabezado correcto y una fila por cada TF con sus contadores y la lista de genes ordenada alfabéticamente.
- **Entrada:** regulón con `CRP` (dual, 2 genes) y `FNR` (represor, 1 gen).
- **Esperado (líneas exactas):**
  ```text
  TF	Total genes	Activados	Reprimidos	Tipo	Lista de genes
  CRP	2	1	1	dual	cyaA, lacZ
  FNR	1	0	1	represor	narG
  ```
- **Nota:** la lista de genes se presenta ordenada (`cyaA, lacZ`), no en orden de inserción.

### 4.2 `test_write_sif`

- **Función:** `write_sif()`.
- **Idea:** cada interacción se escribe como una línea `TF \t etiqueta \t gen`, donde la etiqueta depende del efecto:
  - `"+"` → `activates`
  - `"-"` → `represses`
  - `"+-"` → `regulates`
- **Entrada:** 3 interacciones de `CRP` y `FNR`.
- **Esperado:** 3 líneas en el archivo SIF, una por interacción.

### 4.3 `test_write_summary_empty_regulon`

- **Función:** `write_summary()`.
- **Idea:** con un regulón vacío `{}`, el archivo contiene únicamente el encabezado.
- **Esperado:** una sola línea con los nombres de columna.

### 4.4 `test_write_sif_empty_regulon`

- **Función:** `write_sif()`.
- **Idea:** con una lista de interacciones vacía `[]`, el archivo SIF queda vacío.
- **Esperado:** contenido `""` (tras hacer `.strip()`).

### 4.5 `test_write_summary_single_interaction`

- **Función:** `write_summary()`.
- **Idea:** verifica la escritura de un único regulador con un solo gen activado.
- **Entrada:** `CRP` con `["lacZ"]`, 1 activado, 0 reprimidos.
- **Esperado:** dos líneas — encabezado y `CRP\t1\t1\t0\tactivador\tlacZ`.

### 4.6 `test_write_sif_single_interaction`

- **Función:** `write_sif()`.
- **Idea:** una sola interacción produce una sola línea SIF.
- **Entrada:** `[("CRP", "lacZ", "+")]`.
- **Esperado:** una línea: `CRP\tactivates\tlacZ`.

### 4.7 `test_write_sif_writes_expected_interactions`

- **Función:** `write_sif()`.
- **Idea:** verifica el orden y contenido de varias interacciones (caso ya cubierto parcialmente por 4.2, aquí también se valida el conteo de líneas).
- **Entrada:** 3 interacciones.
- **Esperado:** 3 líneas exactas en el orden de entrada.

---

## 5. Cobertura conceptual

La siguiente tabla resume qué comportamientos del programa están protegidos por las pruebas.

| Comportamiento | Protegido por |
|---|---|
| Clasificación `activador` / `represor` / `dual` | 1.1, 1.2, 1.3 |
| Conteo de activaciones/represiones por TF | 1.4, 1.5, 1.6 |
| Efecto dual `"+-"` se cuenta como activación + represión | 1.6, 3.2 |
| Filtro `min_genes` con distintos umbrales | 2.1, 2.4, 2.5, 2.6, 2.12 |
| Filtro por tipo con valores válidos y desconocidos | 2.2, 2.7, 2.8, 2.9, 2.13 |
| Combinación de ambos filtros | 2.3, 2.10, 2.11 |
| Parsing de TSV de RegulonDB (formato de 7 columnas) | 3.1 a 3.7 |
| Manejo de errores en la lectura | 3.8 |
| Hallazgo: validación incompleta de TF/gene vacíos | 3.9 |
| Formato de salida `summary` (TSV con encabezado) | 4.1, 4.3, 4.5 |
| Formato de salida `sif` con etiquetas `activates`/`represses`/`regulates` | 4.2, 4.4, 4.6, 4.7 |

## 6. Casos sugeridos para futuras pruebas

Aspectos del comportamiento no cubiertos aún que valdría la pena agregar:

- **Genes repetidos para un mismo TF:** verificar que `build_regulon()` no duplica el mismo gen en la lista. La prueba 1.5 sugiere este caso por su nombre pero no lo ejecuta.
- **`filter_by_type()` con `regulator_type=None`:** la guía lo menciona explícitamente. Conviene cubrir que `None` deja pasar todos los reguladores.
- **`filter_interactions_by_regulon()`:** función auxiliar usada en [`src/regulon_summary.py:63`](../src/regulon_summary.py#L63). Aún no tiene cobertura.
- **`write_summary()` con `regulon=None` o `output_file=""`:** la guía sugiere verificar que estos casos eleven una excepción.
- **Interacción con efecto `"+-"` en `write_sif()`:** ninguna de las 4.x usa el efecto dual; convendría agregar uno que verifique la etiqueta `regulates`.
