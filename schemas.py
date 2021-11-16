english_schemas = '''english_words (
id integer primary key,
name text not null,
definition text not null,
wiktionary_entry integer not null
);
'''

old_english_schemas = '''old_english_words (
id integer primary key,
name text not null,
definition text not null,
wiktionary_entry integer not null
);
'''

translations_schemas = '''translations (
id integer primary key,
ne integer not null,
oe integer not null,
foreign key (ne) references english_words(id),
foreign key (oe) references old_english_words(id)
);
'''

conjugations_schemas = '''conjugations (
id integer primary key,
word integer not null,
person text,
plurality text,
mood text,
tense text,
conjugation text not null,
foreign key (word) references old_english_words(id)
);
'''

declensions_schemas = '''declensions (
id integer primary key,
word integer not null,
case text,
plurality text,
declension text not null,
foreign key (word) references old_english_words(id)
);
'''


schemas = [
    english_schemas,
    old_english_schemas,
    translations_schemas,
    conjugations_schemas,
    declensions_schemas
]

triggers = [
]

views = [
]

record_typing = {
    'english_words': '(name, definition, wiktionary_entry)',
    'old_english_words': '(name, definition, wiktionary_entry)',
    'translations': '(ne, oe)',
    'conjugations': '(word, person, plurality, mood, tense, conjugation)',
    'declensions': '(word, case, plurality, declension)'
}
