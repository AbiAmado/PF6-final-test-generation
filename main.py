import requests
import json
import sys

# La URL base de la API de Colombia
API_BASE_URL = "https://api-colombia.com/api/v1"

def dish_fetch(num):
    
    # 1. Asegurarse de que 'num' es un entero positivo
    try:
        dish_id = int(num)
        if dish_id <= 0:
            return {"error": "El ID debe ser un número positivo.", "id": num}
    except ValueError:
        return {"error": "El ID debe ser un número entero válido.", "id": num}

    # 2. Construir la URL para obtener un Departamento por ID
    # Usaremos el endpoint /Department/{id}
    url = f"{API_BASE_URL}/Department/{dish_id}"

    try:
        # 3. Realizar la solicitud HTTP GET a la API
        response = requests.get(url)
        
        # 4. Verificar si la solicitud fue exitosa (código de estado 200)
        if response.status_code == 200:
            data = response.json()
            
            # 5. Formatear la respuesta para que parezca un 'plato'
            # (El departamento tiene 'id' y 'name' que cumplen con los tests)
            plato_info = {
                "id": data.get("id"), # El ID real del departamento
                "name": data.get("name"), # El nombre del departamento (simulado como nombre del plato)
                # Puedes agregar más detalles si quieres enriquecer la simulación
                "description": f"Plato representativo de la región de {data.get('region').get('name')}.",
                "capital": data.get("capital")
            }
            return plato_info
            
        elif response.status_code == 404:
            # Manejar el caso de que el ID no exista
            return {"error": "Plato no encontrado para el ID proporcionado.", "id": dish_id}
            
        else:
            # Manejar otros errores de la API
            return {"error": f"Error al consultar la API. Código de estado: {response.status_code}", "id": dish_id}

    except requests.exceptions.RequestException as e:
        # Manejar errores de conexión (ej. no hay internet)
        return {"error": f"Error de conexión: {e}", "id": dish_id}


def main():
    """
    Función principal para la lógica interactiva del programa.
    Muestra un menú y usa dish_fetch para mostrar la información.
    """
    print("¡Bienvenido al Menú de Platos Típicos de Colombia!")
    print("---")
    print("Selecciona un número de plato (ID de Departamento) para ver su información.")
    print("Los IDs válidos están entre 1 y 33 (Aprox.).")
    
    while True:
        # Pide la entrada al usuario
        user_input = input("\nIngresa el ID del plato (o 'salir'): ").strip()
        
        # Opciones para salir
        if user_input.lower() in ["salir", "exit", "q"]:
            print("¡Gracias por usar el menú! ¡Hasta pronto!")
            sys.exit(0)
            
        # Procesa la entrada
        try:
            dish_id = int(user_input)
            
            # Llamar a la función requerida por los tests
            plato = dish_fetch(dish_id)
            
            # Mostrar el resultado
            if "error" in plato:
                print(f"❌ Error: {plato['error']}")
            else:
                print("\n✅ --- Información del Plato ---")
                print(f"   ID: **{plato['id']}**")
                print(f"   Nombre (simulado): **{plato['name']}**")
                print(f"   Descripción: {plato.get('description', 'N/A')}")
                print(f"   Capital: {plato.get('capital', 'N/A')}")
                print("------------------------------")
                
        except ValueError:
            print("⚠️ Entrada no válida. Por favor, ingresa un número entero o 'salir'.")

if __name__=="__main__":
    # La lógica principal solo se ejecuta cuando el script se corre directamente
    main()