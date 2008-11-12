doc: 
	@doxygen

mrproper:
	@rm -f *~ *.pyc

realclean: mrproper
	@rm -rf doc/

