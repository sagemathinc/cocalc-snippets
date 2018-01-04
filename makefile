PYTHON ?= python3
SCRIPT = examples.py

INDIR  ?= input
OUTDIR ?= .

INPUT  := $(shell find . ${INDIR}/ -type f -name '*.yaml')
OUTPUT := ${OUTDIR}/examples.json

.PHONY: clean test

${OUTPUT}: ${INPUT} ${SCRIPT}
	${PYTHON} ${SCRIPT} ${INDIR} ${OUTPUT}

test:
	${PYTHON} ${SCRIPT} test ${INDIR}

clean:
	-${RM} ${OUTPUT}
