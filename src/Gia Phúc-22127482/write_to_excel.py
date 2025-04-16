from xlsxwriter.workbook import Workbook
import json

def write_to_excel(source_filename, worksheet, format, data):
    '''
        Write to excel the processed data
    '''

    # Set up 5 columns
    worksheet.set_column('A:A', 40)
    worksheet.set_column('B:B', 45)
    worksheet.set_column('C:C', 40)
    worksheet.set_column('D:D', 50)

    # Write 5 titles of the 5 columns
    worksheet.write_string(0, 0, 'ID', format)
    worksheet.write_string(0, 1, 'Image_name', format)
    worksheet.write_string(0, 2, 'Image Box', format)
    worksheet.write_string(0, 3, 'SinoNom OCR', format)

    # Write iteratively each line
    line_in_sheet = 0
    for page in data:

        for idx, sentence in enumerate(page['boxes']):
            line_in_sheet += 1

            # Get the necessary information
            id = f'{source_filename}.{page['page']:0{3}}.{idx + 1:0{3}}'
            # img_name = f'{source_filename}_page{page['page']:0{3}}.jpeg'
            img_name = f'{page['page']:0{3}}.jpeg'
            pos = str(sentence['bbox']) if len(sentence['bbox']) > 0 else ""
            transcription = sentence['transcription']

            # Write them to file
            worksheet.write_string(line_in_sheet, 0, id, format)
            worksheet.write_string(line_in_sheet, 1, img_name, format)
            worksheet.write_string(line_in_sheet, 2, pos, format)
            worksheet.write_string(line_in_sheet, 3, transcription, format)

def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


DATA_FILE = "datasets/nom/boxes1.json"
FILENAME = "Don Minh Truoc Chiu Comonhong"


workbook = Workbook(f'boxes1.xlsx')
worksheet = workbook.add_worksheet()
# red = workbook.add_format({'font_name' : 'Nom Na Tong', 'color': '#FF0000'})
# blue = workbook.add_format({'font_name' : 'Nom Na Tong', 'color': '#0000FF'})
format = workbook.add_format({'font_name' : 'Nom Na Tong'})

aligned_data = load_json(DATA_FILE)

write_to_excel(FILENAME, worksheet, format, aligned_data)

workbook.close()