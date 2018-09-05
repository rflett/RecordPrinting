import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Victorian Collections Record PDF Creation")

    status_frame = tk.Frame(root, padx=10, pady=10)
    status_frame.pack()

    status_message_list = []
    status_message = tk.Text(status_frame, wrap=WORD, height=10, width=60, bd=3)
    status_message.pack()

    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.BOTTOM)

    create_button = tk.Button(button_frame, text='Import CSV', command=csv_import)
    create_button.pack(side=tk.LEFT, padx=5, pady=5)

    create_button = tk.Button(button_frame, text='Create Record', command=create_from_input)
    create_button.pack(side=tk.LEFT, padx=5, pady=5)

    create_range_button = tk.Button(button_frame, text='Create Multiple', command=create_from_range)
    create_range_button.pack(side=tk.LEFT, padx=5, pady=5)


def csv_import():
    pass


def create_from_input():
    pass


def create_from_range():
    pass


if __name__ == "__main__":
    main()