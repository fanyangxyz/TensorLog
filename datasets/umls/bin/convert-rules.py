import sys
import re

#ALLRELS = ['also_see', 'derivationally_related_form', 'has_part',
#           'hypernym', 'hyponym', 'instance_hypernym', 'instance_hyponym',
#           'member_holonym', 'member_meronym', 'member_of_domain_region',
#           'member_of_domain_topic', 'member_of_domain_usage', 'part_of',
#           'similar_to', 'synset_domain_region_of', 'synset_domain_topic_of',
#           'synset_domain_usage_of', 'verb_group']

ALLRELS = [
        'method_of',
        'interconnects',
        'produces',
        'disrupts',
        'measurement_of',
        'occurs_in',
        'indicates',
        'conceptually_related_to',
        'manages',
        'precedes',
        'conceptual_part_of',
        'property_of',
        'causes',
        'connected_to',
        'affects',
        'contains',
        'exhibits',
        'performs',
        'degree_of',
        'adjacent_to',
        'part_of',
        'complicates',
        'process_of',
        'surrounds',
        'measures',
        'assesses_effect_of',
        'diagnoses',
        'analyzes',
        'consists_of',
        'uses',
        'carries_out',
        'derivative_of',
        'developmental_form_of',
        'manifestation_of',
        'evaluation_of',
        'treats',
        'ingredient_of',
        'location_of',
        'prevents',
        'associated_with',
        'practices',
        'co-occurs_with',
        'interacts_with',
        'result_of',
        'issue_in',
        'isa',
        ]

def cvtRules(fIn,fOut,rIdOut):
    rn = 0
    fp = open(fOut,'w')
    fp2 = open(rIdOut,'w')
    #regex = re.compile('^(\w+)\((\w+),(.*)')
    regex = re.compile( '^(\w+)\((\w+(?:(-\w+)|\w+)),(.*)')
    def fixLit(lit):
        m = regex.match(lit) 
        return '%s(%s' % (m.group(2),m.group(3))

    for rel in ALLRELS:
        fp.write('i_%s(X,Y) :- %s(X,Y) {i_%s}.\n' % (rel,rel,rel)) 
        fp2.write('rule\ti_%s\n' % rel)

    for line in open(fIn):
        rn += 1
        if not line.startswith("#") and not line.startswith("interp(P") and not line.startswith("learnedPred(P") and line.strip():
            try:
                head,bodyFeat = line.strip().split(" :- ")
                body,feat0 = bodyFeat.split(" {")
                bodyLits = body.split(", ")
                fp.write(fixLit(head))
                fp.write(' :- ')
                fp.write(", ".join(map(fixLit,bodyLits)))
                fp.write(' {r%d}.\n' % rn)
                fp2.write('rule\tr%d\n' % rn)
            except:
                print(bodyLits)
if __name__ == "__main__":
    cvtRules('raw/train-learned.ppr','inputs/umls-learned.ppr', 'inputs/umls-ruleids.cfacts')
