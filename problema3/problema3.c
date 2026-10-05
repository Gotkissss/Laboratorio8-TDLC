#include <stdio.h>
#include <time.h>

/* Con n = 1000000 serian ~8*10^10 printf (cientos de GB de texto),
   asi que arriba de este limite solo se estima el tiempo. */
#define LIMITE_OPS 1000000000LL

void function(int n) {
    int i, j;
    for (i = 1; i <= n/3; i++) {
        for (j = 1; j <= n; j += 4) {
            printf("Sequence\n");
        }
    }
}

// (n/3) vueltas del for de afuera por ceil(n/4) del de adentro
long long contar_prints(int n) {
    long long afuera = n / 3;
    long long adentro = (n + 3) / 4;
    return afuera * adentro;
}

int main() {
    int valores[] = {1, 10, 100, 1000, 10000, 100000, 1000000};
    double seg_por_print = 0;

    // Los "Sequence" se mandan a NUL (el /dev/null de Windows). Si se imprimen
    // en la consola lo que se mide es la velocidad de la terminal.
    // La tabla de resultados va por stderr para que si se vea.
    if (freopen("NUL", "w", stdout) == NULL) {
        fprintf(stderr, "No se pudo redirigir stdout\n");
        return 1;
    }
    // Windows trata NUL como consola y lo deja sin buffer (cada printf era una
    // llamada al sistema, ~4 us). Con buffer se mide el costo del printf en si.
    setvbuf(stdout, NULL, _IOFBF, 1 << 16);

    FILE *csv = fopen("resultados/problema3.csv", "w");
    if (csv == NULL) {
        fprintf(stderr, "No se pudo abrir resultados/problema3.csv (correr desde la carpeta raiz)\n");
        return 1;
    }
    fprintf(csv, "n,operaciones,tiempo_s,tipo\n");

    fprintf(stderr, "%10s %16s %16s  %s\n", "n", "prints", "tiempo (s)", "tipo");
    for (int t = 0; t < 7; t++) {
        int n = valores[t];
        long long prints = contar_prints(n);
        double tiempo;
        char *tipo = "medido";

        if (prints == 0) {
            // n = 1: n/3 = 0, el for no entra
            clock_t inicio = clock();
            for (int r = 0; r < 1000000; r++)
                function(n);
            tiempo = (double)(clock() - inicio) / CLOCKS_PER_SEC / 1000000;
        } else if (prints <= LIMITE_OPS) {
            long long reps = 1000000LL / prints;
            if (reps < 1) reps = 1;

            clock_t inicio = clock();
            for (long long r = 0; r < reps; r++)
                function(n);
            fflush(stdout);
            tiempo = (double)(clock() - inicio) / CLOCKS_PER_SEC / reps;
            seg_por_print = tiempo / prints;
        } else {
            tiempo = seg_por_print * prints;
            tipo = "estimado";
        }

        fprintf(stderr, "%10d %16lld %16.9f  %s\n", n, prints, tiempo, tipo);
        fprintf(csv, "%d,%lld,%.9f,%s\n", n, prints, tiempo, tipo);
    }

    fclose(csv);
    return 0;
}
