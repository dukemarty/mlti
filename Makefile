doc: 
	@doxygen

mrproper:
	@rm -f *~ *.pyc \#*\# 
	@rm -f templates/*~ templates/\#*\# 

realclean: mrproper
	@rm -rf doc/

