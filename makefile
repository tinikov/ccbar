CXXFLAGS = -Wall -std=c++17 -O3

SOURCE = ./src
BIN = ./bin
PROG_NAME = \
a1plus \
cart2sphr \
effmass \
fks-td \
fks-td-5pt \
fks-ti \
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

all: bin $(TARGETS)

bin:
	mkdir -p $(BIN)

$(TARGETS): $(BIN)/%: $(SOURCE)/%.o $(OBJS)
	$(CXX) $(CXXFLAGS) $< $(OBJS) -o $@

.PHONY: clean
clean:
	$(RM) $(SOURCE)/*.o

.PHONY: clean.all
clean.all:
	$(RM) $(TARGETS)
	$(RM) $(SOURCE)/*.o
