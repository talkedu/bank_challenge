from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import sys
import json


def download_from_folder(drive, folder_id):
    file_list = drive.ListFile({'q': "'%s' in parents and trashed=false" % folder_id}).GetList()
    file_map = {}
    for file1 in file_list:
        file_map[file1['title']] = file1.GetContentString()
    return file_map


def main(bank_folder_id, credit_report_folder_id):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    bank_input_map = download_from_folder(drive, bank_folder_id)
    bank_proccesed_map = process_from_raw_data(bank_input_map)
    save_files_from_processed_data(bank_proccesed_map)

    credit_report_input_map = download_from_folder(drive, credit_report_folder_id)


def save_files_from_processed_data(processed_map):
    for title, flattened_dict in processed_map.iteritems():
        print 'a'


def process_from_raw_data(input_map):
    processed_map = {}
    for title, json_string in input_map.iteritems():
        json_dict = json.loads(json_string)
        flattened_dict = flatten_dict(json_dict)
        flattend_json_string = json.dumps(flattened_dict)
        processed_map[title] = convert_json_string_to_csv(flattend_json_string)
    return processed_map


def convert_json_string_to_csv(json_string):
    return json_string


def flatten_dict(json_dict):
    val = {}
    for i in json_dict.keys():
        if isinstance(json_dict[i], dict):
            get = flatten_dict(json_dict[i])
            for j in get.keys():
                val[i + '-' + j] = get[j]
        elif isinstance(json_dict[i], list):
            print('nada')
        else:
            val[i] = json_dict[i]
    return val

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
