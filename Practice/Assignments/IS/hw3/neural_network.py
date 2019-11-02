from losses import get_loss_function
from optimizers import get_optimizer


class Sequential:
    name = 'sequential'

    def __init__(self):
        self.layers = []
        self.loss_function = None
        self.metrics_names = None
        self.optimizer = None

    def add(self, layer):
        if len(self.layers) > 0:
            prev_layer = self.layers[-1]
            layer.set_input_size(prev_layer.n_units)
        self.layers.append(layer)

    def compile(self, optimizer, loss, metrics):
        self.loss_function = get_loss_function(loss)
        self.metrics_names = metrics
        self.optimizer = get_optimizer(optimizer, model=self)

    def train(self, x_train, y_train, epochs, lr, validation_set=None):
        # Input size validation
        if x_train.shape[1] != self.layers[0].n_units:
            raise Exception(f"Input shape {x_train.shape} does not match with input layer {self.layers[0].n_units}.")

        self.optimizer.set_training_data(x_train, y_train, lr, validation_set)

        # Start epochs
        for epoch in range(epochs):
            xq, yq = self.optimizer.get_data_point()
            self.optimizer.feed(xq, yq, epoch=epoch)

    def feed(self, x):
        pass

    def save(self, model_name, parent_dir):
        from datetime import datetime
        import json
        model = self.get_structure()
        timestamp = datetime.now()
        with open(f'{parent_dir}/{model_name}_{timestamp}.json', 'w', encoding='utf-8') as file:
            json.dump(model, file)

    def get_structure(self):
        return {
            'name': self.name,
            'layers': [layer.get_serialized() for layer in self.layers],
            'loss': self.loss_function.name,
            'metrics': self.metrics_names
        }

    def describe(self):
        print(self.get_structure())

    def load(self, name, parent_dir, find_latest=False):
        import json
        model_name = name if not find_latest else self._get_latest_model_name(name, parent_dir)
        with open(f'{parent_dir}/{model_name}', 'w', encoding='utf-8') as json_file:
            structure = json.load(json_file)
            return self._create_model_from_structure(structure)

    @staticmethod
    def _get_latest_model_name(model_name, parent_dir):
        import os
        files = os.listdir(parent_dir)
        files.sort(reverse=True)
        for file in files:
            if model_name in file:
                return file

    @staticmethod
    def _create_model_from_structure(structure):
        model = get_neural_network(structure['name'])
        model.loss_function = get_loss_function(structure['loss'])
        model.metrics_names = structure['metrics']

        import layers
        model.layers = [layers.create_layer_from_structure(layer) for layer in structure['layers']]


def get_neural_network(name):
    if name == Sequential.name:
        return Sequential()
    else:
        raise Exception(f"Model not found for {name}")