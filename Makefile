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
L3_SML_LIB ?= `l3 --lib-path`

# Other env variable
########################################
VERBOSE ?= 0
MLTON ?= mlton
#
#all: l3-6502
#
#l3-6502: $(BUILDDIR)/cpu6502.sig $(BUILDDIR)/cpu6502.sml $(SMLDIR)/cpu6502.mlb $(SMLDIR)/run.sml $(CDIR)/mem.c
#	mlton -verbose $(VERBOSE) -output $@ -default-ann 'allowFFI true' -export-header $(BUILDDIR)/smlexport.h -cc-opt "-I $(BUILDDIR)/" -default-type intinf -mlb-path-var 'L3_SML_LIB '$(L3_SML_LIB) $(SMLDIR)/cpu6502.mlb $(CDIR)/mem.c
#
#NES: NES_sdl
#
#NES_sdl: $(BUILDDIR)/cpu6502.sig $(BUILDDIR)/cpu6502.sml $(SMLDIR)/nes.mlb $(SMLDIR)/nes-run.sml $(CDIR)/nes-ppu-draw-sdl.c $(CDIR)/nes-ppu.c $(CDIR)/nes-cartridge.c $(CDIR)/nes-mem.c
#	mlton -verbose $(VERBOSE) -output $@ -default-ann 'allowFFI true' -export-header $(BUILDDIR)/smlexport.h -cc-opt "-Wall -g -I $(BUILDDIR)/" -link-opt "-lpthread -lSDL" -default-type intinf -mlb-path-var 'L3_SML_LIB '$(L3_SML_LIB) $(SMLDIR)/nes.mlb $(CDIR)/nes-ppu-draw-sdl.c $(CDIR)/nes-ppu.c $(CDIR)/nes-cartridge.c $(CDIR)/nes-mem.c
#

NES_C_DIR=$(CDIR)/nes-emul
NES_C_SRC=$(wildcard $(NES_C_DIR)/*.c)
NES_OBJ=$(notdir $(patsubst %.c,%.o,$(NES_C_SRC)))

$(NES_OBJ):%.o:$(NES_C_DIR)/%.c libcpu6502
	$(CC) -I $(CDIR) -I $(BUILDDIR) -c -o $(BUILDDIR)/$@ $<

nes-l3: $(NES_OBJ)
	$(CC) -o $@ $(addprefix $(BUILDDIR)/,$^) -lSDL -L$(BUILDDIR) -lcpu6502

libcpu6502: $(BUILDDIR)/cpu6502.sig $(BUILDDIR)/cpu6502.sml $(SMLDIR)/libcpu6502.mlb $(SMLDIR)/libcpu6502.sml
	mlton -verbose $(VERBOSE) -output $(BUILDDIR)/$@.so -format library -default-ann 'allowFFI true' -export-header $(BUILDDIR)/$@.h -default-type intinf -mlb-path-var 'L3_SML_LIB '$(L3_SML_LIB) $(SMLDIR)/libcpu6502.mlb

$(BUILDDIR)/cpu6502.sig $(BUILDDIR)/cpu6502.sml: $(L3SRC)
	mkdir -p $(BUILDDIR)
	echo 'SMLExport.spec ("$(L3SRC)", "$(BUILDDIR)/cpu6502")' | l3 | tee $(BUILDDIR)/l3build.log

clean:
	rm -rf $(BUILDDIR)
