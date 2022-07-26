"""Test creating Cloze cards"""
# https://apps.ankiweb.net/docs/manual20.html#cloze-deletion

import sys
from genanki import Model
from genanki import Note
from genanki import Deck
from genanki import Package


CSS = """.card {
 font-family: arial;
 font-size: 20px;
 text-align: center;
 color: black;
 background-color: white;
}
.cloze {
 font-weight: bold;
 color: blue;
}
.nightMode .cloze {
 color: lightblue;
}
"""

MY_CLOZE_MODEL = Model(
  998877661,
  'My Cloze Model',
  fields=[
    {'name': 'Text'},
    {'name': 'Extra'},
  ],
  templates=[{
    'name': 'My Cloze Card',
    'qfmt': '{{cloze:Text}}',
    'afmt': '{{cloze:Text}}<br>{{Extra}}',
  }, ],
  css=CSS,
  model_type=Model.CLOZE)

my_model = Model(
  1607392319,
  'Simple',
  fields=[
    {'name': 'Question'},
    {'name': 'Answer'},
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Question}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
    },
  ])



def test_cloze():
  """Test Cloze model"""




def _wr_apkg(notes):
  """Write cloze cards to an Anki apkg file"""
  deckname = 'mtherieau'
  deck = Deck(deck_id=3759374, name=deckname)
  for note in notes:
    deck.add_note(note)
  fout_anki = '{NAME}.apkg'.format(NAME=deckname)
  Package(deck).write_to_file(fout_anki)
  print('  {N} Notes WROTE: {APKG}'.format(N=len(notes), APKG=fout_anki))




if __name__ == '__main__':
  notes = []

  fields = ['NOTE ONE: {{c1::single deletion}}', 'Extra']
  my_cloze_note = Note(model=MY_CLOZE_MODEL, fields=fields)
  assert {card.ord for card in my_cloze_note.cards} == {0}
  notes.append(my_cloze_note)




  _wr_apkg(notes)
