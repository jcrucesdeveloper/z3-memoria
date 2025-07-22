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
    
    # Restriccion C3: Producto de dimensiones debe ser igual
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
    
    # Restriccion C4: Todas las dimensiones de salida deben ser > 0 
    for i, dim in enumerate(t_o):
        s.add(t_o_dims[i] > 0)
        if verbose:
            print(f"Restricción para t_o_dims[{i}] (dim={dim}): {t_o_dims[i]} > 0")
    
    # Restriccion C5: Las dimensiones de entrada deben ser > 0 o igual a -1
    for i, dim in enumerate(t_i):
        if dim == -1:
            # Para -1, debe permanecer -1
            s.add(t_i_dims[i] == -1)
            if verbose:
                print(f"Restricción para t_i_dims[{i}] (dim={dim}): {t_i_dims[i]} == -1")
        else:
            # Para valores específicos, deben ser > 0
            s.add(t_i_dims[i] > 0)
            if verbose:
                print(f"Restricción para t_i_dims[{i}] (dim={dim}): {t_i_dims[i]} > 0")
    
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
        print("Reshape valido para el Z3")
        return True
    else:
        # Calcular elementos para el mensaje de error
        input_elements = math.prod(input_shape)
        target_elements = math.prod([d for d in target_shape if d != -1])
        print(f"Reshape inválido (Z3): {input_shape} ({input_elements} elementos) -> {target_shape} ({target_elements} elementos)")
        return False 


if __name__ == "__main__":
    print("\n=== Análisis de reshape con Z3 ===")
    
    # Ejemplo 1: [4, 2, 3] -> [4, 6]
    # 24 elementos -> 24 elementos
    # Valido
    input_shape = [4, 2, 3]  # 24 elementos
    target_shape = [4, 6]    # 24 elementos
    print(f"Ejemplo 1: [4, 2, 3] -> [4, 6]")
    reshape_z3(input_shape, target_shape, verbose=True)

    # Ejemplo 2: [4, 2, 3] -> [4, 7]
    # 24 elementos -> 28 elementos
    # Invalido
    input_shape = [4, 2, 3]  # 24 elementos
    target_shape = [4, 7]    # 28 elementos
    print(f"Ejemplo 2: [4, 2, 3] -> [4, 7]")
    reshape_z3(input_shape, target_shape, verbose=True)
    
    # Ejemplo 3: [6, 4] -> [-6, -4]
    # 24 elementos -> 24 elementos
    # Invalido porque -6 y -4 no son > 0
    input_shape = [6, 4]     
    target_shape = [-6, -4]   
    print(f"Ejemplo 3: [6, 4] -> [-6, -4]")
    reshape_z3(input_shape, target_shape, verbose=True)
    