#!/usr/bin/env python3
"""Convierte BSC_TechPeru_Ampliado_2025.xlsx en js/data.js (window.BSC_SEED).

Uso:  python3 tools/excel_a_datos.py ruta/al/archivo.xlsx [js/data.js]

Qué lee del Excel (hoja '📊 BSC Completo'):
  - Perspectiva / Objetivo / KPI / Unidad / Meta / Real  (columnas B..G)
  - Si el KPI es INVERSO: se detecta leyendo la fórmula de % Cumpl. (col H):
        =ROUND(G/F*100,1) -> mayor es mejor  (Real / Meta)
        =ROUND(F/G*100,1) -> menor es mejor  (Meta / Real)
  - 'Análisis / Acción Recomendada' de las hojas de detalle (col I).
"""
import json, re, sys, openpyxl

src = sys.argv[1] if len(sys.argv) > 1 else "BSC_TechPeru_Ampliado_2025.xlsx"
dst = sys.argv[2] if len(sys.argv) > 2 else "js/data.js"
wb = openpyxl.load_workbook(src)  # fórmulas (para detectar KPIs inversos)
ws = next(s for s in wb if "BSC Completo" in s.title)

PERSP = {"FINANCIERA": "financiera", "CLIENTES": "clientes",
         "PROCESOS": "procesos", "APRENDIZAJE": "aprendizaje"}
DETAIL = {"financiera": "Financiera", "clientes": "Clientes",
          "procesos": "Procesos", "aprendizaje": "Aprendizaje"}

# acciones recomendadas por nombre de KPI (hojas de detalle)
actions = {}
for s in wb:
    if any(d in s.title for d in DETAIL.values()) and "BSC" not in s.title:
        for r in range(3, s.max_row + 1):
            if s.cell(r, 3).value and s.cell(r, 9).value:
                actions[s.cell(r, 3).value.strip()] = s.cell(r, 9).value.strip()

objectives, kpis = [], []
persp = obj = None
for r in range(4, ws.max_row + 1):
    b, c, d = ws.cell(r, 2).value, ws.cell(r, 3).value, ws.cell(r, 4).value
    if b:
        up = b.upper()
        persp = next((v for k, v in PERSP.items() if k in up), persp)
    if c:
        m = re.match(r"(OBJ-[A-Z]\d):\s*(.+)", c.strip())
        obj = {"id": m.group(1), "name": m.group(2).strip(), "perspective": persp}
        objectives.append(obj)
    if d and ws.cell(r, 6).value is not None:
        h = str(ws.cell(r, 8).value)
        mm = re.search(r"ROUND\((\w+?)\d+/(\w+?)\d+\*100", h)
        inverse = bool(mm and mm.group(1) == "F")   # Meta/Real
        kpis.append({
            "name": d.strip(), "perspective": persp, "objectiveId": obj["id"],
            "unit": str(ws.cell(r, 5).value), "target": ws.cell(r, 6).value,
            "current": ws.cell(r, 7).value,
            "direction": "menor" if inverse else "mayor",
            "action": actions.get(d.strip(), "")})

for i, k in enumerate(kpis, 1):
    k["id"] = f"KPI-{i:02d}"
for o in objectives:
    names = [k["name"] for k in kpis if k["objectiveId"] == o["id"]]
    o["description"] = "KPI: " + "; ".join(names) + "."

assert len(kpis) == 36 and len(objectives) == 12, (len(kpis), len(objectives))
seed = {"org": {"name": "TechPeru SAC", "short": "TechPeru", "period": "2025"},
        "objectives": objectives, "kpis": kpis}
with open(dst, "w", encoding="utf-8") as f:
    f.write("/* Generado por tools/excel_a_datos.py desde el Excel. */\n")
    f.write("window.BSC_SEED = " + json.dumps(seed, ensure_ascii=False, indent=1) + ";\n")
print(f"OK: {len(objectives)} objetivos, {len(kpis)} KPI, "
      f"{sum(k['direction']=='menor' for k in kpis)} inversos -> {dst}")
