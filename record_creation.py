import csv


def create_pdf_record(html_record: str):
    pass


def create_html_record(catalogue_number: str) -> str:
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


print_headers = {
        'id': 'ID: ',
        'DateTimeModified': 'Modified: ',
        'DateTimeCreated': 'Created: ',
        'Keywords': 'Keywords: ',
        'Private': 'Private: ',
        'Identification_Name': 'Object Name: ',
        'Identification_RegistrationNumber': 'Catalogue Number: ',
        'Identification_FormalTitle': 'Title: ',
        'Description_PhysicalDescription': 'Physical Description: ',
        'Description_InscriptionsAndMarkings': 'Inscriptions: ',
        'Description_Size': 'Size: ',
        'Description_Materials': 'Materials: ',
        'ManufactureDetails_DateMade': 'Date Made: ',
        'ManufactoreDetails_Makers': 'Makers: ',
        'ManufactureDetails_PlaceMade': 'Place Made: ',
        'ManufactureDetails_PlaceMade_Comments': 'Manufacture Comments: ',
        'Context_HistoricalInformation': 'Historical Information: ',
        'Context_HistoricalStatementOfSignificance': 'Statement Of Significance: ',
        'UsageDetails': 'Usage: ',
        'AcquisitionDetails_HowAcquired': 'Acquired By: ',
        'AcquisitionDetails_DateAcquired': 'Date Acquired: ',
        'AcquisitionDetails_Source_Name': 'Acquired From: ',
        'AcquisitionDetails_Source_Address': 'Address: ',
        'AcquisitionDetails_Source_Phone': 'Phone: ',
        'AcquisitionDetails_Source_Email': 'Email: ',
        'AcquisitionDetails_Acknowledgement': 'Acknowledgement: ',
        'AcquisitionDetails_AcknowledgementDate': 'Acknowledgement Date: ',
        'AcquisitionDetails_Comments': 'Acquisition Comments: ',
        'ConditionReports': 'Condition Reports: ',
        'Storage_RegularLocation': 'Regular Location: ',
        'Storage_CurrentLocation_Location': 'Current Location: ',
        'Storage_CurrentLocation_DateMoved': 'Date Moved: ',
        'Storage_CurrentLocation_TimeMoved': 'Time Moved: ',
        'Storage_CurrentLocation_MovedBy': 'Moved By: ',
        'ValuationReports': 'Valuation Reports: ',
        'Rights_CopyrightPermissions': 'Copyright Permissions: ',
        'Rights_CopyrightAcknowledgement': 'Copyright Acknowledgement: ',
        'Rights_CopyrightResearch': 'Copyright Research: ',
        'Rights_CopyrightKnown': 'Copyright Known: ',
        'Rights_CopyrightCategory': 'Copyright Category: ',
        'Rights_CopyrightExpiry': 'Copyright Expiry: ',
        'Rights_CopyrightHolder_Name': 'Copyright Holder Name: ',
        'Rights_CopyrightHolder_Address': 'Address: ',
        'Rights_CopyrightHolder_Phone': 'Phone: ',
        'Rights_CopyrightHolder_Email': 'Email: ',
        'SupplementaryFile_HasSupplementaryFile': 'Supplementary File: ',
        'SupplementaryFile_SupplementaryFileLocation': 'Supplementary File Location: '}

print_order = [
    'Identification_RegistrationNumber', 'Identification_Name', 'Identification_FormalTitle',
    'Storage_RegularLocation', 'Storage_CurrentLocation_Location', 'Description_PhysicalDescription',
    'Description_InscriptionsAndMarkings', 'Description_Size', 'Description_Materials',
    'ManufactureDetails_DateMade', 'ManufactureDetails_PlaceMade', 'ManufactureDetails_PlaceMade_Comments',
    'ManufactoreDetails_Makers', 'Context_HistoricalInformation', 'Context_HistoricalStatementOfSignificance',
    'Keywords', 'UsageDetails', 'AcquisitionDetails_HowAcquired', 'AcquisitionDetails_DateAcquired',
    'AcquisitionDetails_Source_Name', 'AcquisitionDetails_Source_Address', 'AcquisitionDetails_Source_Phone',
    'AcquisitionDetails_Source_Email', 'AcquisitionDetails_AcknowledgementDate',
    'AcquisitionDetails_Comments', 'ConditionReports']