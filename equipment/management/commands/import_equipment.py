import pandas as pd
from django.core.management.base import BaseCommand
from equipment.models import LegalEntity, Department, Shop, EquipClass, EquipSubClass, EquipmentPos, EquipmentName

class Command(BaseCommand):
    """
    Команда для импорта данных об оборудовании из XLSX-файла.
    Для каждой строки файла создаются или обновляются связанные объекты:
    юридическое лицо, подразделение, производственный участок, класс, подкласс, наименование оборудования и позиция.
    Если оборудование уже существует, его класс и подкласс обновляются при необходимости.
    """

    help = "Импортировать данные об оборудовании из XLSX"

    def add_arguments(self, parser):
        # Добавляет аргумент для пути к XLSX-файлу
        parser.add_argument('xlsx_path', type=str, help='Путь к XLSX-файлу')

    def handle(self, *args, **options):
        # Чтение XLSX-файла и заполнение пустых значений
        xlsx_path = options['xlsx_path']
        df = pd.read_excel(xlsx_path, sheet_name='Структура ОС')
        df = df.fillna('')

        # Обработка каждой строки файла
        for _, row in df.iterrows():
            # Пропуск строк без наименования оборудования
            if not row['Наименование оборудования']:
                continue

            # Получение или создание юридического лица
            legal_entity, _ = LegalEntity.objects.get_or_create(
                name=row['Юридическое лицо']
            )

            # Получение или создание подразделения (может быть пустым)
            department = None
            if row['Подразделение']:
                department, _ = Department.objects.get_or_create(
                    name=row['Подразделение'],
                    legal_entity=legal_entity
                )

            # Получение или создание производственного участка
            shop, _ = Shop.objects.get_or_create(
                name=row['Производственный участок'],
                department=department if department else None
            )

            # Получение или создание класса оборудования
            equip_class, _ = EquipClass.objects.get_or_create(
                name=row['Класс']
            )

            # Получение или создание подкласса оборудования
            equip_subclass = None
            if row['Подкласс']:
                equip_subclass, _ = EquipSubClass.objects.get_or_create(
                    name=row['Подкласс'],
                    equip_class=equip_class
                )

            # Получение или создание наименования оборудования, установка класса и подкласса
            equipment_name, created = EquipmentName.objects.get_or_create(
                name=row['Наименование оборудования'],
                defaults={
                    'equip_class': equip_class,
                    'equip_subclass': equip_subclass
                }
            )
            # Если оборудование уже существует, обновить класс/подкласс при необходимости
            if not created:
                updated = False
                if equipment_name.equip_class != equip_class:
                    equipment_name.equip_class = equip_class
                    updated = True
                if equipment_name.equip_subclass != equip_subclass:
                    equipment_name.equip_subclass = equip_subclass
                    updated = True
                if updated:
                    equipment_name.save()

            # Получение или создание позиции оборудования с привязкой ко всем FK
            EquipmentPos.objects.get_or_create(
                pos=row['Номер позиции'] if row['Номер позиции'] else '',
                shop=shop,
                department=department,
                legal_entity=legal_entity,
                equipment_name=equipment_name
            )

        # Вывод сообщения об успешном завершении импорта
        self.stdout.write(self.style.SUCCESS('Импорт завершён!'))