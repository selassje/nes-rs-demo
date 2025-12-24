ASM = ca65
LD  = ld65

TARGET = nes-rs-demo

all:
	$(ASM) src/main.asm -o main.o
	$(LD) -C nes.cfg -o $(TARGET).nes main.o

clean:
	rm -f *.o *.nes