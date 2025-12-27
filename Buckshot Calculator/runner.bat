@echo off
title Buckshot Roulette Calculator
chcp 65001
cls

set colors=4 6 E 2 A 3 1 5 9 B D C
for %%c in (%colors%) do (
    color %%c
    cls
    echo ================================
    echo Buckshot Roulette Calculator (Limpan is the goat!)
    echo ================================
    type "ascii\face.txt"
    ping -n 1 -w 200 127.0.0.1 >nul
    echo.
)
python calculator.py
pause
