DOCDIR = docs

all: setup html pdf

.PHONY: setup
setup:
	mkdir -p ${DOCDIR}

.PHONY: setup html
html: 
	/usr/bin/rst2html proposal.rst ${DOCDIR}/proposal.html

.PHONY: setup pdf
pdf:
	/usr/bin/rst2pdf proposal.rst -o ${DOCDIR}/proposal.pdf

.PHONY: clean
clean:
	rm -rf ${DOCDIR}

