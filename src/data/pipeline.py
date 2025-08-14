# src/data/pipeline.py
from pathlib import Path
import tensorflow as tf

IMG_SIZE = (224, 224)

def preprocess(img):
    img = tf.image.resize(img, IMG_SIZE)
    img = tf.cast(img, tf.float32) / 255.0
    return img

def load_image(path):
    img = tf.io.read_file(str(path))
    img = tf.io.decode_jpeg(img, channels=3)
    return img

def load_and_preprocess(path):
    return preprocess(load_image(path))

def make_augmenter():
    # Augmentation estável usando tf.image (sem rotação para evitar preenchimento preto)
    # Pequenas variações deixam a imagem visivelmente diferente, mas realista.
    def _augment(img):        # img: [H,W,3] float32 em [0,1]
        img = tf.image.random_flip_left_right(img)
        img = tf.image.random_brightness(img, 0.08)     # +- ~8% de brilho
        img = tf.image.random_contrast(img, 0.9, 1.1)   # +- ~10% contraste
        img = tf.image.random_saturation(img, 0.9, 1.1) # +- ~10% saturação
        img = tf.image.random_hue(img, 0.02)            # +- ~2% de hue
        img = tf.clip_by_value(img, 0.0, 1.0)
        return img
    return _augment
