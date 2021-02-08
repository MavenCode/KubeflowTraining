#importing libraries
import argparse

def train(X_train,y_train):
    #importing libraries
    import numpy as np
    from tensorflow import keras
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense

   #loading the inputs
    X_train = np.load(X_train)
    y_train = np.load(y_train)
    
    #initializing the classifier model with its input, hidden and output layers
    classifier = Sequential()
    classifier.add(Dense(units = 16, activation='relu', input_dim=12,))
    classifier.add(Dense(units = 8, activation='relu'))
    classifier.add(Dense(units = 1, activation='sigmoid'))
    #Compiling the classifier model with Stochastic Gradient Desecnt
    classifier.compile(optimizer = 'adam', loss='binary_crossentropy' , metrics =['accuracy'])
    #fitting the model
    classifier.fit(X_train, y_train, batch_size=10, epochs=150)
    #saving the model
    classifier.save('classifier.h5')

#defining and parsing arguments
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--X_train')
    parser.add_argument('--y_train')
    args = parser.parse_args()
    print('Done with training')
    train(args.X_train,args.y_train)
