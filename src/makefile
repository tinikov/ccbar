OMPDIR=/opt/homebrew/opt/libomp
CXXFLAGS = -Wall -std=c++17 -I$(OMPDIR)/include -O3

TARGETS = \
trev2 \
jre \
effmass \
mean \
a1plus \
ppot \
fks-td \
cart2sphr

OBJS = \
data_process.o \
misc.o

all: $(TARGETS)

$(TARGETS): %: %.o $(OBJS)
	$(CXX) $(CXXFLAGS) $< $(OBJS) -o $@

.PHONY: clean
clean:
	$(RM) *.o

.PHONY: clean.all
clean.all:
	$(RM) $(TARGETS)
	$(RM) *.o
