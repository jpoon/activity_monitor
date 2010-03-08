BUILDDIR = build
STYLEDIR = style

RST2PDF_OPTS = -s ${STYLEDIR}/style.json -b1
RST2HTML_OPTS = --stylesheet=${STYLEDIR}/style.css

all: setup html pdf

.PHONY: setup
setup:
	mkdir -p ${BUILDDIR}

.PHONY: setup html
html: 
	/usr/bin/rst2html ${RST2HTML_OPTS} proposal.rst ${BUILDDIR}/proposal.html
	/usr/bin/rst2html ${RST2HTML_OPTS} progressreport.rst ${BUILDDIR}/progressreport.html
	cp -r imgs ${BUILDDIR}

.PHONY: setup pdf
pdf:
	/usr/bin/rst2pdf ${RST2PDF_OPTS} proposal.rst -o ${BUILDDIR}/proposal.pdf
	/usr/bin/rst2pdf ${RST2PDF_OPTS} progressreport.rst -o ${BUILDDIR}/progressreport.pdf

.PHONY: clean
clean:
	rm -rf ${BUILDDIR}

