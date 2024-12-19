import copy
from tabulate import tabulate
import datetime

def get_rows_by_number(table, start, stop=None, copy_table=False):
    try:
        if stop is None:
            rows = [table[start]]
        else:
            rows = table[start:stop]
        if copy_table:
            rows = copy.deepcopy(rows)
        return rows
    except IndexError:
        raise IndexError(f"Указанный диапазон строк ({start}, {stop}) выходит за пределы таблицы.")

def get_rows_by_index(table, *values, copy_table=False):
    rows = []
    try:
        for row in table:
            if row[0] in values:
                rows.append(row)
        if not rows:
            raise ValueError(f"Значения {values} не найдены в таблице.")
        if copy_table:
            rows = copy.deepcopy(rows)
        return rows
    except Exception as e:
        raise ValueError(f"Ошибка при получении строк по индексам: {e}")

def convert_list_to_dict(table_list):
    if not table_list or len(table_list) < 2:
        raise ValueError("Таблица должна содержать заголовки и хотя бы одну строку данных.")
    headers = table_list[0]
    data = table_list[1:]
    types = {i: type(data[0][i]) for i in range(len(headers))}
    return {'headers': headers, 'data': data, 'types': types}

def get_column_types(table, by_number=True):
    if isinstance(table, list):
        table = convert_list_to_dict(table)

    column_types = {}
    headers = table['headers']
    types = table['types']

    if by_number:
        for col_index, col_type in types.items():
            column_types[col_index] = col_type.__name__
    else:
        for col_index, col_type in types.items():
            column_types[headers[col_index]] = col_type.__name__

    return column_types

def set_column_types(table, types_dict, by_number=True):
    if not table or len(table) < 2:
        raise ValueError("Таблица должна содержать заголовки и данные.")

    if not by_number:
        headers = table[0]
        try:
            types_dict = {headers.index(key): value for key, value in types_dict.items()}
        except ValueError as e:
            raise ValueError(f"Ошибка в указании заголовков: {e}")

    for row in table[1:]:
        for col, col_type in types_dict.items():
            try:
                row[col] = col_type(row[col])
            except ValueError:
                raise ValueError(f"Не удалось преобразовать значение '{row[col]}' в {col_type}.")
            except IndexError:
                raise IndexError(f"Индекс {col} выходит за пределы таблицы.")

    return table

def get_values(table, col_or_row=None, index=None, by_row=True):
    if not table or len(table) < 2:
        raise ValueError("Таблица должна содержать заголовки и данные.")
    
    headers = table[0]

    if not by_row:
        if col_or_row is None:
            raise ValueError("Не указано имя столбца или его индекс.")
        
        try:
            col_index = col_or_row if isinstance(col_or_row, int) else headers.index(col_or_row)
            return [row[col_index] for row in table[1:]]
        except ValueError:
            raise ValueError(f"Заголовок '{col_or_row}' не найден в таблице.")
        except IndexError:
            raise IndexError(f"Индекс столбца {col_or_row} выходит за пределы таблицы.")
    
    if by_row:
        if index is None:
            raise ValueError("Индекс строки должен быть указан, если by_row=True.")
        
        try:
            return table[index]
        except IndexError:
            raise IndexError(f"Индекс строки {index} выходит за пределы таблицы.")


def get_value(table, column=0):
    if len(table) != 1:
        raise ValueError("Функция предназначена только для таблиц с одной строкой.")
    return table[0][column]


def set_values(table, col_or_row, index, values, by_row=True):
    headers = table[0]
    try:
        if not by_row: 
            col_index = col_or_row if isinstance(col_or_row, int) else headers.index(col_or_row)
            
            if len(values) != len(table) - 1:
                raise ValueError("Количество значений не совпадает с количеством строк таблицы.")
            
            for i, value in enumerate(values):
                table[i + 1][col_index] = value
        
        else:
            if index is None or index >= len(table):
                raise IndexError(f"Индекс строки {index} выходит за пределы таблицы.")
            table[index] = values
            
    except ValueError as e:
        raise ValueError(f"Ошибка в данных: {e}")
    except IndexError as e:
        raise IndexError(f"Ошибка в индексах: {e}")


def set_value(table, row_index, col_or_header, value):
    if not table or len(table) < 2:
        raise ValueError("Таблица должна содержать заголовки и данные.")
    headers = table[0]
    try:
        col_index = col_or_header if isinstance(col_or_header, int) else headers.index(col_or_header)
        if row_index >= len(table):
            raise IndexError(f"Индекс строки {row_index} выходит за пределы таблицы.")
        table[row_index][col_index] = value
    except ValueError:
        raise ValueError(f"Заголовок '{col_or_header}' не найден.")
    except IndexError as e:
        raise IndexError(f"Ошибка в индексах: {e}")

def print_table(table):
    if not table:
        raise ValueError("Таблица пуста, нечего отображать.")
    print(tabulate(table, headers="firstrow", tablefmt="grid"))

def concat(table1, table2):
    conn_table = table1 + table2[1:]
    return conn_table

def split(table, row_number):
    splitted_table1 = table[:row_number + 1]
    splitted_table2 = [table[0]] + table[row_number + 1:]
    return splitted_table1, splitted_table2

def determine_column_types(table):
    if not table or len(table) < 2:
        raise ValueError("Таблица должна содержать заголовки и хотя бы одну строку данных.")

    headers, rows = table[0], table[1:]
    column_types = []

    for col_index in range(len(headers)):
        column_values = [row[col_index] for row in rows if len(row) > col_index and row[col_index] != '']
        column_type = str 

        if all(v.isdigit() for v in column_values if isinstance(v, str)):
            column_type = int

        elif all(is_float(v) for v in column_values):
            column_type = float

        elif all(is_date(v) for v in column_values):
            column_type = datetime.datetime

        column_types.append(column_type)

    return column_types

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
    
def is_date(value):
    try:
        datetime.datetime.strptime(value, "%Y-%m-%d")
        return True
    except ValueError:
        return False