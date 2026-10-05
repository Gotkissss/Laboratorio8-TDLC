@echo off
rem Compila y corre los 3 problemas y despues genera graficas y tablas.
rem Se corre desde la carpeta raiz del repo. Tarda ~4 minutos en total.

if not exist resultados mkdir resultados

echo === Compilando ===
gcc -O0 -o problema1\problema1.exe problema1\problema1.c || exit /b 1
gcc -O0 -o problema3\problema3.exe problema3\problema3.c || exit /b 1

echo.
echo === Problema 1 (n=100000 tarda ~1-2 min) ===
problema1\problema1.exe

echo.
echo === Problema 2 ===
python problema2\problema2.py

echo.
echo === Problema 3 (n=100000 tarda ~1-2 min) ===
problema3\problema3.exe

echo.
echo === Graficas ===
python graficas\graficar.py
