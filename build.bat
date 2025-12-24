@echo off
ca65 src\main.asm -o main.o
ld65 -C nes.cfg -o nes-rs-demo.nes main.o
echo Build complete!