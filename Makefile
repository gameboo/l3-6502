#######################################
# Makefile for the L3 6502 simulator ##
#######################################

# generating the L3 source list
# /!\ inclusion order matters /!\
#######################################
L3SRCDIR=src/l3
L3SRCBASE+=display.spec
L3SRCBASE+=base.spec
L3SRCBASE+=memory.spec
L3SRCBASE+=addressing-modes.spec
L3SRCBASE+=instructions.spec
L3SRCBASE+=decode.spec
L3SRCBASE+=next.spec
L3SRC=$(patsubst %, $(L3SRCDIR)/%, $(L3SRCBASE))

# make targets
#######################################
SIM ?= l3-6502
BUILDDIR ?= builddir
SMLLIBDIR=src/sml/lib
SMLLIBSRC=Runtime.sig Runtime.sml\
          IntExtra.sig IntExtra.sml\
          Nat.sig Nat.sml\
          L3.sig L3.sml\
          Bitstring.sig Bitstring.sml\
          BitsN.sig BitsN.sml\
          FP64.sig FP64.sml\
          Ptree.sig Ptree.sml\
          MutableMap.sig MutableMap.sml
SMLLIB=$(patsubst %, $(SMLLIBDIR)/%, $(SMLLIBSRC))

all: $(SIM)

$(SIM): $(BUILDDIR)/cpu6502.sig $(BUILDDIR)/cpu6502.sml $(SMLLIB)
	mlton -output $(SIM) -default-type intinf src/sml/cpu6502.mlb

$(BUILDDIR)/cpu6502.sig $(BUILDDIR)/cpu6502.sml: $(L3SRC)
	mkdir -p $(BUILDDIR)
	echo 'SMLExport.spec ("$(L3SRC)", "$(BUILDDIR)/cpu6502")' | l3 | tee $(BUILDDIR)/l3build.log

clean:
	rm -rf $(BUILDDIR)
