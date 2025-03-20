# picoCMP Guide

To interface with the picoCMP, two folders are provided:

- `i2c_communication` folder: Contains the sketch to be uploaded to Arduino.
- `GUI` folder: Contains the graphical interface for setting the comparator thresholds.

## Setup Instructions

1. Upload the sketch from the `i2c_communication` folder to the Arduino.
2. After uploading, place a capacitor between the Reset and GND pins to prevent the Arduino from auto-resetting during communication.
3. Power the picoCMP and connect the Arduino to the board and the PC.
4. Once the connections are set up, open **Visual Studio Code** and navigate to the `GUI` folder, then run the `gui.py` file. This will launch the graphical interface.

## Using the GUI

1. Use the drop-down menus to select the I2C addresses of the DACs on the board.
2. Check where the A0, A1, C0, and C1 pins have been soldered and set their values in the interface accordingly.
3. Enter the desired threshold values in volts for each input.
   - If you set a value in the "Set Threshold In1 to In14" field, all input thresholds from In1 to In14 will be set to the same value.
   - The In0_A and In0_B/Trigger thresholds will remain unchanged and must be modified in their respective text boxes.
4. Click **"Apply"** to confirm and apply the changes.
5. To reset all thresholds to zero, click the **"Reset"** button.
