import torch
import torch.nn as nn

# Red neuronal simple con reshape
class SimpleNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(6, 2)  # 6 entradas, 2 salidas
    
    def forward(self, x):
        # Reshape de (batch_size, 2, 3) a (batch_size, 6)
        x_flat = x.reshape(x.size(0), 7)  # Error: intentando reshape a 7 elementos en lugar de 6
        return self.fc(x_flat)

# Crear modelo e input
model = SimpleNet()
x = torch.randn(4, 2, 3)  # batch_size=4, forma (2, 3)

# Forward pass
output = model(x)

print("Forma del input:", x.shape)
print("Forma aplanada:", x.reshape(x.size(0), -1).shape)
print("Forma del output:", output.shape)
print("Output:\n", output)