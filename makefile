PYTHON ?= python3
SCRIPT = examples.py

INDIR  ?= src
OUTDIR ?= .

INPUT  := $(shell find . ${INDIR}/ -type f -name '*.yaml')
OUTPUT := ${OUTDIR}/examples.json

.PHONY: clean test

${OUTPUT}: ${INPUT} ${SCRIPT}
	${PYTHON} ${SCRIPT} ${INDIR} ${OUTPUT}

test:
	${PYTHON} ${SCRIPT} test ${INDIR}

testtest:
	${PYTHON} ${SCRIPT} test test

clean:
	-${RM} ${OUTPUT}
