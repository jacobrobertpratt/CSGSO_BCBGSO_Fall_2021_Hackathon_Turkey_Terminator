import re
from typing import List

case_list: List[str] = ['oblique', 'genitive', 'dative', 'accusative', 'nominative', 'instrumental']
plurality_list: List[str] = ['singular', 'plural']

cases = r'(oblique|genitive|dative|accusative|nominative|instrumental|gen|acc|nom)'
case_capture = r'(?P<cases>{0}((/| ){0})*)'.format(cases)
plurality = r'(?P<plurality>(singular|plural)(/(singular|plural))*)'
person = r'(?P<person>(first|second|third)(/(first|second|third))*-person)'

root_reference = r'( ?of (?P<word>(\*|\w|-)+))?'

noun_declensions = re.compile(r'^(?P<alt>alternative )?'
                              r'{0}?'
                              r'( ?{1})?{2}'.format(case_capture, plurality, root_reference))

verb_conjugations = re.compile(r'((inflected|'
                               r'((?P<participle>(past|present) participle)|'
                               r'({1}))|{0}|simple|preterite|'
                               r'(?P<mood>indicative|subjunctive|imperative)|'
                               r'(supine )?infinitive|(?P<tense>past|present)( tense)?) ?)+{2}'
                               .format(plurality, person, root_reference))

adjective_conjugation = re.compile(r'(((?P<strength>(strong|weak)(/(strong|weak))*)|'
                                   r'(?P<gender>(masculine|feminine|neuter)(/(masculine|feminine|neuter))*)|'
                                   r'{0}|{1}|'
                                   r'(?P<degree>(superlative|comparative)(/(superlative|comparative))*( degree)?)|'
                                   r'form|and|(?P<inflection>Inflected)) ?)+{2}'
                                   .format(plurality, case_capture, root_reference))
