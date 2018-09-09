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

    ret_record_dict = {"success": False}

    with open(csv_filename) as csv_file:
        reader_obj = csv.reader(csv_file)

        for row in reader_obj:
            record_data = {}

            if reader_obj.line_num == 1:
                headers = row

                for header in headers:
                    if header not in csv_headers:
                        ret_record_dict["error"] = f"Unexpected header in csv: {header}"
                        return ret_record_dict

                continue

            for i in range(len(row)):
                if row[i] == "":
                    continue

                elif headers[i] == 'ManufactoreDetails_Makers':
                    row[i] = multi_entry_field(row[i], maker_multi_entry_headers)
                elif headers[i] == 'UsageDetails':
                    row[i] = multi_entry_field(row[i], usage_multi_entry_headers)
                elif headers[i] == 'ConditionReports':
                    row[i] = multi_entry_field(row[i], condition_multi_entry_headers)
                elif headers[i] == 'ValuationReports':
                    row[i] = multi_entry_field(row[i], valuation_multi_entry_headers)

                record_data[headers[i]] = row[i]
            ret_record_dict[row[6]] = record_data

    ret_record_dict["success"] = True
    return ret_record_dict


def multi_entry_field(field: str, header_list: list) -> list:
    # split field for readability

    ret_entry_list = []
    entry_list = field.split("|")

    for entry in entry_list:
        attributes = entry.split(";")

        entry_dict = {}
        for attribute in attributes:
            attribute_split = [x.strip() for x in attribute.split(":")]

            if len(attribute_split[1]) == 0:
                continue

            k, v = attribute_split[0], attribute_split[1]
            entry_dict[k] = [v][0]

        ret_entry_list.append(entry_dict)

    return ret_entry_list


def multi_entry_field_html_format(entry_list: list) -> str:
    # format multi entry field for html display
    ret_field = ""

    field_list = []
    for entry in entry_list:
        attribute_list = [f"{k}: {v}" for k, v in entry.items()]
        entry_string = " ; ".join(attribute_list)
        field_list.append(entry_string)

    ret_field = "<br>".join(field_list)
    return ret_field


def open_records_folder() -> None:
    os.system(f"explorer {os.path.abspath(os.path.join('.', 'records'))}")


maker_multi_entry_headers = ['Name', 'Contact_Name', 'Contact_Address',
                             'Contact_Phone', 'Contact_Email', 'Role']

usage_multi_entry_headers = ['Used By', 'Date Used', 'Usage Comments', 'Place Used']

condition_multi_entry_headers = ['Condition', 'DateChecked', 'CheckedBy_Name', 'CheckedBy_Address',
                                 'CheckedBy_Phone', 'CheckedBy_Email', 'Comments']

valuation_multi_entry_headers = ['ValuationAmount', 'DateValued', 'CheckedBy_Name', 'CheckedBy_Address',
                                 'CheckedBy_Phone', 'CheckedBy_Email', 'Comments']

csv_headers = [
    'id',
    'DateTimeModified',
    'DateTimeCreated',
    'Keywords',
    'Private',
    'Identification_Name',
    'Identification_RegistrationNumber',
    'Identification_FormalTitle',
    'Description_PhysicalDescription',
    'Description_InscriptionsAndMarkings',
    'Description_Size',
    'Description_Materials',
    'ManufactureDetails_DateMade',
    'ManufactoreDetails_Makers',
    'ManufactureDetails_PlaceMade',
    'ManufactureDetails_PlaceMade_Comments',
    'Context_HistoricalInformation',
    'Context_HistoricalStatementOfSignificance',
    'UsageDetails',
    'AcquisitionDetails_HowAcquired',
    'AcquisitionDetails_DateAcquired',
    'AcquisitionDetails_Source_Name',
    'AcquisitionDetails_Source_Address',
    'AcquisitionDetails_Source_Phone',
    'AcquisitionDetails_Source_Email',
    'AcquisitionDetails_Acknowledgement',
    'AcquisitionDetails_AcknowledgementDate',
    'AcquisitionDetails_Comments',
    'ConditionReports',
    'Storage_RegularLocation',
    'Storage_CurrentLocation_Location',
    'Storage_CurrentLocation_DateMoved',
    'Storage_CurrentLocation_TimeMoved',
    'Storage_CurrentLocation_MovedBy',
    'ValuationReports',
    'Rights_CopyrightPermissions',
    'Rights_CopyrightAcknowledgement',
    'Rights_CopyrightResearch',
    'Rights_CopyrightKnown',
    'Rights_CopyrightCategory',
    'Rights_CopyrightExpiry',
    'Rights_CopyrightHolder_Name',
    'Rights_CopyrightHolder_Address',
    'Rights_CopyrightHolder_Phone',
    'Rights_CopyrightHolder_Email',
    'SupplementaryFile_HasSupplementaryFile',
    'SupplementaryFile_SupplementaryFileLocation']
