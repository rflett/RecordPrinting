import tkinter as tk
from tkinter.filedialog import askopenfilename
import record_creation


class MainApplication:

    record_dict = {}

    def __init__(self, parent):
        self.parent = parent

        self.parent.title("Victorian Collections Record PDF Creation")

        self.status_frame = tk.Frame(parent, padx=10, pady=10)
        self.status_frame.pack()

        self.button_frame = tk.Frame(self.parent)
        self.button_frame.pack(side=tk.BOTTOM)

        self.status_message = tk.Text(self.status_frame, wrap=tk.WORD, height=30, width=80, bd=3)
        self.status_message.pack()

        self.create_button = tk.Button(self.button_frame, text='Import CSV', command=self.csv_import)
        self.create_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.create_button = tk.Button(self.button_frame, text='Create Record', command=self.create_from_input)
        self.create_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.create_range_button = tk.Button(self.button_frame, text='Create Multiple', command=self.create_from_range)
        self.create_range_button.pack(side=tk.LEFT, padx=5, pady=5)

    def csv_import(self):
        filename = askopenfilename()
        self.status_message.delete(1.0, tk.END)
        self.status_message.insert(tk.INSERT, "Importing CSV...\n")
        self.parent.update()
        self.record_dict = record_creation.csv_to_dict(filename)
        self.status_message.insert(tk.INSERT, "Done.")

    def create_from_input(self):
        pass

    def create_from_range(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root)
    root.mainloop()
