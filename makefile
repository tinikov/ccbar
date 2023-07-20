OMPDIR=/opt/homebrew/opt/libomp
CXXFLAGS = -Wall -std=c++17 -I$(OMPDIR)/include -O3

SOURCE = ./src
BIN = ./bin
PROG_NAME = \
a1plus \
cart2sphr \
effmass \
fks-td \
jre \
mean \
norm \
prev \
trev2 \

PRE = \
data_process.o \
misc.o

TARGETS = $(addprefix $(BIN)/,$(PROG_NAME))
OBJS = $(addprefix $(SOURCE)/,$(PRE))

all: $(TARGETS)

$(TARGETS): $(BIN)/%: $(SOURCE)/%.o $(OBJS)
	$(CXX) $(CXXFLAGS) $< $(OBJS) -o $@

.PHONY: clean
clean:
	$(RM) $(SOURCE)/*.o

.PHONY: clean.all
clean.all:
	$(RM) $(TARGETS)
	$(RM) $(SOURCE)/*.o
