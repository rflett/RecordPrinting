import tkinter as tk
import csv


def main():
    root = tk.Tk()
    root.title("Victorian Collections Record PDF Creation")

    status_frame = tk.Frame(root, padx=10, pady=10)
    status_frame.pack()

    status_message_list = []
    status_message = tk.Text(status_frame, wrap=tk.WORD, height=10, width=60, bd=3)
    status_message.pack()

    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.BOTTOM)

    create_button = tk.Button(button_frame, text='Import CSV', command=csv_import)
    create_button.pack(side=tk.LEFT, padx=5, pady=5)

    create_button = tk.Button(button_frame, text='Create Record', command=create_from_input)
    create_button.pack(side=tk.LEFT, padx=5, pady=5)

    create_range_button = tk.Button(button_frame, text='Create Multiple', command=create_from_range)
    create_range_button.pack(side=tk.LEFT, padx=5, pady=5)

    root.mainloop()


def csv_import():
    pass


def create_from_input():
    pass


def create_from_range():
    pass


def csv_to_dict(csv_filename: str) -> dict:
    # convert csv file to dictionary for use in creating printable records

    ret_record_dict = {}

    with open(csv_filename) as csv_file:
        reader_obj = csv.reader(csv_file)

        for row in reader_obj:
            record_data = {}
            if reader_obj.line_num == 1:
                headers = row
                continue
            for i in range(len(row)):
                if row[i] == "":
                    continue
                elif i == 13 or i == 18 or i == 18:
                    row[i] = multi_entry_field(row[i])
                record_data[headers[i]] = row[i]
            ret_record_dict[row[6]] = record_data

    return ret_record_dict


def create_html_record(catalogue_number: str) -> str:
    pass


def multi_entry_field(field: str) -> list:
    # split field for readability

    ret_entry_list = []
    entry_list = field.split("|")

    for entry in entry_list:
        attributes = entry.split(";")

        entry_dict = {}
        for attribute in attributes:
            attribute_split = attribute.split(":")

            attribute_split[0]
            attribute_split[1].strip()
            k, v = attribute_split[0].strip(), attribute_split[1].strip()
            if v == "":
                continue
            entry_dict.update({k: v})

        ret_entry_list.append(entry_dict)

    return ret_entry_list


if __name__ == "__main__":
    main()
