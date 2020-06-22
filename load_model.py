from keras.models import load_model,Sequential
from keras.layers import Dense

def get_model_structure():
    VGG16 = load_model('models_and_weights\VGG16.h5')
    VGG16.layers.pop()
    return VGG16

def get_test_model(model_structure):
    model = Sequential() 
    for layer in model_structure.layers:
        model.add(layer)
    model.add(Dense(11, activation = 'softmax'))
    
    model.load_weights('models_and_weights/0619_01_weights.h5')
    return model



