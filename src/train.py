import tensorflow as tf
import numpy as np
import os
from util import load_params

import models
from dvc.api import make_checkpoint

MODEL_FILE = "models/model.h5"

class DVCCheckpointsCallback(tf.keras.callbacks.Callback):

    def __init__(self, frequency = 1):
        self.frequency = frequency

    def on_train_begin(self, logs=None):
        pass

    def on_train_end(self, logs=None):
        pass

    def on_epoch_begin(self, epoch, logs=None):
        pass

    def on_epoch_end(self, epoch, logs=None):
        if (epoch % self.frequency) == 0:
            make_checkpoint()

    def on_test_begin(self, logs=None):
        pass

    def on_test_end(self, logs=None):
        pass

    def on_predict_begin(self, logs=None):
        pass

    def on_predict_end(self, logs=None):
        pass

    def on_train_batch_begin(self, batch, logs=None):
        pass

    def on_train_batch_end(self, batch, logs=None):
        pass

    def on_test_batch_begin(self, batch, logs=None):
        pass

    def on_test_batch_end(self, batch, logs=None):
        pass

    def on_predict_batch_begin(self, batch, logs=None):
        pass

    def on_predict_batch_end(self, batch, logs=None):
        pass

def load_npz_data(filename):
    npzfile = np.load(filename)
    return (npzfile['images'], npzfile['labels'])

def history_to_csv(history):
    keys = list(history.history.keys())
    csv_string = ", ".join(["epoch"] + keys) + "\n"
    list_len = len(history.history[keys[0]])
    for i in range(list_len):
        row = str(i+1) + ", " + ", ".join([str(history.history[k][i]) for k in keys]) + "\n"
        csv_string += row

    return csv_string

def main():
    params = load_params()["train"]
    if params["resume"] and os.path.exists(MODEL_FILE):
        m = tf.keras.models.load_model(MODEL_FILE)
    else:
        m = models.get_model()
    m.summary()

    whole_train_img, whole_train_labels = load_npz_data("data/preprocessed/mnist-train.npz")
    test_img, test_labels = load_npz_data("data/preprocessed/mnist-test.npz")
    validation_split_index = int((1 - params["validation_split"]) * whole_train_img.shape[0])
    if validation_split_index == whole_train_img.shape[0]:
        x_train = whole_train_img
        x_valid = test_img
        y_train = whole_train_labels
        y_valid = test_labels
    else:
        x_train = whole_train_img[:validation_split_index]
        x_valid = whole_train_img[validation_split_index:]
        y_train = whole_train_labels[:validation_split_index]
        y_valid = whole_train_labels[validation_split_index:]

    print(f"x_train: {x_train.shape}")
    print(f"x_valid: {x_valid.shape}")
    print(f"y_train: {y_train.shape}")
    print(f"y_valid: {y_valid.shape}")

    history = m.fit(x_train,
                    y_train,
                    batch_size = params["batch_size"],
                    epochs = params["epochs"],
                    verbose=1,
                    validation_data = (x_valid, y_valid),
                    callbacks=[DVCCheckpointsCallback(frequency=1)])

    with open("logs.csv", "w") as f:
        f.write(history_to_csv(history))

    m.save(MODEL_FILE)

if __name__ == "__main__":
    main()
