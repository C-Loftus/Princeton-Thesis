# makefile to build thesis from md files

# 1 inch margins
MARGIN = 2.54cm
GEOM = geometry:margin=$(MARGIN)
OUT_DIR = ./out
FONT_SIZE = fontsize=12pt
COLOR = urlcolor='[HTML]{ff5733}'
SETTINGS = -V $(GEOM) -V $(FONT_SIZE) -V $(COLOR) --filter pandoc-citeproc --bibliography=citations.bib --csl=ieee.csl --metadata link-citations=true --lua-filter=./columns.lua

thesis:
	pandoc $(SETTINGS) -o $(OUT_DIR)/thesis.pdf ./chapters/*.md 

chapters:
	for i in ./chapters/*.md; do \
		pandoc $(SETTINGS)  -o $(OUT_DIR)/$$(basename $$i .md).pdf $$i; \
	done

proposal:
	for i in ./proposals/*.md; do \
		pandoc $(SETTINGS)  -o $(OUT_DIR)/$$(basename $$i .md).pdf $$i; \
	done

clean:
	rm $(OUT_DIR)/*.pdf

dependencies:
	code --install-extension notZaki.pandocciter
	code --install-extension esbenp.prettier-vscode
	code --install-extension yzhang.markdown-all-in-one
	code --install-extension streetsidesoftware.code-spell-checker
	
	sudo apt install pandoc
	sudo apt install pandoc-citeproc