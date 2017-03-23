# default experiment and its output

#expt: expt.log eval.log

expt.log: inputs/cfacts inputs/learned.ppr inputs/examples
	python umls-expt.py > expt.log

#eval.log: expt.log
#	proppr eval tmp-cache/wnet-test.examples tmp-cache/hypernym-test.solutions.txt --metric auc --defaultNeg > eval.log

# prepare for running expt

setup: inputs tmp-cache inputs/cfacts inputs/learned.ppr inputs/examples

inputs:
	mkdir $@

tmp-cache:
	mkdir $@

inputs/examples:
	python bin/convert-examples.py

inputs/cfacts: inputs/ruleids.cfacts
	cut -f2- raw/train.cfacts raw/test.cfacts | perl -nae 'print join("\t",$$F[0],"s".$$F[1],"s".$$F[2]),"\n"' > inputs/umls-core.cfacts
	cat inputs/umls-*.cfacts > inputs/umls.cfacts

inputs/learned.ppr inputs/ruleids.cfacts:
	python bin/convert-rules.py

# a quickly-viewable check on the default experiment (like a unit test)

check: actual.txt
	diff -y actual.txt expected.txt || true

actual.txt: expt.log eval.log
	echo \# actual output of expt on `date` > actual.txt
	grep training.*done expt.log >> actual.txt
	grep micro eval.log >> actual.txt 

# clean up the directory

clean:
	rm -f *.pyc *.prof *~ expt.log

