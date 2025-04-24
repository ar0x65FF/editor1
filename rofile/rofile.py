from dataclasses import dataclass
from typing import List

@dataclass
class SongData:
    tone: List[bytes]
    obligato: List[bytes]
    chord: List[bytes]

@dataclass
class Song:
    address: int
    tone_addr: int
    obligato_addr: int
    chord_addr: int
    songdata: SongData
    endofdata: int

class ROMPackData:
    def __init__(self):
        self.header = b'\x5A\x00\x00'
        self.footer_address: int
        self.song_count: int
        self.endofdata: int
        self.songs: List[Song] = []
        self.endofdataplus3: int

    def swap_songs(self, i, j):
        self.songs[i], self.songs[j] = self.songs[j], self.songs[i]

    

    def read_3_bytes_address(self,f) -> int:
        b = f.read(3)

        if len(b) < 3:
            raise EOFError("Error!")
        
        address = int(int.from_bytes(b[::-1], byteorder="big")/2)
        return address

    def read_data_3byte(self, f, stop_marker=b'\xF0\x00\x00') -> List[bytes]:
        data = []
        while True:
            chunk = f.read(3)
            data.append(chunk)
            if chunk == stop_marker or len(chunk) < 3:
                break;
        return data

    def read_data_2byte(self, f, stop_marker=b'\xF0\x00') -> List[bytes]:
        data = []
        while True:
            chunk = f.read(2)
            data.append(chunk)
            if chunk == stop_marker:
                break
        return data
    
    def read_2byte(self, f) -> int:
        data = f.read(2)
        parsed_data = int(int.from_bytes(data[::-1], byteorder="big"))
        return parsed_data
    
    
    def readfile(self, filename: str):
        with open(filename, "rb") as f:
            header = f.read(3)
            if header != b'\xA5\x00\x00':
                #raise ValueError("Invalid Header")
                return 1
            
            self.footer_address = self.read_3_bytes_address(f)
            self.song_count = self.read_2byte(f)
            self.endofdata = self.read_3_bytes_address(f)

            addresses = [self.read_3_bytes_address(f) for _ in range(self.song_count)]

            top_pos = f.tell()
            for addr in addresses:
                current_pos = f.tell()
                f.seek(addr)
                
                tone_hdr = f.read(1)
                if tone_hdr == b'\x00':
                    tone_addr = self.read_3_bytes_address(f)
                else:
                    return 2

                obligato_hdr = f.read(1)
                if obligato_hdr == b'\x10':
                    obligato_addr = self.read_3_bytes_address(f)
                else:
                    return 3
                
                chord_hdr = f.read(1)
                if chord_hdr == b'\x02':
                    chord_addr = self.read_3_bytes_address(f)
                else:
                    return 4

                endofdata_hdr = f.read(1)
                if endofdata_hdr == b'\xFF':
                    endofdata_s = self.read_3_bytes_address(f)
                else:
                    return 5

                #Tone
                f.seek(tone_addr)
                tone_data = self.read_data_3byte(f)

                #Obligato
                f.seek(obligato_addr)
                obligato_data = self.read_data_3byte(f)

                #Chord
                f.seek(chord_addr)
                chord_data = self.read_data_2byte(f)

                songdata = SongData(tone=tone_data, obligato=obligato_data, chord=chord_data)
                self.songs.append(Song(address=addr, songdata=songdata, endofdata=endofdata_s, tone_addr=tone_addr, obligato_addr=obligato_addr, chord_addr=chord_addr))
                f.seek(current_pos)
            f.seek(top_pos)
            self.endofdataplus3 = self.read_3_bytes_address(f)
        return 0

    def write_address_3byte(self, address):
        dst_address = address * 2;
        return dst_address.to_bytes(3, byteorder="little")
    
    def writefile(self, filename: str):
        data = bytearray()
        data.extend([0xA5, 0x00, 0x00])
        footer_last_24 = len(data)
        data.extend(b'\x00\x00\x00')
        
        data.extend(len(self.songs).to_bytes(2, "little"))
        end_of_data = len(data)
        data.extend(b'\xEE\xEE\xEE')

        song_addresses_placeholder = []

        
        for song in self.songs:
            song_addresses_placeholder.append(len(data))
            data.extend(b"\x00\x00\x00")
        
        end_of_data_p3 = len(data)
        data.extend(b"\xFF\xFF\xFF")
        
        song_start_addresses = []

        for i, song in enumerate(self.songs):
            song_start_addresses.append(len(data))

            data[song_addresses_placeholder[i]:song_addresses_placeholder[i]+3] = self.write_address_3byte(len(data))

            data.extend(b"\x00")
            tone_start_placeholder = len(data)
            data.extend(b"\x00\x00\x00")

            data.extend(b"\x10")
            obligato_start_placeholder = len(data)
            data.extend(b"\x00\x00\x00")

            data.extend(b"\x02")
            chord_start_placeholder = len(data)
            data.extend(b"\x00\x00\x00")

            data.extend(b"\xFF")
            end_of_song_placeholder = len(data)
            data.extend(b"\x00\x00\x00")
             
            

            data[tone_start_placeholder:tone_start_placeholder+3] = self.write_address_3byte(len(data))
            chunk_tone = bytearray()
            for chunk in song.songdata.tone:
                chunk_tone += chunk
            
            data += chunk_tone

            data[obligato_start_placeholder:obligato_start_placeholder+3] = self.write_address_3byte(len(data))
            chunk_obligato = bytearray()
            for chunk in song.songdata.obligato:
                chunk_obligato += chunk
            
            data += chunk_obligato

            data[chord_start_placeholder:chord_start_placeholder+3] = self.write_address_3byte(len(data))
            chunk_chord = bytearray()
            for chunk in song.songdata.chord:
                chunk_chord += chunk
            
            data += chunk_chord

            data[end_of_song_placeholder:end_of_song_placeholder+3] = self.write_address_3byte(len(data))


            data[end_of_data:end_of_data+3] = self.write_address_3byte(len(data))
            data[end_of_data_p3:end_of_data_p3+3] = self.write_address_3byte(len(data)+3)

            
        file_size = len(data)
        if file_size <= 6*1024+24:
            zerofillin = 6 * 1024
        elif file_size <= 8*1024+24:
            zerofillin = 8*1024
        elif file_size <= 16*1024+24:
            zerofillin = 16*1024
        else:
            zerofillin = 32*1024
        
        data += b'\x00' * (zerofillin - file_size - 24)

        data[footer_last_24:footer_last_24+3] = self.write_address_3byte(len(data))
        data.extend(b"\x23\x83\x93\x06\x47\x83\xAB\x02\x63\x27\x4B\x27\x47\x93\x2B\x83\xFF\xFF\xFF\xFF\x00\x00\x00\x00")

        with open(filename, "wb") as f:
            f.write(data)

    def loadsongpart(self, filename: str):
        with open(filename, "rb") as f:
            tone_data = self.read_data_3byte(f)
            obligato_data = self.read_data_3byte(f)
            chord_data = self.read_data_2byte(f)
            songdata = SongData(tone=tone_data, obligato=obligato_data, chord=chord_data)
            self.songs.append(Song(address=1, songdata=songdata, endofdata=1, tone_addr=0x00, obligato_addr=0x10, chord_addr=0x02))
            self.song_count = self.song_count + 1