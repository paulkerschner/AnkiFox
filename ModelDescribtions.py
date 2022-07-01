from genanki import Model
from genanki import Note
from genanki import Deck
from genanki import Package



MY_CLOZE_MODEL = Model(
    998877661,
    'Import Cloze',
    fields=[
        {'name': 'Text'},
        {'name': 'Extra'},
    ],
    templates=[{
        'name': 'Import Cloze Card',
        'qfmt': '{{cloze:Text}}',
        'afmt': '{{cloze:Text}}<br>{{Extra}}',
    }, ],
    model_type=Model.CLOZE)

MY_AllInOne_MODEL = Model(
    998877758,
    'Import AllInOne',
    fields=[
        {'name': 'Title'},
        {'name': 'Question'},
        {'name': 'QType (0=kprim,1=mc,2=sc)'},
        {'name': 'Q_1'},
        {'name': 'Q_2'},
        {'name': 'Q_3'},
        {'name': 'Q_4'},
        {'name': 'Q_5'},
        {'name': 'Answers'},
        {'name': 'Source'},
        {'name': 'Extra 1'},
    ],
    templates=[{
        'name': 'Import AllInOne Card',
        'qfmt': '{{#Title}}<h3 id="myH1">{{Title}}</h3>{{/Title}}',
        'afmt': '{{#Question}}<p>{{Question}}</p>{{/Question}}',
    }, ],
    model_type=Model.FRONT_BACK)