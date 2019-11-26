import numpy as np
import matplotlib.pyplot as plt


from akipy.layers import Input, Som2D
from akipy.losses import ReverseExponentialDecay
from akipy.neural_network import Sequential
from utils.data_manager import DataManager

dm = DataManager()
attributes = [
    [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0],  # Dove
    [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],  # Hen
    [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],  # Duck
    [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1],  # Goose
    [1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0],  # Owl
    [1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0],  # Hawk
    [0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0],  # Eagle
    [0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0],  # Fox
    [0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0],  # Dog
    [0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0],  # Wolf
    [1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0],  # Cat
    [0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0],  # Tiger
    [0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0],  # Lion
    [0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0],  # Horse
    [0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0],  # Zebra
    [0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],  # Cow
]
train_set = []
test_set = []

for i in range(16):
    animal = [1 if j == i else 0 for j in range(16)]
    data_point = list(animal)
    data_point.extend(attributes[i])
    train_set.append(data_point)
    data_point = list(animal)
    data_point.extend([0 for j in range(13)])
    test_set.append(data_point)

dm.x_train = np.array(train_set)
dm.x_test = np.array(test_set)

model = Sequential('som_animal_clusters')
model.add(Input(units=29))
model.add(Som2D(units=(10, 10), sigma=1, time_constant=500, decay=ReverseExponentialDecay(time_constant=500)))

model.compile(optimizer='SGD', loss='WTA-min', metrics=['error'])

model.train(x_train=dm.x_train, y_train=dm.x_train, epochs=10, lr=0.1)

feature_maps = model.test(x_test=dm.x_train)

fig, axs = plt.subplots(4, 4, num=1, figsize=(15, 15), constrained_layout=True)
axs = axs.flatten()
for i in range(16):
    axs[i].imshow(feature_maps[i], cmap="gray")

fig.savefig('figures/feature_maps.png')
fig.show()

for i in range(16):
    print(np.unravel_index(feature_maps[i].argmin(), feature_maps[i].shape))

print()
