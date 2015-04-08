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
BUILDDIR ?= builddir
CDIR=src/c
SMLDIR=src/sml
SMLLIBDIR=$(SMLDIR)/lib
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

# Other env variable
########################################
VERBOSE ?= 0

all: l3-6502

l3-6502: $(BUILDDIR)/cpu6502.sig $(BUILDDIR)/cpu6502.sml $(SMLDIR)/cpu6502.mlb $(SMLDIR)/run.sml $(CDIR)/mem.c
	mlton -verbose $(VERBOSE) -output $@ -default-ann 'allowFFI true' -export-header $(BUILDDIR)/smlexport.h -cc-opt "-I $(BUILDDIR)/" -default-type intinf $(SMLDIR)/cpu6502.mlb $(CDIR)/mem.c

NES: NES_sdl

NES_sdl: $(BUILDDIR)/cpu6502.sig $(BUILDDIR)/cpu6502.sml $(SMLDIR)/nes.mlb $(SMLDIR)/nes-run.sml $(CDIR)/nes-ppu-draw-sdl.c $(CDIR)/nes-ppu.c $(CDIR)/nes-mem.c
	mlton -verbose $(VERBOSE) -output $@ -default-ann 'allowFFI true' -export-header $(BUILDDIR)/smlexport.h -cc-opt "-I $(BUILDDIR)/" -link-opt "-lpthread -lSDL" -default-type intinf $(SMLDIR)/nes.mlb $(CDIR)/nes-ppu-draw-sdl.c $(CDIR)/nes-ppu.c $(CDIR)/nes-mem.c

$(BUILDDIR)/cpu6502.sig $(BUILDDIR)/cpu6502.sml: $(L3SRC)
	mkdir -p $(BUILDDIR)
	echo 'SMLExport.spec ("$(L3SRC)", "$(BUILDDIR)/cpu6502")' | l3 | tee $(BUILDDIR)/l3build.log

clean:
	rm -rf $(BUILDDIR)
