PYTHON ?= python3
SCRIPT = examples.py

INDIR  ?= src
OUTDIR ?= .
LANG   = ''

INPUT  := $(shell find . ${INDIR}/ -type f -name '*.yaml')
OUTPUT := ${OUTDIR}/examples.json

.PHONY: clean test

${OUTPUT}: ${INPUT} ${SCRIPT}
	${PYTHON} ${SCRIPT} ${INDIR} ${OUTPUT}

# just test one subdirectory like make LANG=sage test
test:
	${PYTHON} ${SCRIPT} test ${INDIR}/${LANG}

testtest:
	${PYTHON} ${SCRIPT} test test

clean:
	-${RM} ${OUTPUT}
