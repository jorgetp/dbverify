PROTOS = $(shell grep -l theory *.spthy)
GENERIC = generic

verify: $(PROTOS:.spthy=.proof)

%.proof: %.spthy $(GENERIC)
	sed '/^\/\/GENERIC CODE AFTER THIS LINE/q' $< > $<.tmp
	cat $(GENERIC) >> $<.tmp
	echo end >> $<.tmp
	cat $<.tmp > $<
	$(RM) $<.tmp
	(time tamarin-prover --prove $< ) > $@.tmp 2>&1
	(sed -n '/^theory $* begin/,$$p' $@.tmp) > $@
	$(RM) $@.tmp