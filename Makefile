SOURCEFILES=pti.py tests_pti.py
DOCUFILES=doc-src/src/general.doxysrc

tests: tests_pti.py
	./tests_pti.py

doc: Doxyfile ${SOURCEFILES} ${DOCUFILES}
	@doxygen

mrproper:
	@rm -f *~ *.pyc \#*\# 
	@rm -f templates/*~ templates/\#*\#

realclean: mrproper
	@rm -rf doc/

