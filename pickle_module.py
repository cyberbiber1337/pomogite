import pickle
from table_operations import determine_column_types

def load_table(*files, determine_types=False):
    data = []
    expected_header = None
    for file_path in files:
        with open(file_path, 'rb') as picklefile:
            table = pickle.load(picklefile)
            if not table:
                raise ValueError(f"Файл {file_path} пустой.")
            header = table[0]
            if expected_header is None:
                expected_header = header
            elif header != expected_header:
                raise ValueError(f"Несоответствие структуры столбцов в файле {file_path}.")
            data.extend(table[1:] if data else table)
    if determine_types:
        column_types = determine_column_types(data)
        return data, column_types

    return data

def save_table(base_file_path, table, max_rows):
    if max_rows < 1:
        raise ValueError("max_rows должен быть больше 0.")
    
    header = table[0]
    rows = table[1:]
    
    file_parts = [
        rows[i:i + max_rows - 1] for i in range(0, len(rows), max_rows - 1)
    ]
    
    for index, part in enumerate(file_parts):
        part_file_path = base_file_path.replace('.pkl', f'_part{index + 1}.pkl')
        with open(part_file_path, 'wb') as picklefile:
            pickle.dump([header] + part, picklefile) 