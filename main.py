from csv_module import load_table as load_csv, save_table as save_csv
from pickle_module import load_table as load_pickle, save_table as save_pickle
from table_operations import (
    get_rows_by_number,
    get_rows_by_index,
    get_column_types,
    set_column_types,
    get_values,
    get_value,
    set_values,
    set_value,
    concat,
    split,
    print_table
)

def main():
    data = [
        ["Имя", "Возраст", "Город", "Дата рождения"],
        ["Дмитрий", "25", "Санкт-Петербург", "1999-01-16"],
        ["Мария", "19", "Москва", "2005-05-16"],
        ["Павел", "24", "Новосибирск", "2000-11-08"],
        ["Дарья", "21", "Сочи", "2003-02-28"]
    ]


    save_csv("csv_table", data, 4)
    csv_loaded, column_types1 = load_csv("csv_table_part1.csv", determine_types=True)
    print("Таблица из CSV:")
    print_table(csv_loaded)


    save_pickle("pickle_table.pkl", data, 5)
    pickle_loaded, column_types2 = load_pickle("pickle_table_part1.pkl", determine_types=True)
    print("\n\nТаблица из Pickle:")
    print_table(pickle_loaded)


    print("\n\nСтрока 2 (демонстрация get_rows_by_number):")
    row = get_rows_by_number(csv_loaded, 2)
    print_table(row)
 

    rows = get_rows_by_index(csv_loaded, "Мария", "Дарья")
    print("\n\nСтроки по именам (демонстрация get_rows_by_index):")
    print_table(rows)
    

    print("\n\nТипы данных в столбцах таблицы Pickle (демонстрация get_column_types):")
    print("По индексу:")
    print(get_column_types(pickle_loaded, by_number=True))
    print("По заголовку:")
    print(get_column_types(pickle_loaded, by_number=False))


    print("\n\nПреобразование типов данных по индексу (демонстрация set_column_types):")
    print("\n1)Результат определения типов данных функцией get_column_types:")
    set_column_types(pickle_loaded, {2: bool}, by_number=True)
    print(get_column_types(pickle_loaded))
    print("\n2)Таблица после преобразования:")
    print_table(pickle_loaded)



    print("\n\nПреобразование типов данных по заголовку (демонстрация set_column_types):")
    print("\n1)Результат определения типов данных функцией get_column_types:")
    set_column_types(pickle_loaded, {"Имя": bool}, by_number=False)
    print(get_column_types(pickle_loaded)) 
    print("\n2)Таблица после преобразования:")
    print_table(pickle_loaded)

    save_pickle("pickle_table.pkl", data, 5)
    pickle_loaded = load_pickle("pickle_table_part1.pkl")

    print("\nПолучение значений столбца 'Возраст'(демонстрация get_values):")
    ages = get_values(pickle_loaded, "Возраст", by_row=False)
    print(ages)

    
    print("\n\nДемонстрация функции get_value:")
    single_data = [["Имя", "Возраст", "Город"], ["Иван", "18", "Москва"]]
    save_csv("csv_sngl_data.csv", single_data, max_rows=1)
    csv_sngl_data = load_csv("csv_sngl_data_part1.csv")
    name = get_value([csv_sngl_data[1]], column=0)
    age = get_value([csv_sngl_data[1]], column=1)
    city = get_value([csv_sngl_data[1]], column=2)
    print("Имя:", name)
    print("Возраст:", age)
    print("Город:", city)

    print("\nИзменение возраста (демонстрация set_values):")
    set_values(pickle_loaded, "Возраст", None, ["30", "20", "29", "22"], by_row=False)
    print_table(pickle_loaded)


    print("\nИзменение города для Марии (демонстрация set_value):")
    set_value(pickle_loaded, 2, "Город", "Казань")
    print_table(pickle_loaded)

    #Усложнение №1,2 (Сложность 2)
    print("\n\nПоддержка загрузки таблицы, разбитой на несколько файлов")
    print("csv:")
    save_csv("a", data, 2)
    spltted_csv_loaded = load_csv("a_part1.csv","a_part2.csv")
    print_table(spltted_csv_loaded)
    print("pickle:")
    save_pickle("b.pkl", data, 2)
    spltted_pkl_loaded = load_pickle("b_part1.pkl","b_part2.pkl","b_part3.pkl","b_part4.pkl")
    print_table(spltted_pkl_loaded)

    #Усложнение №3 (Сложность 1)
    print("\n\nСклеенная таблица (демонстрация работы функциии concat):")
    split1_loaded = load_csv("split_table1.csv")
    split2_loaded = load_csv("split_table2.csv")
    connected_table = concat(split1_loaded,split2_loaded)
    print_table(connected_table)

    
    print("\n\nРазделение таблицы на 2 части по строке 3 (демонстрация работы функции split):")
    table_part1, table_part2 = split(csv_loaded, 3)

    print("\nЧасть 1:")
    print_table(table_part1)

    print("\nЧасть 2:")
    print_table(table_part2)

    #Усложнение №4 (Сложность 2 (determine_column_types)) + Усложнение №5 (Сложность 2(datetime))
    print("\n\nДемонстрация определения типа столбцов по хранящимся в таблице значениям (determine_column_types):")
    print(column_types1)
    print(column_types2)


if __name__ == "__main__":
    main()