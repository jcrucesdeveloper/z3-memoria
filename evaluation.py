from z3 import *
import math

def reshape_constraints_z3(e1, e2):
    """
    Verifica si un reshape de e1 a la forma e2 es válido usando Z3 solver.
    
    Args:
        e1: lista de dimensiones del tensor de entrada [d0, ..., dn]
        e2: lista de dimensiones objetivo [d'0, ..., d'm]
    
    Returns:
        bool: True si el reshape es válido, False en caso contrario
    """
    # Crear solver Z3
    s = Solver()
    
    # Variables simbolicas para las dimensiones
    e1_dims = [Int(f"e1_{i}") for i in range(len(e1))]
    e2_dims = [Int(f"e2_{i}") for i in range(len(e2))]
    
    # Restricciones C3: Producto de dimensiones debe ser igual
    product_e1 = 1
    for i, dim in enumerate(e1):
        product_e1 *= dim
        s.add(e1_dims[i] == dim)
    
    product_e2 = 1
    for i, dim in enumerate(e2):
        if dim != -1:
            product_e2 *= dim
        s.add(e2_dims[i] == dim)

    # Verifica que el producto de las dimensiones del tensor de entrada sea igual al producto de las dimensiones objetivo
    s.add(product_e1 == product_e2) 
    
    # Restricciones C4 y C5: Todas las dimensiones deben ser > 0 o = -1
    for i, dim in enumerate(e2):
        if dim == -1:
            # Para -1, permitir cualquier valor positivo
            s.add(e2_dims[i] > 0)
        else:
            # Para valores específicos, deben ser > 0
            s.add(e2_dims[i] > 0)
    
    # Verificar si es satisfacible
    return s.check() == sat

def check_reshape_with_z3(input_shape, target_shape):
    """
    Verifica si un reshape es válido usando Z3 antes de ejecutarlo.
    
    Args:
        input_shape: lista de dimensiones del tensor de entrada
        target_shape: lista de dimensiones objetivo
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if reshape_constraints_z3(input_shape, target_shape):
        return True, "Reshape válido (verificado con Z3)"
    else:
        # Calcular elementos para el mensaje de error
        input_elements = math.prod(input_shape)
        target_elements = math.prod(target_shape)
        
        error_msg = f"Reshape inválido (Z3): {input_shape} ({input_elements} elementos) -> {target_shape} ({target_elements} elementos)"
        return False, error_msg

def analyze_example_py():
    """
    Analiza el código de example.py para detectar problemas de reshape.
    """


    print("=== Análisis de example.py con Z3 ===")

    # Caso 1: [4, 2, 3] -> [4, 7]
    # Caso valido


    # Caso 2: [4, 2, 3] -> [4, 6]


    # Caso 3: [4, 2, 3] -> [4, 7]
    
    # Caso del ejemplo: [4, 2, 3] -> [4, 7]
    input_shape = [4, 2, 3]  # 24 elementos
    target_shape = [4, 7]    # 28 elementos
    
    is_valid, msg = check_reshape_with_z3(input_shape, target_shape)
    print(f"example.py reshape: {msg}")
    
    # Caso correcto: [4, 2, 3] -> [4, 6]
    correct_target = [4, 6]  # 24 elementos
    is_valid_correct, msg_correct = check_reshape_with_z3(input_shape, correct_target)
    print(f"Caso correcto: {msg_correct}")
    
    # Caso con -1 para inferencia automática
    auto_target = [4, -1]  # Z3 inferirá 6
    is_valid_auto, msg_auto = check_reshape_with_z3(input_shape, auto_target)
    print(f"Caso con inferencia automática: {msg_auto}")

# Ejemplo de uso
if __name__ == "__main__":
    analyze_example_py()
    
    print("\n=== Casos de prueba adicionales ===")
    
    # Caso válido
    input_shape = [4, 2, 3]  # 24 elementos
    target_shape = [4, 6]    # 24 elementos
    is_valid, msg = check_reshape_with_z3(input_shape, target_shape)
    print(f"Caso 1: {msg}")
    
    # Caso inválido (como en tu ejemplo)
    input_shape = [4, 2, 3]  # 24 elementos
    target_shape = [4, 7]    # 28 elementos
    is_valid, msg = check_reshape_with_z3(input_shape, target_shape)
    print(f"Caso 2: {msg}")
    
    # Caso con -1
    input_shape = [6, 4]     # 24 elementos
    target_shape = [2, -1]   # Z3 inferirá 12
    is_valid, msg = check_reshape_with_z3(input_shape, target_shape)
    print(f"Caso 3: {msg}") 
    