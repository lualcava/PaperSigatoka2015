MAINFILE=Paper_Sigatoka_-_2015

PDFLATEX=pdflatex -interaction=batchmode
ECHO=/bin/echo -E


# TeX files
TEXFILES = $(wildcard ./*.tex) 
BIBFILES = $(wildcard *.bib)

# implicit rules (pattern rules)

# -----------------------------------------------------------------------------
# Targets
# -----------------------------------------------------------------------------

pdf:     $(MAINFILE).pdf

$(MAINFILE).pdf:	$(TEXFILES) $(PDFFILES) $(BIBFILES)
	@echo "Generating PDF file..."; \
	echo "------------------------------------------" ;\
	echo "Running latex once..." ;\
	$(PDFLATEX) $(MAINFILE) > pdf.log 2>&1 ;\
	if ( bibtex $(MAINFILE) >> pdf.log 2>&1 ) ; then \
	  echo " Bibliography ok" ;\
	else \
	  echo " Bibliography failed" ;\
	fi ;\
	$(PDFLATEX) $(MAINFILE) > pdf.log 2>&1 ;\
	latex_count=5 ; \
	while egrep -s 'Rerun (LaTeX|to get cross-references right)' $(MAINFILE).log && [ $$latex_count -gt 0 ] ;\
	    do \
	      echo "Rerunning latex...." ;\
	      $(PDFLATEX) $(MAINFILE).tex >> pdf.log 2>&1 ;\
	      latex_count=`expr $$latex_count - 1` ;\
	    done ;\
	echo "Ready."

force-pdf: 
	touch $(MAINFILE).tex ;\
	make pdf

clean:
	@echo "Cleaning..." ;\
	rm -f *.log *.lot *.toc *.lof *.aux *.dvi *.nlo *.nls ;\
	rm -f *.idx *.ilg *.ind *.bbl *.blg *.brf *.out *.todo *.flc *.xmp ;\

clean-all: clean
	@rm -f `find . -name "*~"` \#* fig/*.aux ;\
	rm -fr fig/*fig.bak ;\
	echo "All cleaned up"

help:
	@echo "This Makefile provides following targets: " ;\
	echo " pdf:       generate $(MAINFILE).pdf" ;\
	echo " force-pdf: force generation of $(MAINFILE).pdf" ;\
	echo " clean:     remove temporary files but keep final ps and pdf" ;\
	echo " clean-all: like clean but remove also final files"
