PGMS = epanet-single epanet-stepwise

SINGLE_SRCS = epanet-single.cc utility.cc
SINGLE_OBJS = ${SINGLE_SRCS:%.cc=%.o}

STEPWISE_SRCS = epanet-stepwise.cc utility.cc
STEPWISE_OBJS = ${STEPWISE_SRCS:%.cc=%.o}

ALL_SRCS = ${SINGLE_SRCS} ${STEPWISE_SRCS}
ALL_OBJS = ${SINGLE_OBJS} ${STEPWISE_OBJS}

EPANET_BASE = ../epanet-solver

CFLAGS += -I${EPANET_BASE}/src/solver/include
LDFLAGS += -L${EPANET_BASE}/build/bin -Wl,--rpath=${EPANET_BASE}/build/bin -lepanet2

LD = ld.lld

.PHONY:	all depend clean cleanall

all:	${PGMS}

depend:
	mkdep ${CXXFLAGS} ${ALL_SRCS}

.depend:	.OPTIONAL

${ALL_OBJS}:	.depend

epanet-single:	${SINGLE_OBJS}
	${CXX} ${LDFLAGS} ${SINGLE_OBJS} ${LDLIBS} -o ${.TARGET}

epanet-stepwise:	${STEPWISE_OBJS}
	${CXX} ${LDFLAGS} ${STEPWISE_OBJS} ${LDLIBS} -o ${.TARGET}

clean:
	rm -f ${ALL_OBJS}

cleanall:	clean
	rm -f ${PGMS} .depend
