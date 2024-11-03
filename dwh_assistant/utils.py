import numpy as np
from dwh_assistant.db import execute_sql_query


def build_dbml_schema(table_names):
    """
    Генерирует DBML-схему для указанных таблиц.
    """
    if not table_names:
        return ""

    tables_str = ', '.join(f"'{elem}'" for elem in table_names)
    query = f"""
    SELECT table_name, column_name, data_type
    FROM information_schema.columns
    WHERE table_schema = 'public'
    AND table_name IN ({tables_str})
    ORDER BY table_name, ordinal_position;
    """

    result = execute_sql_query(query)

    if result['error']:
        print(f"Ошибка при создании DBML схемы: {result['error']}")
        return ""

    tables_info = result['result']

    dtypes = {
        'integer': 'int',
        'character varying': 'varchar',
        'timestamp without time zone': 'timestamp',
        'double precision': 'double',
        'text': 'text',
        'boolean': 'bool',
    }

    dbml = ''
    for table_name in np.unique(tables_info['table_name']):
        table = tables_info[tables_info['table_name'] == table_name]
        table_dbml = f'Table {table_name} ' + '{\n'

        for _, row in table.iterrows():
            column_name = row['column_name']
            data_type = dtypes.get(row['data_type'], row['data_type'])
            table_dbml += f'  {column_name} {data_type}\n'

        table_dbml += '}\n'
        dbml += table_dbml
    return dbml
