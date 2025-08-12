import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from repairs.models import Repairs
from equipment.models import EquipmentPos, LegalEntity, Shop

class Command(BaseCommand):
    help = "Import repairs data from a CSV file into the Repairs table"

    def handle(self, *args, **kwargs):
        # Delete all existing Repairs records
        Repairs.objects.all().delete()
        self.stdout.write("All existing Repairs records deleted.")

        csv_file_path = '/Users/alex_d/Dev/equipment_base/data/csv_4_DB_processed.csv'
        legal_entity_name = 'ООО "Русфорест Магистральный"'  # Legal entity is the same for all rows

        try:
            # Fetch the LegalEntity object
            legal_entity = LegalEntity.objects.filter(name=legal_entity_name).first()
            if not legal_entity:
                self.stdout.write(f"LegalEntity '{legal_entity_name}' not found. Aborting.")
                return

            with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Format 'pos' to XXXX format
                    formatted_pos = row['pos'].zfill(4)

                    # Fetch Shop for this legal entity
                    shop_name = row.get('shop')
                    if not shop_name:
                        self.stdout.write(f"Skipping row due to missing shop: {row}")
                        continue

                    shop = Shop.objects.filter(name=shop_name, department__legal_entity=legal_entity).first()
                    if not shop:
                        self.stdout.write(f"Skipping row due to missing Shop: {row}")
                        continue

                    # Fetch EquipmentPos object based on formatted 'pos' and shop
                    equipment_pos = EquipmentPos.objects.filter(pos=formatted_pos, shop=shop).first()
                    if not equipment_pos:
                        self.stdout.write(f"Skipping row due to missing EquipmentPos: {row}")
                        continue

                    # Create Repairs object
                    try:
                        Repairs.objects.create(
                            equipment_pos=equipment_pos,
                            legal_entity=legal_entity,
                            start=datetime.strptime(row['start'], '%Y-%m-%d %H:%M:%S'),
                            end=datetime.strptime(row['end'], '%Y-%m-%d %H:%M:%S'),
                            reason=row['reason'] if row['reason'] else None,
                            job=row['job'] if row['job'] else None,
                            duration=float(row['duration']),
                            note=row['note'] if row['note'] else None
                        )
                        self.stdout.write(f"Successfully imported repair for EquipmentPos {formatted_pos} in shop {shop_name}")
                    except Exception as e:
                        self.stdout.write(f"Error importing row: {row} | Error: {e}")

        except FileNotFoundError:
            self.stdout.write(f"File not found: {csv_file_path}")
        except Exception as e:
            self.stdout.write(f"An error occurred: {e}")