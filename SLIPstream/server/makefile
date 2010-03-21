EXE=startServer
CC=gcc
CFLAGS=-I. -O -g -Wall -std=gnu99

%.o: %.c 
	$(CC) -c -o $@ $< $(CFLAGS)

all: main.o
	gcc -o $(EXE) main.o $(CFLAGS)
clean: 
	rm -f *.o *~ core $(EXE)

