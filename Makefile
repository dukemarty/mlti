SOURCEFILES=mlti.py mlticore.py mltihelpers.py
DOCUFILES=doc-src/src/general.doxysrc doc-src/images/mlti-logo.graffle doc-src/images/mlti-projecttitle.graffle

tests: tests_mlticore.py
	./tests_mlticore.py

doc: Doxyfile ${SOURCEFILES} ${DOCUFILES}
	@doxygen

mrproper:
	@rm -f *~ *.pyc \#*\# 
	@rm -f templates/*~ templates/\#*\#

realclean: mrproper
	@rm -rf doc/

