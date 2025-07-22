from z3 import *
import math  

def reshape_constraints_z3(t_i, t_o, verbose=False):
    """
    Verifica si un reshape de t_i a la forma t_o es válido usando Z3 solver.
    
    Args:
        t_i: lista de dimensiones del tensor de entrada [d0, ..., dn]
        t_o: lista de dimensiones objetivo [d'0, ..., d'm]
        verbose: si es True, muestra información detallada del proceso Z3
    
    Returns:
        bool: True si el reshape es válido, False en caso contrario
    """
    # Crear solver Z3
    s = Solver()
    
    # Variables simbolicas para las dimensiones
    t_i_dims = [Int(f"t_i_{i}") for i in range(len(t_i))]
    t_o_dims = [Int(f"t_o_{i}") for i in range(len(t_o))]
    
    # Restricciones C3: Producto de dimensiones debe ser igual
    product_t_i = 1
    for i, dim in enumerate(t_i):
        product_t_i *= dim
        s.add(t_i_dims[i] == dim)
    
    product_t_o = 1
    for i, dim in enumerate(t_o):
        if dim != -1:
            product_t_o *= dim
        s.add(t_o_dims[i] == dim)

    # Verifica que el producto de las dimensiones del tensor de entrada sea igual al producto de las dimensiones objetivo
    s.add(product_t_i == product_t_o) 
    
    if verbose:
        print("Restricciones en lenguaje natural para el Z3")
        print(f"Dimensiones simbolicas para t_i: {t_i_dims}")
        print(f"Dimensiones simbolicas para t_o: {t_o_dims}")
        print(f"Producto t_i: {product_t_i}")
        print(f"Producto t_o: {product_t_o}")
        print(f"Restricción de igualdad: {product_t_i} == {product_t_o}")
    
    # Restricciones C4 y C5: Todas las dimensiones deben ser > 0 o = -1
    for i, dim in enumerate(t_o):
        if dim == -1:
            # Para -1, permitir cualquier valor positivo
            s.add(t_o_dims[i] > 0)
            if verbose:
                print(f"Restricción para t_o_dims[{i}] (dim={dim}): {t_o_dims[i]} > 0")
        else:
            # Para valores específicos, deben ser > 0
            s.add(t_o_dims[i] > 0)
            if verbose:
                print(f"Restricción para t_o_dims[{i}] (dim={dim}): {t_o_dims[i]} > 0")
    
    # Verificar si es satisfacible
    result = s.check()
    
    if verbose:
        print("")
        print("Restricciones en el solver:")
        for i, constraint in enumerate(s.assertions()):
            print(f"  {i+1}. {constraint}")
        
        print(f"\nResultado del solver: {result}")
    return result == sat

def reshape_z3(input_shape, target_shape, verbose=False):
    """
    Verifica si un reshape es válido usando Z3 antes de ejecutarlo.
    
    Args:
        input_shape: lista de dimensiones del tensor de entrada
        target_shape: lista de dimensiones objetivo
        verbose: si es True, muestra información detallada del proceso Z3
    Returns:
        tuple: (is_valid, error_message)
    """
    if reshape_constraints_z3(input_shape, target_shape, verbose):
        return True, "Reshape válido"
    else:
        # Calcular elementos para el mensaje de error
        input_elements = math.prod(input_shape)
        target_elements = math.prod([d for d in target_shape if d != -1])
        
        error_msg = f"Reshape inválido (Z3): {input_shape} ({input_elements} elementos) -> {target_shape} ({target_elements} elementos)"
        return False, error_msg


if __name__ == "__main__":
    print("\n=== Análisis de reshape con Z3 ===")
    
    # Ejemplo 1: [4, 2, 3] -> [4, 6]
    # 24 elementos -> 24 elementos
    # Valido
    input_shape = [4, 2, 3]  # 24 elementos
    target_shape = [4, 6]    # 24 elementos
    print(f"Caso 1: [4, 2, 3] -> [4, 6]")
    is_valid, msg = reshape_z3(input_shape, target_shape, verbose=True)
    print(f"{msg}")
    print("##############################################") 
    # Ejemplo 2: [4, 2, 3] -> [4, 7]
    # 24 elementos -> 28 elementos
    # Invalido
    input_shape = [4, 2, 3]  # 24 elementos
    target_shape = [4, 7]    # 28 elementos
    print("Caso 2: [4, 2, 3] -> [4, 7]")
    is_valid, msg = reshape_z3(input_shape, target_shape, verbose=True)
    print(f"{msg}")
    
    # # Caso 3: [6, 4] -> [-2, -1]
    # 24 elementos -> 12 elementos
    # Invalido porque -2 no es > 0
    input_shape = [6, 4]     
    target_shape = [2, -1]   
    is_valid, msg = reshape_z3(input_shape, target_shape, verbose=True)
    print(f"Caso 3: [6, 4] -> [2, -1] {msg}")
    