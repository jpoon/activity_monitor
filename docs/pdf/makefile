BUILDDIR = build
STYLEDIR = style

RST2PDF_OPTS = -s ${STYLEDIR}/style.json -b1

all: setup pdf

.PHONY: setup
setup:
	mkdir -p ${BUILDDIR}

.PHONY: setup pdf
pdf:
	/usr/bin/rst2pdf ${RST2PDF_OPTS} proposal.rst -o ${BUILDDIR}/proposal.pdf
	/usr/bin/rst2pdf ${RST2PDF_OPTS} progressreport.rst -o ${BUILDDIR}/progressreport.pdf

.PHONY: clean
clean:
	rm -rf ${BUILDDIR}

