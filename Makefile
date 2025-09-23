NAME=paper

TARGET=$(NAME)

all: $(TARGET).pdf

quick: Makefile *.tex sections/*.tex *.bib
	pdflatex  $(TARGET).tex
	rm -f *.aux *.log *.out *.bbl *.blg *~ *.bak *.ps *.synctex.gz
	if which xdg-open 1>/dev/null 2>&1; then \
		xdg-open $(TARGET).pdf; \
	else \
		open -a Preview $(TARGET).pdf & \
	fi

$(TARGET).pdf: Makefile *.tex sections/*.tex *.bib
	pdflatex  $(TARGET).tex
	-bibtex --min-crossrefs=100    $(TARGET)
	pdflatex  $(TARGET).tex
	pdflatex  $(TARGET).tex
	rm -f *.aux *.log *.out *.bbl *.blg *~ *.bak *.ps *.synctex.gz
	if which xdg-open 1>/dev/null 2>&1; then \
		xdg-open $(TARGET).pdf; \
	else \
		open -a Preview $(TARGET).pdf & \
	fi

clean:
	rm -f *.aux *.log *.out *.bbl *.blg *~ *.bak *.ps $(TARGET).pdf *.synctex.gz
