import json
import csv

# Función para leer el archivo JSON que contenga la Carta Porte v3.1 a evaluar.
def read_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:      # Lectura del JSON en codificación para mostrar los acentos 
            data = json.load(file)
            # print(f"Data read from file: {data}")                 # Muestra contenido de todo el archivo
            if isinstance(data, dict):
                return data
            else:
                print("El archivo no contiene una estructura de JSON válida.")
                return None
    except json.JSONDecodeError as e:
        print(f"Error al decodificar el JSON: {e}")                      # En caso de JSON inválido
        return None
    except Exception as e:
        print(f"Error encontrado: {e}")
        return None

# Funcion para leer el catálogo de Productos y servicios del SAT para carta porte. Regresa el código de "MaterialPeligroso" 
def search_CP_code(code_to_search):								
	with open(catalog_data, encoding='utf-8') as csvfile:
		contents = csv.reader(csvfile, delimiter=',', quotechar='"')
		for row in contents:
			if row[0] == code_to_search:
				return row[3]

# Función para iterar sobre los productos en el JSON
def iterate_products(json_data):
	try:
		complemento = json_data.get('Complemento', {})            # Desecha el resto del JSON y obtiene solo lo contenido en Mercancias > Mercancia
		carta_porte = complemento.get('CartaPorte31', {})
		mercancias = carta_porte.get('Mercancias', {})
		productos = mercancias.get('Mercancia', [])

		for index,producto in enumerate(productos):               # Recorre todas las mercancías incluidas en el JSON, mostrando los valores referentes al material peligroso
			clave_material_peligroso = search_CP_code(producto.get('BienesTransp'))		# Busca la clave indicada en "BienesTransp" en los catálogos del SAT
			
			# Si la clave es "1" el JSON debe tener "Sí" en campo "MaterialPeligroso"
			if clave_material_peligroso == "1":			
				if producto.get('MaterialPeligroso') == "Sí":
					print(f'• Mercancia[{index}] ✅ .')
				else:
					print(f'• Mercancia[{index}] ❌ : Para "BienesTransp":"{producto.get("BienesTransp")}", el campo "MaterialPeligroso" debe estar indicado y ser "Sí" según lo indicado en los catálogos del SAT ({clave_material_peligroso})')	

			# Si la clave es "0" el JSON no debe tener el campo "MaterialPeligroso"
			if clave_material_peligroso == "0":			
				if producto.get('MaterialPeligroso'):
					print(f'• Mercancia[{index}] ❌ : Para "BienesTransp":"{producto.get("BienesTransp")}", el campo "MaterialPeligroso" no debe ser incluido según lo indicado en los catálogos del SAT ({clave_material_peligroso})')		
				else:
					print(f'• Mercancia[{index}] ✅ .')
					
			# Si la clave es "0,1" el JSON debe tener "Sí" o "No" en campo "MaterialPeligroso"
			elif clave_material_peligroso == "0,1":		
				if producto.get('MaterialPeligroso') == "Sí" or producto.get('MaterialPeligroso') == "No":
					print(f'• Mercancia[{index}] ✅ .')
				else:
					print(f'• Mercancia[{index}] ❌ : Para "BienesTransp":"{producto.get("BienesTransp")}", el campo "MaterialPeligroso" debe ser incluido según lo indicado en los catálogos del SAT ({clave_material_peligroso})')

			elif clave_material_peligroso == None:								
				print(f'• Mercancia[{index}] ❌  "BienesTransp":"{producto.get("BienesTransp")}" no encontrado en los catalogos de productos y servicios de Carta Porte v3.1')

	except KeyError as e:
		print(f"Key not found: {e}")
	except TypeError as e:
		print(f"Type error: {e}")


# Programa
file_path = 'CartaPorte.json'  			# Ruta del archivo JSON de la Carta Porte v3.1
catalog_data = 'c_ClaveProdServCP.csv'	# Ruta del catálogo de Productos & Servicios de Carta Porte v3.1

json_data = read_json(file_path)   
iterate_products(json_data) if json_data else print("Error al crear objeto a partir de archivo JSON.")
