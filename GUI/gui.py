import tkinter
from tkinter import ttk
from data_handler import DataHandler

class ThresholdSelectorApp:
    def __init__(self, root):
        """
        Initialize the Threshold Selector Application.
        """
        self.data_handler = DataHandler()

        root.title("Threshold Selector")
        frame = tkinter.Frame(root)
        frame.pack()

        """Frame for selecting I2C addresses"""
        i2c_addres_frame = tkinter.Frame(frame)
        i2c_addres_frame.grid(row=0, column=0)

        """Label for "AD5673 I2C Address" centered above the column of Comboboxes"""
        tkinter.Label(i2c_addres_frame, text="AD5673 I2C Address", font=("Helvetica", 10, "bold")).grid(row=0, column=1, pady=5)
        self.combobox_A1 = self.create_combobox(i2c_addres_frame, "A1", 1, 0, ["Vcc", "Gnd"])
        self.combobox_A0 = self.create_combobox(i2c_addres_frame, "A0", 1, 2, ["Vcc", "Gnd"])

        tkinter.Label(i2c_addres_frame, text="").grid(row=2, column=1)  # Empty row for spacing

        """Label for "LTC2627 I2C Address" centered above the column of Comboboxes"""
        tkinter.Label(i2c_addres_frame, text="LTC2627 I2C Address", font=("Helvetica", 10, "bold")).grid(row=3, column=1, pady=5)
        self.combobox_C1 = self.create_combobox(i2c_addres_frame, "C1", 4, 0, ["Vcc", "Gnd", "Float"])
        self.combobox_C0 = self.create_combobox(i2c_addres_frame, "C0", 4, 2, ["Vcc", "Gnd", "Float"])
        tkinter.Label(i2c_addres_frame, text="").grid(row=5, pady=5)

        """Configure column weights for alignment in the I2C Address frame"""
        i2c_addres_frame.grid_columnconfigure(0, weight=1)
        i2c_addres_frame.grid_columnconfigure(1, weight=2)  # Center column for labels
        i2c_addres_frame.grid_columnconfigure(2, weight=1)

        """Frame for the title label between Set All Thresholds and I2C Addresses"""
        title_threshold_frame = tkinter.Frame(frame)
        title_threshold_frame.grid(row=1, column=0, columnspan=3)

        """Label for threshold range information"""
        tkinter.Label(title_threshold_frame, text="Threshold Setting [min: -1.25V, Max: +1.25V]", font=("Helvetica", 10, "italic", "bold")).grid(row=0, column=0)

        """Frame for individual threshold entries"""
        threshold_frame = tkinter.Frame(frame)
        threshold_frame.grid(row=2, column=0, pady=20, sticky="w")

        self.threshold_entries = self.create_threshold_entries(threshold_frame)

        """Frame for the "Set All Thresholds" entry"""
        set_all_frame = tkinter.Frame(frame)
        set_all_frame.grid(row=3, column=0, pady=10, sticky="w")
        tkinter.Label(set_all_frame, text="                                  ").grid(row=0, column=0)
        tkinter.Label(set_all_frame, text="Set Thresholds In1 to In14:").grid(row=0, column=1)
        self.set_all_entry = tkinter.Entry(set_all_frame, width=20)
        self.set_all_entry.grid(row=0, column=2, padx=10, pady=10)

        """Frame for the "Apply" and "Reset" buttons"""
        buttons_frame = tkinter.Frame(frame)
        buttons_frame.grid(row=4, column=0, columnspan=2, pady=10)

        """Create the "Apply" button"""
        apply_button = tkinter.Button(buttons_frame, text="Apply", width=20, command=self.apply_changes)
        apply_button.grid(row=0, column=0, padx=10)  # Place "Apply" in the first slot

        """Create the "Reset" button"""
        reset_button = tkinter.Button(buttons_frame, text="Reset", width=20, command=self.reset_values)
        reset_button.grid(row=0, column=1, padx=10)  # Place "Reset" in the second slot

        """Configure column weights for alignment in the buttons frame"""
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)

    def create_combobox(self, parent, label, row, col, values):
      
        tkinter.Label(parent, text=label).grid(row=row, column=col, sticky="e")
        combobox = ttk.Combobox(parent, values=values)
        combobox.grid(row=row, column=col + 1, padx=10)
        return combobox

    def create_threshold_entries(self, parent):
       
        labels = ["In0_A", "In0_B/Trigger", "In1", "In2", "In3", "In4", "In5", "In6", "In7", "In8", "In9", "In10", "In11", "In12", "In13", "In14"]
        entries = {}

        """Define that we want a maximum of 8 items per column"""
        max_items_per_column = 8
        row = 0  # Start from the first row
        col = 0  # Start from the first column

        for i, label in enumerate(labels):
            """Position the labels"""
            tkinter.Label(parent, text=label).grid(row=row, column=col * 2, padx=10, pady=5)  # Alternate column for label
            """Position the entry widgets"""
            entry = tkinter.Entry(parent)
            entry.grid(row=row, column=col * 2 + 1, padx=20, pady=5)
            entries[label] = entry

            row += 1
            """If the number of rows exceeds the limit, move to the next column"""
            if row >= max_items_per_column:
                row = 0  # Return to the first row
                col += 1  # Move to the next column

        return entries

    def apply_changes(self):
        """
        Retrieve the data from the comboboxes and threshold entries,
        and pass it to the data handler.
        """
        addrres = DataHandler.get_i2c_address(self)
        thresholds = DataHandler.get_threshold(self)
        self.data_handler.handle_data(addrres, thresholds)

    def reset_values(self):
        """
        Reset all text boxes (In0_A/Trigger to In14) to zero, excluding the comboboxes,
        and update the data handler with the reset values.
        """
        for label, entry in self.threshold_entries.items():
            entry.delete(0, tkinter.END)
            entry.insert(0, "0")  # Set all entries to zero

        """Reset the "Set All Thresholds" entry to zero"""
        self.set_all_entry.delete(0, tkinter.END)
        self.set_all_entry.insert(0, "0")  # Set "Set All Thresholds" to zero

        """Create the data to pass to the handler, without touching A1, A0, C1, C0"""
        i2c_data = {
            "A1": self.combobox_A1.get(),
            "A0": self.combobox_A0.get(),
            "C1": self.combobox_C1.get(),
            "C0": self.combobox_C0.get(),
        }

        threshold_data = {}
        for label in self.threshold_entries:
            threshold_data[label] = "0"  # Set all thresholds to "0"

        """Update the data through the handler"""
        self.data_handler.handle_data(i2c_data, threshold_data)

if __name__ == "__main__":
    """
    Initialize the main window and run the application.
    """
    window = tkinter.Tk()
    app = ThresholdSelectorApp(window)
    window.mainloop()
