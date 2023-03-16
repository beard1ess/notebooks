import mido
from mido import Message, MidiFile, MidiTrack

chords = {
    'C': ['C', 'E', 'G'],
    'D': ['D', 'F#', 'A'],
    'E': ['E', 'G#', 'B'],
    'F': ['F', 'A', 'C'],
    'G': ['G', 'B', 'D'],
    'A': ['A', 'C#', 'E'],
    'B': ['B', 'D#', 'F#'],
    'Cm': ['C', 'Eb', 'G'],
    'Dm': ['D', 'F', 'A'],
    'Em': ['E', 'G', 'B'],
    'Fm': ['F', 'Ab', 'C'],
    'Gm': ['G', 'Bb', 'D'],
    'Am': ['A', 'C', 'E'],
    'Bm': ['B', 'D', 'F#'],
}

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

def create_midi_file(chords, output_filename='output.mid', duration=480):
    midi_file = MidiFile()
    track = MidiTrack()
    midi_file.tracks.append(track)

    for chord_notes in chords:
        for note in chord_notes:
            midi_note = note_to_midi_pitch(note + '3')
            track.append(Message('note_on', note=midi_note, velocity=64, time=0))
        track.append(Message('note_off', note=midi_note, velocity=64, time=duration))

    midi_file.save(output_filename)

chord_progression = input("Enter a chord progression separated by commas: ").split(', ')
notes = get_notes(chord_progression)

for chord, chord_notes in zip(chord_progression, notes):
    print(f"{chord}: {', '.join(chord_notes)}")

create_midi_file(notes)
