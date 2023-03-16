import mido
from mido import Message, MidiFile, MidiTrack

root_notes = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'G#', 'A', 'Bb', 'B']
chord_types = {
    '': [0, 4, 7],
    'm': [0, 3, 7],
    'dim': [0, 3, 6],
    'aug': [0, 4, 8],
    '7': [0, 4, 7, 10],
    'Maj7': [0, 4, 7, 11],
    'm7': [0, 3, 7, 10],
    'dim7': [0, 3, 6, 9],
    'mMaj7': [0, 3, 7, 11],
    'aug7': [0, 4, 8, 10],
}

def note_name(pitch_class):
    return root_notes[pitch_class % 12]

def transpose(note, interval):
    index = root_notes.index(note)
    return note_name(index + interval)

def create_chord_map():
    chord_map = {}
    for root in root_notes:
        for chord_type, intervals in chord_types.items():
            chord_name = root + chord_type
            chord_notes = [transpose(root, interval) for interval in intervals]
            chord_map[chord_name] = chord_notes
    return chord_map

chords = create_chord_map()

def note_to_midi_pitch(note):
    pitch_map = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
    octave = int(note[-1]) + 1
    pitch_class = note[0]
    pitch_modifier = note[1] if len(note) > 2 else None

    pitch = pitch_map[pitch_class] + (octave * 12)
    if pitch_modifier == '#':
        pitch += 1
    elif pitch_modifier == 'b':
        pitch -= 1

    return pitch

def get_notes(chord_progression):
    notes = []
    for chord in chord_progression:
        if chord in chords:
            notes.append(chords[chord])
        else:
            print(f"Chord {chord} not recognized.")
    return notes

def create_midi_file(chords, output_filename='output.mid', duration=1920):
    midi_file = MidiFile()
    track = MidiTrack()
    midi_file.tracks.append(track)

    for chord_notes in chords:
        for note in chord_notes:
            midi_note = note_to_midi_pitch(note + '3')
            track.append(Message('note_on', note=midi_note, velocity=64, time=0))
        for note in chord_notes:
            midi_note = note_to_midi_pitch(note + '3')
            track.append(Message('note_off', note=midi_note, velocity=64, time=duration))

    midi_file.save(output_filename)

chord_progression = input("Enter a chord progression separated by commas: ").split(', ')
notes = get_notes(chord_progression)

for chord, chord_notes in zip(chord_progression, notes):
    print(f"{chord}: {', '.join(chord_notes)}")

create_midi_file(notes)
