# makefile to build thesis from md files

MARGIN = 1.5cm
DOC_DIR = doc/out

thesis:
	pandoc -V geometry:margin=$(MARGIN) -o $(DOC_DIR)/thesis.pdf chapters/*.md
chapter:
	for i in chapters/*.md; do \
		pandoc -V geometry:margin=$(MARGIN) -o $(DOC_DIR)/$$(basename $$i .md).pdf $$i; \
	done

proposal:
	for i in proposals/*.md; do \
		pandoc -V geometry:margin=$(MARGIN) -o $(DOC_DIR)/$$(basename $$i .md).pdf $$i; \
	done

clean:
	rm $(DOC_DIR)/*.pdf