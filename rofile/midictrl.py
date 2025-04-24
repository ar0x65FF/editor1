from typing import List
import mido
import time

class PartMidiControl:
    def __init__(self):
        self.mido = mido.MidiFile(ticks_per_beat=480)
    def rnote_midi(self, note):
        octave = (note & 0xF0) >> 4
        key = note & 0x0F
        return (octave * 12 + (key-1))+12        
    def writemidifile(self, data_1: List[bytes], data_2: List[bytes], filename='output.mid'):
        self.writemiditrack2(data_1, 0)
        self.writemiditrack2(data_2, 1)
        self.mido.save(filename=filename)
    def to_instrument(self, track, instrument=0, channel=0, time=0):
        inst_tone = {
            0x00:   0,
            0x10:   7,
            0x20:   18,
            0x30:   40,
            0x40:   73,
            0x50:   71,
            0x60:   56,
            0x70:   8,
        }
        inst_oblg = {
            0x00:   0,
            0x10:   0,
            0x20:   71,
            0x30:   73,
            0x40:   73,
            0x50:   71,
            0x60:   71,
            0x70:   8,
        }

        if channel == 0:
            track.append(mido.Message('program_change', program=inst_tone[instrument], channel=channel, time=time))
        elif channel == 1:
            track.append(mido.Message('program_change', program=inst_oblg[instrument], channel=channel, time=time))
    
    def ticks_to_midi_time(self, val):
        if val < 0:
            return 0
        return int(round(val * (480/0x18)))

    def writemiditrack2(self,data: List[bytes], channel=0):
        track = mido.MidiTrack()
        self.mido.tracks.append(track)

        time_before_next_event = 0
        last_byte3 = 0

        for i,chunk in enumerate(data):
            b1, b2, b3 = chunk
            current_event_time = time_before_next_event
            
            if b1 == 0x10:
                rest_ticks = b2
                new_rest_ticks = self.ticks_to_midi_time(rest_ticks)
                time_before_next_event += new_rest_ticks
                current_event_time += rest_ticks
                last_byte3 = b3
            elif b1 == 0x20:
                high_byte = b3
                low_byte = last_byte3
                combined_rest = (high_byte<<8) | low_byte
                extended_rest = self.ticks_to_midi_time(combined_rest)
                time_before_next_event += extended_rest
            elif b1 == 0x50:
                time_before_next_event = 0
                rest_ticks = self.ticks_to_midi_time(b3)
                time_before_next_event = rest_ticks
            elif b1 == 0x60:
                time_before_next_event = 0
                rest_ticks = self.ticks_to_midi_time(b3)
                time_before_next_event = rest_ticks
                if 0x00 <= b2 <= 0x70:
                    self.to_instrument(track=track, instrument=b2, channel=channel, time=current_event_time)
                elif 0x80 <= b2 <= 0xF0:
                    continue
            elif 0x31 <= b1 <= 0x65 and (b1 & 0x0F) != 0:
                midi_note = self.rnote_midi(b1)
                note_duration_ticks = self.ticks_to_midi_time(b2)

                track.append(mido.Message('note_on', note=midi_note,velocity=64,time=current_event_time,channel=channel))
                track.append(mido.Message('note_off', note=midi_note,velocity=0,time=note_duration_ticks,channel=channel))
                rest_ticks = self.ticks_to_midi_time(b3)
                time_before_next_event = rest_ticks
                last_byte3 = b3
                """
                if note_duration_ticks <= 0:
                    rest_ticks = self.ticks_to_midi_time(b3)
                    time_before_next_event = rest_ticks
                    last_byte3 = b3
                else:
                    track.append(mido.Message('note_on', note=midi_note,velocity=64,time=current_event_time,channel=channel))
                    track.append(mido.Message('note_off', note=midi_note,velocity=0,time=note_duration_ticks,channel=channel))
                    rest_ticks = self.ticks_to_midi_time(b3)
                    time_before_next_event = rest_ticks
                    last_byte3 = b3
                """
            else:
                print(f"Unknown command Position\t{i}\tChannel\t{channel}\t{hex(b1)} {hex(b2)} {hex(b3)}")
                #time_before_next_event = 0
                #last_byte3 = 0
    
    def midi_to_casio_note(self, midi_note:int):
        if not (0 <= midi_note <= 127):
            print("OUTOFRANGE!")
        key = (midi_note % 12) + 1
        octave = midi_note//12
        return (octave << 4) | key

    def ticks_to_hex(self, ticks):
        if ticks < 0:
            ticks = 0
        calculated_ticks = ticks * (24.0/480)
        hex_value = int(round(calculated_ticks))
        return max(0,hex_value)
    
    def encode_rest_to_command(self, rest_ticks):
        commands = []
        target_hex_value = self.ticks_to_hex(rest_ticks)
        if target_hex_value == 0:
            return {'byte3_for_prev': 0x00, 'extra_commands': []}
        if target_hex_value > 0xFF:
            if target_hex_value > 0xFFFF:
                print("error 1")
            low_byte = target_hex_value & 0xFF
            high_byte = (target_hex_value >> 8) & 0xFF
            commands.append([0x20,0x00,high_byte])
            return {'byte3_for_prev': low_byte, 'extra_commands': commands}
        else:
            return {'byte3_for_prev': target_hex_value, 'extra_commands': commands}

    def part_converter(self, src_filename: str, dst_filename: str):
        try:
            mid = mido.MidiFile(src_filename)
        except Exception as e:
            print(f"Error opening MIDI file {src_filename}: {e}")
            return None
        inst_tone = {
            0:      0x00,
            7:      0x10,
            18:     0x20,
            40:     0x30,
            73:     0x40,
            71:     0x50,
            56:     0x60,
            8:      0x70,
        }
        
        output_data = []
        active_notes = {}
        accumulated_delta_ticks = 0
        current_absolute_tick = 0
        last_command_index = -1
        for i,track in enumerate(mid.tracks):
            for j,msg in enumerate(track):
                accumulated_delta_ticks += msg.time
                current_absolute_tick += msg.time

                if msg.type == 'note_on' and msg.velocity > 0:
                    if msg.note in active_notes:
                        print(f"Warning: Note {msg.note} retriggered at tick {current_absolute_tick} before note_off. Handling sequentially.")
                    active_notes[msg.note] = {
                        'start_tick_abs': current_absolute_tick,
                        'velocity': msg.velocity,
                        'delta_before': accumulated_delta_ticks
                    }
                    accumulated_delta_ticks = 0
                elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                    if msg.note in active_notes:
                        note_info = active_notes.pop(msg.note)
                        note_duration_ticks = current_absolute_tick - note_info['start_tick_abs']
                        rest_ticks_before_note = note_info['delta_before']
                        
                        rest_encoding = self.encode_rest_to_command(rest_ticks_before_note)

                        if last_command_index >= 0:
                            output_data[last_command_index][2] = rest_encoding['byte3_for_prev']
                            output_data.extend(rest_encoding['extra_commands'])
                        elif rest_ticks_before_note > 0:
                            print(f"Note: Initial rest of {rest_ticks_before_note} ticks detected before first note.")
                            initial_rest_hex = self.ticks_to_hex(rest_ticks_before_note)
                            if initial_rest_hex <= 0xFF:
                                pass
                            else:
                                low = initial_rest_hex & 0xFF
                                high = (initial_rest_hex>>8) & 0xFF
                                output_data.append([0x20,0x00, high])
                        try:
                            byte1 = self.midi_to_casio_note(msg.note)
                        except ValueError as e:
                            print(f"Skipping note event due to error: {e}")
                            continue # Skip this note event
                        
                        byte2_duration = self.ticks_to_hex(note_duration_ticks)
                        if byte2_duration > 0xFF:
                            print(f"Warning: Note duration {note_duration_ticks} ticks converts to hex {hex(byte2_duration)} > 0xFF. Clamping byte2.")
                            byte2_duration = 0xFF
                        
                        new_command = [byte1, byte2_duration, 0x00]
                        output_data.append(new_command)
                        last_command_index = len(output_data) - 1

                        accumulated_delta_ticks = 0
                    else:
                        print(f"Warning: Encountered note_off for note {msg.note} at tick {current_absolute_tick} which was not tracked as active.")

                elif msg.type == 'program_change':
                    rest_ticks_before_pc = accumulated_delta_ticks
                    rest_encoding = self.encode_rest_to_command(rest_ticks_before_pc)

                    if last_command_index >= 0:
                        output_data[last_command_index][2] = rest_encoding['byte3_for_prev']
                        output_data.extend(rest_encoding['extra_commands'])
                    elif rest_ticks_before_pc > 0:
                        print(f"Note: Initial rest of {rest_ticks_before_pc} ticks detected before first program change.")
                        initial_rest_hex = self.ticks_to_hex_code(rest_ticks_before_pc)
                        if initial_rest_hex <= 0xFF:
                            pass
                        else:
                            low = initial_rest_hex & 0xFF
                            high = (initial_rest_hex >> 8) & 0xFF
                            output_data.append([0x20, 0x00, high])

                    byte1 = 0x60
                    byte2 = inst_tone[msg.program]
                    new_command = [byte1, byte2, 0x00]
                    output_data.append(new_command)
                    last_command_index= len(output_data)-1

                elif msg.type == 'end_of_track':
                    if accumulated_delta_ticks > 0:
                        print(f"Handling final rest of {accumulated_delta_ticks} ticks.")
                        rest_encoding = self.encode_rest_to_commands(accumulated_delta_ticks)
                        if last_command_index >= 0:
                            output_data[last_command_index][2] = rest_encoding['byte3_for_prev']
                            output_data.extend(rest_encoding['extra_commands'])
                        else:
                            print("A")
                    break
        with open(dst_filename, 'wb') as f:
            for i,msg in enumerate(output_data):
                #print(f"[{i}] ", end="")
                b = bytearray()
                for j,cmd in enumerate(msg):
                    b.append(cmd)
                    #print(f"{hex(cmd)} ", end="")
                f.write(b)
                #print("\n")