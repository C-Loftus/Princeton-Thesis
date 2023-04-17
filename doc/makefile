# makefile to build thesis from md files

# 1 inch margins
MARGIN = 2.54cm
GEOM = geometry:margin=$(MARGIN)
OUT_DIR = ./out
FONT_SIZE = fontsize=12pt
COLOR = urlcolor='[HTML]{ff5733}'
# use double spacing
SPACING = documentclass=report


SETTINGS = -V $(GEOM) \
  -V $(FONT_SIZE)\
  -V $(COLOR) \
  --filter pandoc-citeproc \
  --bibliography=citations.bib \
  --csl=ieee.csl \
  --metadata link-citations=true \
  -V $(SPACING)  \
#   --template=report.tex 
#   --lua-filter=./columns.lua \
#   -F mermaid-filter 

thesis:
	pandoc $(SETTINGS) -o $(OUT_DIR)/written_final_report.pdf main.md

combine:
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
	sudo apt install librsvg2-bin
	sudo npm install --global mermaid-filter
	sudo apt-get install texlive-bibtex-extra biber