"""Lee los CSV de resultados/ y genera una grafica por problema + tablas en markdown."""
import csv
import math
import os

import matplotlib
matplotlib.use("Agg")  # solo guardar imagenes, sin abrir ventana
import matplotlib.pyplot as plt

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTADOS = os.path.join(RAIZ, "resultados")
CARPETA_GRAFICAS = os.path.join(RAIZ, "graficas")

AZUL = "#2a78d6"
GRIS = "#52514e"

# nombre, funcion teorica para la curva de referencia, etiqueta
problemas = [
    ("problema1", lambda n: n * n * math.log2(n), "O(n² log n)"),
    ("problema2", lambda n: n, "O(n)"),
    ("problema3", lambda n: n * n, "O(n²)"),
]


def leer_csv(nombre):
    filas = []
    with open(os.path.join(RESULTADOS, nombre + ".csv")) as f:
        for fila in csv.DictReader(f):
            filas.append({
                "n": int(fila["n"]),
                "ops": int(fila["operaciones"]),
                "tiempo": float(fila["tiempo_s"]),
                "tipo": fila["tipo"],
            })
    return filas


def formato_tiempo(seg):
    if seg < 1e-6:
        return f"{seg * 1e9:.1f} ns"
    if seg < 1e-3:
        return f"{seg * 1e6:.2f} µs"
    if seg < 1:
        return f"{seg * 1e3:.2f} ms"
    if seg < 3600:
        return f"{seg:.2f} s"
    return f"{seg:.0f} s (~{seg / 3600:.1f} h)"


tablas = []
for nombre, teorica, etiqueta in problemas:
    datos = leer_csv(nombre)

    medidos = [d for d in datos if d["tipo"] == "medido"]
    estimados = [d for d in datos if d["tipo"] == "estimado"]

    fig, ax = plt.subplots(figsize=(7, 4.5))

    # curva teorica escalada para que pase por el ultimo punto medido
    ultimo = medidos[-1]
    c = ultimo["tiempo"] / teorica(ultimo["n"])
    xs = [10 ** (k / 10) for k in range(10, 61)]
    ax.plot(xs, [c * teorica(x) for x in xs], "--", color=GRIS, linewidth=1.5,
            label=f"{etiqueta} (escalada)")

    ax.plot([d["n"] for d in datos], [d["tiempo"] for d in datos], "-",
            color=AZUL, linewidth=2)
    ax.plot([d["n"] for d in medidos], [d["tiempo"] for d in medidos], "o",
            color=AZUL, markersize=8, label="medido")
    if estimados:
        ax.plot([d["n"] for d in estimados], [d["tiempo"] for d in estimados], "o",
                markerfacecolor="white", markeredgecolor=AZUL, markeredgewidth=2,
                markersize=8, label="estimado (no se ejecutó)")

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("tamaño de input n")
    ax.set_ylabel("tiempo (s)")
    ax.set_title(f"Problema {nombre[-1]}: tamaño de input vs. tiempo")
    ax.grid(True, which="major", color="#e4e3df", linewidth=0.8)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    ax.legend(frameon=False)
    fig.tight_layout()

    salida = os.path.join(CARPETA_GRAFICAS, nombre + ".png")
    fig.savefig(salida, dpi=150)
    plt.close(fig)
    print("guardada", salida)

    tabla = [f"### Problema {nombre[-1]}", "",
             "| n | operaciones | tiempo | tipo |", "|---:|---:|---:|---|"]
    for d in datos:
        tabla.append(f"| {d['n']:,} | {d['ops']:,} | {formato_tiempo(d['tiempo'])} | {d['tipo']} |")
    tablas.append("\n".join(tabla))

with open(os.path.join(RESULTADOS, "tablas.md"), "w", encoding="utf-8") as f:
    f.write("\n\n".join(tablas) + "\n")
print("guardada", os.path.join(RESULTADOS, "tablas.md"))
