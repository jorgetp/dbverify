PROTOS = $(shell grep -l theory *.spthy)
FLAGS = $(wildcard *.flag)
GENERIC = generic.txt

verify: $(PROTOS:.spthy=.proof)

%.proof: %.spthy $(GENERIC) $(FLAGS)
	@echo Processing protocol $*
	@echo '  'Writing generic code into \'$<\'
	@sed '/^\/\/GENERIC CODE AFTER THIS LINE/q' $< > $*.tmp
	@cat $(GENERIC) >> $*.tmp
	@echo end >> $*.tmp
	@cat $*.tmp > $<
	@echo '  'Done.
	@echo '  'Running \'tamarin-prover $(shell test -e $*.flag && cat $*.flag) $< --prove\'
	@(time tamarin-prover $(shell test -e $*.flag && cat $*.flag) $< --prove) > $*.tmp 2>&1
	@(sed -n '/^theory $* begin/,$$p' $*.tmp) > $@
	@$(RM) $*.tmp
	@echo '  'Done.

clean:
	$(RM) *.tmp