import os
import sys
import time
import csv
from contextlib import redirect_stdout


def function(n):
    if n <= 1:
        return
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            print("Sequence")
            break


def medir(n, repeticiones):
    # los print se mandan a devnull, si no la terminal se vuelve lo mas lento
    with open(os.devnull, "w") as nulo, redirect_stdout(nulo):
        inicio = time.perf_counter()
        for _ in range(repeticiones):
            function(n)
        fin = time.perf_counter()
    return (fin - inicio) / repeticiones


valores = [1, 10, 100, 1000, 10000, 100000, 1000000]

# se puede correr desde la raiz o desde la carpeta problema2
carpeta_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ruta_csv = os.path.join(carpeta_raiz, "resultados", "problema2.csv")

filas = []
print(f"{'n':>10} {'prints':>10} {'tiempo (s)':>15}")
for n in valores:
    # para n chicos se repite para que el tiempo no salga 0
    # y se mide 3 veces quedandose con el minimo (el ruido del sistema solo suma tiempo)
    reps = max(1, 100000 // n)
    t = min(medir(n, reps) for _ in range(3))
    prints = n if n > 1 else 0
    filas.append([n, prints, f"{t:.9f}", "medido"])
    print(f"{n:>10} {prints:>10} {t:>15.9f}")
    sys.stdout.flush()

os.makedirs(os.path.dirname(ruta_csv), exist_ok=True)
with open(ruta_csv, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["n", "operaciones", "tiempo_s", "tipo"])
    w.writerows(filas)
