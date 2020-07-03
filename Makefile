PGMS = epanet-single epanet-stepwise

SINGLE_SRCS = epanet-single.cc utility.cc
SINGLE_OBJS = ${SINGLE_SRCS:%.cc=%.o}

STEPWISE_SRCS = epanet-stepwise.cc utility.cc
STEPWISE_OBJS = ${STEPWISE_SRCS:%.cc=%.o}


EPANET_BASE = ../epanet-solver

CFLAGS += -I${EPANET_BASE}/src/solver/include
LDFLAGS += -L${EPANET_BASE}/build/bin -Wl,--rpath=${EPANET_BASE}/build/bin -lepanet2

LD = ld.lld

all:	${PGMS}

.PHONY:	all

.depend:
	mkdep ${CXXFLAGS} ${SINGLE_SRCS} ${STEPWISE_SRCS}

epanet-single:	${SINGLE_OBJS} .depend
	${CXX} ${LDFLAGS} ${SINGLE_OBJS} ${LDLIBS} -o ${.TARGET}

epanet-stepwise:	${STEPWISE_OBJS} .depend
	${CXX} ${LDFLAGS} ${STEPWISE_OBJS} ${LDLIBS} -o ${.TARGET}

clean:
	rm ${SINGLE_OBJS} ${STEPWISE_OBJS}
