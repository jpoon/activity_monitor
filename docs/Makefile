DOCDIR = build
STYLEDIR = style

RST2PDF_OPTS = -s ${STYLEDIR}/style.json
RST2HTML_OPTS = --stylesheet=${STYLEDIR}/style.css

all: setup html pdf

.PHONY: setup
setup:
	mkdir -p ${DOCDIR}

.PHONY: setup html
html: 
	/usr/bin/rst2html ${RST2HTML_OPTS} proposal.rst ${DOCDIR}/proposal.html

.PHONY: setup pdf
pdf:
	/usr/bin/rst2pdf ${RST2PDF_OPTS} proposal.rst -o ${DOCDIR}/proposal.pdf

.PHONY: clean
clean:
	rm -rf ${DOCDIR}

