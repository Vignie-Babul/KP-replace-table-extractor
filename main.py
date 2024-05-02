import camelot

import copy
import json


# [row][column]
# print(table.cells[0][1].text)


def save_data(data) -> None:
	with open('data.json', 'w', encoding='utf-8') as file:
		json.dump(data, file, indent=4, ensure_ascii=False)


def get_value(row: int, column: int, table) -> str:
	cell_value = table.cells[row][column].text
	cell_value_clear = cell_value.replace('\n', '')
	cell_value_result = cell_value_clear

	if cell_value_clear.startswith(' '):
		cell_value_result = cell_value_result[1:]
	if cell_value_clear.endswith(' '):
		cell_value_result = cell_value_result[:-1]

	return cell_value_result


def get_data_from_table(row: int, table) -> dict:
	data = {
		'lesson_replacement_number': 0,
		'group': get_value(row=row, column=1, table=table),
		'changing_lesson': {
			'number': get_value(row=row, column=2, table=table),
			'subject': get_value(row=row, column=3, table=table),
			'teacher': get_value(row=row, column=4, table=table),
			'classroom': get_value(row=row, column=5, table=table),
		},
		'replacement_lesson': {
			'number': get_value(row=row, column=6, table=table),
			'subject': get_value(row=row, column=7, table=table),
			'teacher': get_value(row=row, column=8, table=table),
			'classroom': get_value(row=row, column=9, table=table),
		}
	}

	return data


tables = camelot.read_pdf('file.pdf')
table = tables[0]

group_number = len(table.cells) - 4

replacements_data = {}

for row in range(2, group_number + 2):
	lesson_number = str(row - 1)
	data = get_data_from_table(row=row, table=table)
	data['lesson_replacement_number'] = lesson_number
	replacements_data[lesson_number] = data


for data_number in replacements_data.keys():
	if replacements_data[data_number]['group'] == '':
		replacements_data[data_number]['group'] = replacements_data[str(int(data_number) - 1)]['group']


for data_number in replacements_data.keys():
	numbers = replacements_data[data_number]['changing_lesson']['number'].split(', ')
	if len(numbers) > 1:
		changing_lesson_subjects = (
			replacements_data[data_number]['changing_lesson']['subject'].split(', ')
		)
		replacement_lesson_subjects = (
			replacements_data[data_number]['replacement_lesson']['subject'].split(', ')
		)

		subjects_list = [changing_lesson_subjects, replacement_lesson_subjects]
		new_subjects_list = []
		for subjects in subjects_list:
			if len(subjects) == 1:
				new_subjects_list.append(subjects + subjects)
			else:
				new_subjects_list.append(subjects)


		data_copy = copy.deepcopy(replacements_data)
		data_copy_new = copy.deepcopy(replacements_data[data_number])


		data_copy[data_number]['changing_lesson']['number'] = numbers[0]
		data_copy[data_number]['replacement_lesson']['number'] = numbers[0]

		data_copy[data_number]['changing_lesson']['subject'] = new_subjects_list[0][0]		
		data_copy[data_number]['replacement_lesson']['subject'] = new_subjects_list[1][0]


		data_copy_new['changing_lesson']['number'] = numbers[1]
		data_copy_new['replacement_lesson']['number'] = numbers[1]

		data_copy_new['changing_lesson']['subject'] = new_subjects_list[0][1]
		data_copy_new['replacement_lesson']['subject'] = new_subjects_list[1][1]

		data_copy[str(int(data_number) + 1)] = data_copy_new


replacements_data = data_copy


save_data(data=replacements_data)
