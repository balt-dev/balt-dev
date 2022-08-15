from pathlib import Path
import sys
import os

def clean_error(msg: str):
    sys.stderr.write(msg+'\n')
    sys.exit(1)

try:
    import pretty_midi
except ModuleNotFoundError:
    clean_error('It seems you don\'t have the Pretty MIDI package installed.\nTry typing "pip install pretty_midi" into your console.')

def clear_console():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

try:
    i = Path(sys.argv[1])
except:
    clean_error(f'Please provide a file path to a midi file.\nTry "{"py" if os.name == "nt" else "python"} playnotes.py [filepath]".')

if not (i.is_file() and i.suffix in ['.mid', '.midi']):
    clean_error('The file path input is not a midi file or does not exist.')

try:
    mid = pretty_midi.PrettyMIDI(str(i.resolve()))
except EOFError:
    clean_error('It seems that midi file is corrupted. Try another one?')
    
clear_console()
for i, instrument in enumerate(mid.instruments):
    print(i, pretty_midi.program_to_instrument_name(instrument.program), f'({len(instrument.notes)} notes)')
print('\n\nWhich instrument do you want to turn into a command?')
i = input('> ')
while not (i.isdigit() and int(i) in range(len(mid.instruments))):
    clear_console()
    for i, instrument in enumerate(mid.instruments):
        print(i, pretty_midi.program_to_instrument_name(instrument.program), f'({len(instrument.notes)} notes)')
    print('\n\nWhich instrument do you want to turn into a command?')
    i = input('> ')
inst_index = int(i)

clear_console()
transpose_amount = input('How many half-steps do you want to transpose?\n\n> ')
while not (str(transpose_amount).lstrip('-').isdigit()):
    clear_console()
    transpose_amount = input('How many half-steps do you want to transpose?\n\n> ')

clear_console()
transpose_amount = int(transpose_amount)
inst = mid.instruments[inst_index]
notes = inst.notes
output = []
for i, note in enumerate(notes):
    note_number = note.pitch + transpose_amount
    if note_number < 18:
        note_number = ((note_number - 30) % 12) + 30
    elif note_number >= 42:
        note_number = ((note_number - 30) % 12) + 30
    note_name = pretty_midi.note_number_to_name(note_number)
    output.append(note_name)
    try:
        note_length = int((notes[i+1].start - note.start)*20)
        output.append(str(note_length))
    except IndexError:
        pass
    if len(','.join(output)) + 10 >= 250:
        print('Hit the chat limit!')
        break

print(f'Here\'s your command:\n\n@playnotes {",".join(output)}\n\nHave a good day!')