import os
import csv
import pdfkit
from jinja2 import FileSystemLoader, Environment
from print_data import print_order, print_headers


def create_pdf_record(catalogue_number: str, html_record: str):
    if not os.path.exists(os.path.join(".", "records")):
        os.mkdir(os.path.join(".", "records"))
    pdfkit.from_string(html_record, os.path.join(".", "records", f"{catalogue_number}.pdf"))


def create_html_record(catalogue_number: str, record_dictionary: dict) -> str:

    ret_record = ""
    record = []

    # use print order list to order how fields are displayed
    for title in print_order:
        entry = {}

        try:
            entry['header'] = print_headers[title]

            if type(record_dictionary[catalogue_number][title]) == list:
                entry['data'] = multi_entry_field_html_format(record_dictionary[catalogue_number][title])
            else:
                entry['data'] = record_dictionary[catalogue_number][title]
            record.append(entry)
        except KeyError:
            pass

    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('record_template.html')

    ret_record = template.render(record=record)
    return ret_record


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
                elif i == 13 or i == 18 or i == 28:
                    row[i] = multi_entry_field(row[i])
                record_data[headers[i]] = row[i]
            ret_record_dict[row[6]] = record_data

    return ret_record_dict


def multi_entry_field(field: str) -> list:
    # split field for readability

    ret_entry_list = []
    entry_list = field.split("|")

    for entry in entry_list:
        attributes = entry.split(";")

        entry_dict = {}
        for attribute in attributes:
            attribute_split = attribute.split(":")

            if attribute_split[1] == " " or attribute_split[1] == "":
                continue

            k, v = attribute_split[0].strip(), attribute_split[1].strip()
            entry_dict[k] = [v][0]

        ret_entry_list.append(entry_dict)

    return ret_entry_list


def multi_entry_field_html_format(entry_list: list) -> str:
    # format multi entry field for html display
    ret_field = ""

    field_list = []
    for entry in entry_list:
        attribute_list = []
        for k, v in entry.items():
            attribute = f"{k}: {v}"
            attribute_list.append(attribute)
        entry_string = " ; ".join(attribute_list)
        field_list.append(entry_string)

    ret_field = "<br>".join(field_list)
    return ret_field


def open_records_folder():
    os.system(f"explorer {os.path.abspath(os.path.join('.', 'records'))}")
