# BSC TechPeru — Prototipo interactivo de gestión estratégica

## Ejecutar
1. Descomprime `BSC_Prototipo.zip`.
2. Abre `index.html` con Chrome, Edge, Firefox o Safari.
3. Credenciales de demostración:
   - Administrador: `admin@demo.com` / `BSC2026!`
   - Gerente: `gerente@demo.com` / `BSC2026!`
   - Responsable: `responsable@demo.com` / `BSC2026!`

El proyecto usa HTML, CSS y JavaScript sin proceso de compilación. Chart.js se carga desde CDN para gráficos; si no hay conexión a Internet, la aplicación y los módulos CRUD siguen funcionando, pero los gráficos pueden no mostrarse.

## Estructura
- `index.html`: acceso y shell de la aplicación.
- `css/styles.css`: estilos responsivos.
- `js/data.js`: datos generados desde el Excel.
- `tools/excel_a_datos.py`: conversor Excel → `js/data.js`.
- `js/app.js`: lógica de negocio, navegación, formularios, persistencia y exportación.
- `html/`: carpeta reservada para ampliar pantallas HTML independientes si se requiere separar la SPA en páginas físicas.

## Módulos
Dashboard, **BSC Completo (hoja tipo Excel)**, mapa estratégico, objetivos, KPI, registro de mediciones, iniciativas, reportes y administración.

## Datos: integración con el Excel (v4)
Los datos provienen de `BSC_TechPeru_Ampliado_2025.xlsx` (TechPeru SAC · 4 perspectivas · 12 objetivos · 36 KPI) y se cargan desde `js/data.js`.
Para regenerar `js/data.js` tras cambiar el Excel: `python3 tools/excel_a_datos.py ruta/BSC_TechPeru_Ampliado_2025.xlsx js/data.js` y luego "Restaurar datos del Excel" en Administración.

| Excel | Prototipo |
|---|---|
| Hoja `📊 BSC Completo` (Meta, Real) | Página **BSC Completo**: celdas azules editables, % y estado recalculados al instante |
| `% Cumpl. = ROUND(Real/Meta*100,1)` | `achievement()` en `js/app.js`, dirección "mayor es mejor" |
| KPI inverso `ROUND(Meta/Real*100,1)` (11 KPI) | dirección "menor es mejor"; el script la detecta leyendo la fórmula |
| Estado: ≥90 ✅ LOGRADO · 75–89,9 ⚠️ EN RIESGO · <75 ❌ CRÍTICO | `statusOf()`; umbrales 90/75 editables por KPI |
| Hoja `📈 Dashboard` (semáforo e índice global) | Dashboard: índice global, contadores y tablero por perspectiva (ahora calculados, no texto fijo) |
| Columna "Análisis / Acción Recomendada" | Campo `action` del KPI (detalle, edición y exportación CSV) |

Con los datos del Excel el prototipo reproduce exactamente: índice global **84,2 %**, **11** logrados, **19** en riesgo, **6** críticos, y el % de los 36 KPI.

## Lógica de cumplimiento
- Mayor es mejor: `Real ÷ Meta × 100`. Menor es mejor: `Meta ÷ Real × 100`. Redondeo a 1 decimal (como `ROUND(...,1)` del Excel) y tope configurable (por defecto 150 %, Administración).
- Rango: 100 % dentro del rango y disminución proporcional fuera de sus límites.
- Estados: Logrado ≥ umbral Logrado (90); En riesgo ≥ umbral En riesgo (75); Crítico por debajo.
- Cumplimiento global: promedio ponderado KPI → objetivo → perspectiva (25 % c/u). Con los pesos iguales del Excel equivale a su promedio simple de 36 KPI (se muestra también como "Promedio simple (Excel)"). Un KPI sin dato queda fuera del cálculo.

### Diferencias deliberadas respecto al Excel
1. **Real = 0 en KPI inverso** (p. ej. 0 defectos): el Excel devuelve "-" y no lo evalúa; el prototipo lo trata como resultado perfecto (tope).
2. **Real vacío**: en el Excel la celda "-" se compara como texto y `"-">=90` es VERDADERO, por lo que un KPI sin dato aparecería ✅ LOGRADO; en el prototipo es "Sin datos" y no entra al promedio.
3. **Tope de cumplimiento**: el Excel no limita el %; el prototipo sí (configurable) para que un KPI sobresaliente no tape a los demás.

### Supuestos al cargar el Excel (el Excel no los trae)
Responsables y áreas por perspectiva (Finanzas, Comercial, Operaciones, Personas, asignados a usuarios demo); frecuencia "Anual"; prioridad "Media"; pesos iguales. Las 8 iniciativas son propuestas derivadas de las acciones recomendadas del Excel, con presupuesto S/ 0, avance 0 % y fechas 2026 por completar.

## Persistencia y límites
- Los datos se guardan en `localStorage` y la sesión de acceso en `sessionStorage`.
- La autenticación es simulada y las contraseñas de demostración están definidas en el código. No usar para producción.
- No hay backend, base de datos multiusuario ni control de acceso de servidor.
- Exportación CSV y JSON se realiza localmente. Imprimir permite usar la opción “Guardar como PDF” del navegador.

## Validación técnica realizada
El JavaScript se verifica con `node --check`. Este proyecto está diseñado para abrirse desde `index.html`; no requiere servidor local.
