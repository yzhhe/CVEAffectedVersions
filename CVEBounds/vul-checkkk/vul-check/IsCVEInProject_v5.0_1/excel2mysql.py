__all__ = ['excel2mysql']

import os
import time
import warnings
import pandas as pd
from tqdm import tqdm
from sqlalchemy import create_engine

DB = 'EXCEL647'
FOLDER = r'D:\北交\漏洞\IsCVEInProject_v5.0'
SQL_CONFIG = {'host': 'localhost',
              'port': 3306,
              'user': 'root',
              'passwd': 'root',
              'database': '',
              'charset': 'utf8'}


def excel2mysql(db: int = DB, folder: str = FOLDER,
                sql_config: dict = None,
                if_count: bool = True, if_warning: bool = False):
    def _url():
        return 'mysql+pymysql://' \
               '{0[user]}:{0[passwd]}' \
               '@{0[host]}:{0[port]}/' \
               '{0[database]}?' \
               'charset={0[charset]}'.format(sql_config)

    if not if_warning:
        warnings.filterwarnings('ignore')

    fail_files = []

    sql_config = sql_config or SQL_CONFIG
    engine = create_engine(_url())
    engine.execute(f'CREATE DATABASE IF NOT EXISTS {db} DEFAULT CHARSET UTF8MB3;')
    sql_config['database'] = db
    engine = create_engine(_url())
    res = dict()
    for path in tqdm((iter, list)[if_count](os.scandir(folder))):
        try:
            # xls_name = path.name.rpartition(".")[0]
            with pd.ExcelFile(path) as xls:
                for sheet_name in xls.sheet_names:
                    sheet = xls.parse(sheet_name)
                    if sheet_name in res:
                        res[sheet_name] = res[sheet_name].append(sheet, ignore_index=True)
                    else:
                        res[sheet_name] = sheet
                    # sheet.to_sql(f'{xls_name}.{sheet_name}', engine,
                    #              if_exists='replace')
        except:
            fail_files.append(path.path)

    for _name, _sheet in res.items():
        _sheet.to_sql(_name, engine,
                      if_exists='replace')

    if fail_files and not time.sleep(0.1):
        print('The following files are failed to import:')
        print('\n'.join(fail_files))
    else:
        print('Done!')


if __name__ == '__main__':
    excel2mysql()
