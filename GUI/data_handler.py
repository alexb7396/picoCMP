import tkinter
from tkinter import ttk
import struct
import binascii
import serial
import time

# Lookup table for C1 and C0 configuration of LTC2627
lookup_table_C1C0 = [
    ['Gnd',     'Gnd',      '00010000'],
    ['Gnd',     'Float',    '00010001'],
    ['Gnd',     'Vcc',      '00010010'],
    ['Float',   'Gnd',      '00010011'],
    ['Float',   'Float',    '00100000'],
    ['Float',   'Vcc',      '00100001'],
    ['Vcc',     'Gnd',      '00100010'],
    ['Vcc',     'Float',    '00100011'],
    ['Vcc',     'Vcc',      '00110000'],
]

# Lookup table for A1 and A0 configuration of AD5673
lookup_table_A1A0 = [
    ['Gnd', 'Gnd', '00001100'],
    ['Gnd', 'Vcc', '00001101'],
    ['Vcc', 'Gnd', '00001110'],
    ['Vcc', 'Vcc', '00001111'],
]

# DAC addresses for channel selection
dac_addresses = [
    "0000", "0001", "0010", "0011",
    "0100", "0101", "0110", "0111",
    "1000", "1001", "1010", "1011",
    "1100", "1101"
]

# Command value to be used (0011 shifted left by 4)
command = 48  # 0x30 in hexadecimal

# Array to store byte sequences generated for DACs
array_of_bytes = []

class DataHandler:
    def __init__(self):
        # Dictionary to store the previous threshold values for persistence
        self.previous_threshold_data = {}

    def find_address(self, address, lookup_table, key):
        """Finds the address from the lookup table based on the input key values."""
        for row in lookup_table:
            if row[0] == address[key[0]] and row[1] == address[key[1]]:
                return row[2]  # Return the address from the table
        return None 

    def get_address(self, ca1, ca2):
        """ Retrieves the address for given C1 and C0 values. """
        for row in lookup_table_C1C0:
            if row[0] == ca1 and row[1] == ca2:
                return row[2]
        return "Address not found: check the ca1 and ca2 values"

    def handle_data(self, i2c_data, threshold_data):
        """
        Processes the I2C data and threshold values, generating byte sequences for DAC configuration. """
        # Find LTC and AD56 I2C addresses
        ltc_address = int(self.find_address(i2c_data, lookup_table_C1C0, ["C1", "C0"]), 2)
        ad56_address = int(self.find_address(i2c_data, lookup_table_A1A0, ["A1", "A0"]), 2)
        
        # Extract threshold data as a list
        threshold_data = list(threshold_data.values())

        # Iterate over 16 channels to configure DACs
        for i in range(16):
            msb, lsb = self.map_value_to_16bit(float(threshold_data[i]))
            
            if i < 2:
                dac_bytes = self.construct_dac_bytes(
                    ltc_address,
                    dac_addresses[i],
                    command,
                    msb,
                    lsb,
                    "LTC ",
                    i
                )
            else:
                dac_bytes = self.construct_dac_bytes(
                    ad56_address,
                    dac_addresses[i - 2],
                    command,
                    msb,
                    lsb,
                    "AD56 ",
                    i-2
                )

            # Append the constructed bytes to the array
            array_of_bytes.append(dac_bytes)
            print("tipo di array:", type(array_of_bytes[0]))

        ser = serial.Serial('COM5', 9600)  # Usa la porta seriale corretta per il tuo sistema
        for data in array_of_bytes:
            ser.write(data)
            time.sleep(0.01)
        ser.close()

    def construct_dac_bytes(self, device_address, dac_address_bin, command, msb, lsb, device_label, index_dac):
        """ Constructs the byte sequence for a DAC configuration. """

        # Compute DAC address by combining command and DAC binary address
        dac_address = command + int(dac_address_bin, 2)
        
        # Pack individual bytes into a single binary structure
        device_address_bytes = struct.pack('>B', device_address)
        dac_address_bytes = struct.pack('>B', dac_address)
        msb_bytes = struct.pack('>B', msb)
        lsb_bytes = struct.pack('>B', lsb)

        # Combine all bytes into a single sequence
        full_bytes = device_address_bytes + dac_address_bytes + msb_bytes + lsb_bytes

        # Convert byte sequence to binary string for readability
        full_bytes_bin = ' '.join(format(byte, '08b') for byte in full_bytes)

        # Print the byte sequence in hexadecimal and binary format
        print(f"{device_label}{index_dac} hex:", end="\t")
        print(''.join(f'{data:02x}' for data in full_bytes), end="\t")
        print(f"bin: {full_bytes_bin}")

        return full_bytes

    def map_value_to_16bit(self, x):
        """ Maps a threshold value to a 16-bit representation."""
        mapped_value = int(((-x + 1.25) / 2.5) * 4095)

        # Ensure the value is within valid range
        if mapped_value > 4095:
            mapped_value = 4095
        elif mapped_value < 0:
            mapped_value = 0

        msb = mapped_value >> 4
        lsb = (mapped_value & 0xF) << 4

        return msb, lsb
    
    def get_i2c_address(self):
        """Retrieves I2C address configuration from comboboxes."""
        i2c_data = {
            "A1": self.combobox_A1.get(),
            "A0": self.combobox_A0.get(),
            "C1": self.combobox_C1.get(),
            "C0": self.combobox_C0.get(),
        }
        return i2c_data

    def get_threshold(self):
        """ Retrieves threshold values entered in the GUI and applies "Set All Thresholds" if applicable."""
        set_all_value = self.set_all_entry.get()
        threshold_data = {}

        if set_all_value:
            for label, entry in self.threshold_entries.items():
                if label in [f"In{i}" for i in range(1, 15)]:
                    entry.delete(0, tkinter.END)
                    entry.insert(0, set_all_value)
                    threshold_data[label] = set_all_value
                elif label in ["In0_A", "In0_B/Trigger"]:
                    current_value = entry.get()
                    if current_value.strip():
                        threshold_data[label] = current_value
                    else:
                        threshold_data[label] = self.previous_threshold_data.get(label, "")
        else:
            for label, entry in self.threshold_entries.items():
                current_value = entry.get()
                if current_value.strip():
                    threshold_data[label] = current_value
                else:
                    threshold_data[label] = self.previous_threshold_data.get(label, "")

        self.previous_threshold_data = threshold_data

        return threshold_data
