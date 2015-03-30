#######################################
# Makefile for the L3 6502 simulator ##
#######################################

# generating the L3 source list
# /!\ inclusion order matters /!\
#######################################
L3SRCDIR=src/l3
L3SRCBASE+=base.spec
L3SRCBASE+=memory.spec
L3SRCBASE+=instructions.spec
L3SRCBASE+=addressing-modes.spec
L3SRCBASE+=decode.spec
L3SRCBASE+=next.spec
L3SRC=$(patsubst %, $(L3SRCDIR)/%, $(L3SRCBASE))

# generating the sml source list
#######################################
SMLSRCBASE+=6502.sig
SMLSRCBASE+=6502.sml

# make targets
#######################################
SIM ?= l3-6502

all: $(SIM)

$(SIM): 6502.sig 6502.sml

6502.sig 6502.sml: $(L3SRC)
	echo 'SMLExport.spec ("$(L3SRC)", "6502")' | l3

clean:
	rm -f 6502.sig 6502.sml
