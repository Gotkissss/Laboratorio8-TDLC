#include <stdio.h>
#include <time.h>

/* Si el numero de operaciones pasa de esto, no se corre y se estima el tiempo.
   Con n = 1000000 serian ~5*10^12 iteraciones (horas de ejecucion). */
#define LIMITE_OPS 50000000000LL

long long total = 0; // para que el compilador no borre los ciclos

// La funcion del enunciado. Se usa long long porque counter pasa de 2^31
long long function(int n) {
    int i, j, k;
    long long counter = 0;
    for (i = n/2; i <= n; i++) {
        for (j = 1; j+n/2 <= n; j++) {
            for (k = 1; k <= n; k = k*2) {
                counter++;
            }
        }
    }
    return counter;
}

// cuantas veces se ejecuta counter++ (sale del analisis de la parte a)
long long contar_ops(int n) {
    long long vueltas_i = n - n/2 + 1;
    long long vueltas_j = n - n/2;
    long long vueltas_k = 0;
    for (long long k = 1; k <= n; k *= 2)
        vueltas_k++;
    return vueltas_i * vueltas_j * vueltas_k;
}

int main() {
    int valores[] = {1, 10, 100, 1000, 10000, 100000, 1000000};
    int cant = 7;
    double seg_por_op = 0;

    FILE *csv = fopen("resultados/problema1.csv", "w");
    if (csv == NULL) {
        printf("No se pudo abrir resultados/problema1.csv (correr desde la carpeta raiz)\n");
        return 1;
    }
    fprintf(csv, "n,operaciones,tiempo_s,tipo\n");

    printf("%10s %18s %16s  %s\n", "n", "operaciones", "tiempo (s)", "tipo");
    for (int t = 0; t < cant; t++) {
        int n = valores[t];
        long long ops = contar_ops(n);
        double tiempo;
        char *tipo;

        if (ops <= LIMITE_OPS) {
            // con n chico la funcion tarda menos que la resolucion del reloj,
            // entonces se repite varias veces y se saca el promedio
            long long reps = 10000000LL / ops;
            if (reps < 1) reps = 1;

            clock_t inicio = clock();
            for (long long r = 0; r < reps; r++)
                total += function(n);
            clock_t fin = clock();

            tiempo = (double)(fin - inicio) / CLOCKS_PER_SEC / reps;
            seg_por_op = tiempo / ops;
            tipo = "medido";
        } else {
            // se estima con el tiempo por operacion de la ultima corrida
            tiempo = seg_por_op * ops;
            tipo = "estimado";
        }

        printf("%10d %18lld %16.9f  %s\n", n, ops, tiempo, tipo);
        fprintf(csv, "%d,%lld,%.9f,%s\n", n, ops, tiempo, tipo);
        fflush(stdout);
    }

    fclose(csv);
    printf("(total = %lld)\n", total);
    return 0;
}
