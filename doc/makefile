# makefile to build thesis from md files

# 1 inch margins
MARGIN = 2.54cm
GEOM = geometry:margin=$(MARGIN)
DOC_DIR = ./out
FONT_SIZE = fontsize=12pt
COLOR = urlcolor='[HTML]{ff5733}'
SETTINGS = -V $(GEOM) -V $(FONT_SIZE) -V $(COLOR)

thesis:
	pandoc $(SETTINGS) -o $(DOC_DIR)/thesis.pdf ./chapters/*.md

chapter:
	for i in ./chapters/*.md; do \
		pandoc $(SETTINGS)  -o $(DOC_DIR)/$$(basename $$i .md).pdf $$i; \
	done

proposal:
	for i in ./proposals/*.md; do \
		pandoc $(SETTINGS)  -o $(DOC_DIR)/$$(basename $$i .md).pdf $$i; \
	done

clean:
	rm $(DOC_DIR)/*.pdf
