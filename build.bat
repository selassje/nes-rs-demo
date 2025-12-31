@echo off
setlocal EnableExtensions EnableDelayedExpansion

echo Assembling...
ca65 src\main.asm -o main.o || goto :error
ca65 src\globals.asm -o globals.o || goto :error
ca65 src\procedures.asm -o procedures.o || goto :error

echo Linking...
ld65 -C nes.cfg main.o globals.o procedures.o -o nes-rs-demo.nes || goto :error

echo Build succeeded.
exit /b 0

:error
echo.
echo BUILD FAILED
exit /b 1