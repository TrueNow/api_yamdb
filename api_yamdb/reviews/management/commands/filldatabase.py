import csv
import os
import sqlite3

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    @staticmethod
    def filter_files(path, endswith):
        result = []
        for root, _, files in os.walk(path):
            for name in files:
                if name.endswith(endswith):
                    result.append(os.path.join(root, name))
        return result

    def handle(self, *args, **options):
        DB_FOLDER = os.getcwd()
        DB_NAME = 'db.sqlite3'
        APP_NAME = 'reviews'

        CSV_FOLDER = os.path.join(DB_FOLDER, 'static', 'data')
        DB_FILE = os.path.join(DB_FOLDER, DB_NAME)

        csv_files = self.filter_files(CSV_FOLDER, endswith='.csv')

        con = sqlite3.connect(DB_FILE)
        cur = con.cursor()

        for csv_file in csv_files:
            with open(csv_file, 'r', encoding='utf-8') as f:
                dr = csv.DictReader(f)

                TABLE_NAME, _ = os.path.basename(csv_file).split('.')
                fieldnames_string = ', '.join(dr.fieldnames)
                questions_string = ', '.join(
                    ['?'] * len(dr.fieldnames)
                )
                data = [tuple(row.values()) for row in dr]

                try:
                    cur.executemany(
                        f"INSERT INTO {APP_NAME}_{TABLE_NAME}({fieldnames_string}) VALUES ({questions_string});",
                        data
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Таблица {APP_NAME}_{TABLE_NAME} успешно заполнена!'
                        )
                    )
                except sqlite3.IntegrityError as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Таблица {APP_NAME}_{TABLE_NAME} уже заполнена!'
                        )
                    )
                except sqlite3.OperationalError:
                    cur.execute(
                        f"CREATE TABLE {APP_NAME}_{TABLE_NAME}({fieldnames_string})"
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Таблица {APP_NAME}_{TABLE_NAME} создана.'
                        )
                    )
                con.commit()
        con.close()
