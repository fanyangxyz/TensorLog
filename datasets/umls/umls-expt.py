import sys

from tensorlog import expt
from tensorlog import declare
from tensorlog import comline
from tensorlog import learn
from tensorlog import plearn

if __name__=="__main__":
    #usage: [targetPredicate] [epochs]
    
    #get the command-line options for this experiment
    #pred = 'hypernym' if len(sys.argv)<=1 else sys.argv[1]
    pred = 'affects' if len(sys.argv)<=1 else sys.argv[1]
    epochs = 30 if len(sys.argv)<=2 else int(sys.argv[2])

    # use comline.parseCommandLine to set up the program, etc
    optdict,args = comline.parseCommandLine([
            '--logging', 'warn',
            '--db', 'inputs/umls.db|inputs/umls.cfacts',
            '--prog','inputs/umls-learned.ppr', '--proppr',
            '--train','inputs/umls-train.dset|inputs/umls-train.exam',
            '--test', 'inputs/umls-test.dset|inputs/umls-test.exam'])

    # prog is shortcut to the output optdict, for convenience.
    prog = optdict['prog']

    # the weight vector is sparse - just the constants in the unary predicate rule
    prog.setRuleWeights(prog.db.vector(declare.asMode("rule(i)")))

    # use a non-default learner, overriding the tracing function,
    # number of epochs, and regularizer
    learner = plearn.ParallelFixedRateGDLearner(
        prog,epochs=epochs,parallel=40,regularizer=learn.L2Regularizer())
#    learner = plearn.ParallelAdaGradLearner(
#        prog,epochs=epochs,parallel=40,regularizer=learn.L2Regularizer())
    targetMode = 'i_%s/io' % pred if pred!='ALL' else None

    # configute the experiment
    params = {'prog':prog,
              'trainData':optdict['trainData'], 
              'testData':optdict['testData'],
              'targetMode':targetMode,
              'savedTestPredictions':'tmp-cache/%s-test.solutions.txt' % pred,
              'savedTrainExamples':'tmp-cache/umls-train.examples',
              'savedTestExamples':'tmp-cache/umls-test.examples',
              'learner':learner
    }

    # run the experiment
    expt.Expt(params).run()
