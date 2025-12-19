''' Program for the generation of Sine, Triangular, and Square waveforms
    using the AD9833(DDS) module, controlled via the ExpEYES-17 experimental platform using Python.
    Date: 19_12_2025 by Dr. Ujjwal Ghanta
'''
import time
import sys
import eyes17.eyes # Import the library for ExpEYES-17

# --- AD9833 Class Definition ---
class AD9833:
    # Use 25 MHz as the default DDS clock for ExpEYES-17
    DDS_CLOCK = 25000000.0 
    DDS_MAX_FREQ = 268435456
    
    # Control bytes (Register Addresses and Control Bits)
    DDS_B28 = 13
    DDS_FSELECT = 11
    DDS_RESET = 8
    DDS_OPBITEN = 5
    DDS_MODE = 1

    DDS_SINE = (0)
    DDS_TRIANGLE = (1<<DDS_MODE)
    DDS_SQUARE = (1<<DDS_OPBITEN)
    
    def __init__(self, I=None):
        # Using 'CS1' as confirmed by the user
        self.CS = 'CS1' 
        if I:
            self.I = I
        else:
            from SEEL import interface 
            self.I = interface.connect()
            
        # Set SPI parameters: 2 bytes per word, CPOL=1, CPHA=1 (Mode 3)
        self.I.SPI.set_parameters(2, 2, 1, 1, 0)

        print('DDS Clock frequency assumed to be:', self.DDS_CLOCK, 'Hz')

        self.waveform_mode = self.DDS_SINE
        self.active_channel = 0
        self.frequency = 1000
        
        # Reset and initialize the chip
        self.write(1<<self.DDS_RESET)
        self.write((1<<self.DDS_B28) | self.waveform_mode)
        
    def write(self, con):
        """Sends a 16-bit control word to the AD9833 via SPI."""
        self.I.SPI.start(self.CS)
        self.I.SPI.send16(con)
        self.I.SPI.stop(self.CS)

    def set_frequency(self, freq, register=0, **args):
        """Calculates and sets the frequency register (FREG0 or FREG1)."""
        self.active_channel = register
        self.frequency = freq
        
        # Frequency Setting Word calculation
        freq_setting = int(round(freq * self.DDS_MAX_FREQ / self.DDS_CLOCK))
        
        modebits = (1<<self.DDS_B28) | self.waveform_mode
        
        # Select FREG0 (0x4000) or FREG1 (0x8000)
        regsel = 0x8000 if register else 0x4000 

        self.write( (1<<self.DDS_RESET) | modebits ) # Ready to load DATA
        
        # Write LSB (bits D0 to D13)
        self.write( (regsel |  (freq_setting & 0x3FFF)) & 0xFFFF )           
        
        # Write MSB (bits D14 to D27)
        self.write( (regsel | ((freq_setting >> 14) & 0x3FFF)) & 0xFFFF )    
        
        # Write Phase Register (P0 or P1). Using 0xc000 for P0
        phase = args.get('phase', 0)
        self.write( 0xc000 | phase)                            
        
        self.write(modebits) # Finished loading data, enable output

    def set_waveform_mode(self, mode):
        """Sets the output waveform (SINE, TRIANGLE, or SQUARE)."""
        self.waveform_mode = mode
        modebits = mode
        # Ensure the correct FSELECT bit is used for the active channel
        if self.active_channel:    
            modebits |= (1<<self.DDS_FSELECT)
        self.write(modebits)


# --- Main Execution Block ---
if __name__ == "__main__":
    try:
        # Connect to ExpEYES-17
        I = eyes17.eyes.open()
        if I is None:
            print("Could not connect to ExpEYES-17 device.")
            sys.exit(1)
            
        # Initialize the AD9833
        A = AD9833(I=I)
        
        print("\n--- AD9833 Waveform and Frequency Generator ---")
        
        # Set an initial state (e.g., 1000 Hz Sine wave)
        A.set_waveform_mode(A.DDS_SINE)
        A.set_frequency(1000, 0)
        print("Initial state: Sine wave at 1000.00 Hz")

        # 2. Interactive Loop
        while True:
            try:
                # Get input from the user: e.g., "s 5000" or "t 100" or "x"
                print("\n--- Waveform Options ---")
                print(" s <freq> : Sine wave at <freq> Hz")
                print(" t <freq> : Triangular wave at <freq> Hz")
                print(" q <freq> : Square wave at <freq> Hz")
                input_str = input(
                    "Enter command (e.g., s 5000) or 'x' to quit: "
                ).strip().lower()
                
                parts = input_str.split()

                if parts and parts[0] == 'x':
                    print("Exiting generator.")
                    break
                    
                if len(parts) != 2:
                    print("Invalid command format. Use: <wave_type> <frequency> (e.g., s 5000)")
                    continue

                wave_type = parts[0]
                new_freq = float(parts[1])
                
                if new_freq <= 0:
                    print("Frequency must be positive.")
                    continue
                
                # Determine the waveform mode
                if wave_type == 's':
                    mode_const = A.DDS_SINE
                    mode_name = "Sine"
                elif wave_type == 't':
                    mode_const = A.DDS_TRIANGLE
                    mode_name = "Triangular"
                elif wave_type == 'q':
                    mode_const = A.DDS_SQUARE
                    mode_name = "Square"
                else:
                    print(f"Unknown waveform type '{wave_type}'. Please use 's', 't', or 'q'.")
                    continue
                    
                # 3. Apply the new waveform and frequency
                A.set_waveform_mode(mode_const)
                A.set_frequency(new_freq, 0) # Set FREG0
                
                # Verify and confirm
                print(f"✅ Output set to {mode_name} wave at {new_freq:.2f} Hz. Check the output signal.")
                
            except ValueError:
                print("Invalid frequency value. Please ensure the frequency is a number.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                # Optional: break out of the loop on unexpected error
                # break 

    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    finally:
        # Clean up or ensure device is reset
        if 'I' in locals() and I:
            # Optionally reset the chip to a safe state on exit
            A.write(1<<A.DDS_RESET)
            print("AD9833 reset upon exit.")
