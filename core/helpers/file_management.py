import json
import csv
import os

class READ:

    def json_file(file_path:str) -> dict:
        if os.path.exists(file_path) and file_path.endswith('.json'):
            with open(file_path, 'r') as json_file:
                try:
                    data = json.load(json_file)
                    return data
                except json.JSONDecodeError as e:
                    print(f"Error al decodificar JSON: {e}")
                    return {}
        else:
            print("Archivo no encontrado o el formato no es JSON.")
            return {}

    def txt_file(file_path:str) -> list:
        if os.path.exists(file_path) and file_path.endswith('.txt'):
            with open(file_path, 'r') as txt_file:
                lines = txt_file.read()
                return lines
        else:
            print("Can't open file, not found")
            return []

    def csv_file(file_path:str) -> list:
        if os.path.exists(file_path) and file_path.endswith('.csv'):
            with open(file_path, 'r') as csv_file:
                reader = csv.reader(csv_file)
                data = [row for row in reader]
                return data
        else:
            print("Archivo no encontrado o el formato no es CSV.")
            return []


class SEARCH:

    def file_in_folder(folder_path:str, file_name: str) -> bool:
        try:
            # Check if exist folder and file
            if os.path.exists(folder_path) and os.path.isdir(folder_path):

                # Searching file in folder
                for file in os.listdir(folder_path):
                    if file == file_name:
                        return True
                    
                # If not found file
                return False
            else:
                print(f"Not valid path '{folder_path}'")
                return False
            
        except Exception as e:
            print(f"Error searching file: {e}")
            return False
