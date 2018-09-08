import tkinter as tk
from tkinter import simpledialog
from tkinter.filedialog import askopenfilename
import record_creation


class MainApplication:

    record_dict = {}

    def __init__(self, parent):
        self.parent = parent

        self.parent.title("Victorian Collections Record PDF Creation")

        self.status_frame = tk.Frame(parent, padx=10, pady=10)
        self.status_frame.pack()

        self.status_message = tk.Text(self.status_frame, wrap=tk.WORD, height=20, width=60, bd=3)
        self.status_message.pack()

        self.button_frame = tk.Frame(self.parent)
        self.button_frame.pack(side=tk.BOTTOM)

        self.create_button = tk.Button(self.button_frame, text='Import CSV', command=self.csv_import)
        self.create_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.create_button = tk.Button(self.button_frame, text='Create Record', command=self.create_from_input)
        self.create_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.create_range_button = tk.Button(self.button_frame, text='Create Multiple', command=self.create_from_range)
        self.create_range_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.open_folder_button = tk.Button(self.button_frame, text='Open Folder', command=self.open_folder)
        self.open_folder_button.pack(side=tk.LEFT, padx=5, pady=5)

    def csv_import(self):
        filename = askopenfilename()
        self.status_message.delete(1.0, tk.END)

        if not filename.endswith(".csv"):
            self.status_message.insert(tk.INSERT, "Error: Invalid File")
            return

        self.status_message.insert(tk.INSERT, "Importing CSV...\n")
        self.parent.update()
        self.record_dict = record_creation.csv_to_dict(filename)
        self.status_message.insert(tk.INSERT, "Done.")

    def create_from_input(self):
        user_input = simpledialog.askstring("Create Record", "Enter catalogue number", parent=self.parent)
        if user_input is None:
            return
        self.status_message.delete(1.0, tk.END)

        if user_input not in self.record_dict.keys():
            self.status_message.insert(tk.INSERT, f"Error: Record {user_input} does not exist.")
            return

        self.status_message.insert(tk.INSERT, f'Creating record {user_input} ...\n')
        self.parent.update()

        record_html = record_creation.create_html_record(user_input, self.record_dict)
        record_creation.create_pdf_record(user_input, record_html)

        self.status_message.insert(tk.INSERT, 'Record created.')

    def create_from_range(self):
        input_range_start = simpledialog.askstring("Starting Range", "Enter starting catalogue number", parent=self.parent)
        if input_range_start is None:
            return
        input_range_end = simpledialog.askstring("Ending Range", "Enter ending catalogue number", parent=self.parent)
        if input_range_end is None:
            return

        self.status_message.delete(1.0, tk.END)

        if input_range_start not in self.record_dict.keys():
            self.status_message.insert(tk.INSERT, f"Error: Record {input_range_start} does not exist.")
            self.parent.update()
            return
        elif input_range_end not in self.record_dict.keys():
            self.status_message.insert(tk.INSERT, f"Error: Record {input_range_end} does not exist.")
            self.parent.update()
            return

        record_list = list(self.record_dict)
        try:
            record_list_slice = record_list[record_list.index(input_range_start):record_list.index(input_range_end) + 1]
        except ValueError as err:
            self.status_message.insert(tk.INSERT, f"Error: {err}")
            self.parent.update()
            return

        for count, record in enumerate(record_list_slice):
            self.status_message.insert(tk.INSERT, f"Creating record {record}. ({count + 1}/{len(record_list_slice)})\n")
            self.parent.update()
            self.status_message.yview_pickplace(tk.END)
            record_html = record_creation.create_html_record(record, self.record_dict)
            record_creation.create_pdf_record(record, record_html)

        self.status_message.insert(tk.INSERT, "Record creation complete.")

    def open_folder(self):
        record_creation.open_records_folder()


if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root)
    root.mainloop()
