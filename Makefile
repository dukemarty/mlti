doc: 
	@doxygen

mrproper:
	@rm -rf *~ *.pyc

realclean: mrproper
	@rm -rf doc/

