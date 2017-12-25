PYTHON ?= python3

INDIR  ?= input
OUTDIR ?= .

INPUT  := $(shell find . ${INDIR}/ -type f -name '*.yaml')
OUTPUT := ${OUTDIR}/examples.json

.PHONY: clean

${OUTPUT}: ${INPUT} build.py
	${PYTHON} build.py ${INDIR} ${OUTPUT}

clean:
	-${RM} ${OUTPUT}
