import torch

# Creamos un tensor de 2x3
x = torch.tensor([[1, 2, 3],
                  [4, 5, 6]])
print("Original:")
print(x)

# Reestructuramos el tensor a 3x2
y = x.reshape(3, 2)
print("\nDespués de reshape a 3x2:")
print(y)


