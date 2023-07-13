dep:
	sudo apt install texlive-latex-extra
	sudo apt install latexmk
	sudo apt install texlive-extra-utils


count:
	@echo "Word count: "
	@texcount -inc -sum -total -1 -merge -q -utf8 -dir -sub=none -template="{sum}" report.tex

clean:
	rm -f *.aux *.bbl *.blg *.log *.out *.toc *.lot *.lof *.gz *.dvi *.fdb_latexmk *.fls _minted*
