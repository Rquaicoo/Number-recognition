# -*- coding: utf-8 -*-
"""Number_detection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CeZsD6KAAbV0qKI3RHSJXk5-AGmYPqz_
"""

from keras.datasets import mnist

(train_imgs, train_labels) , (test_imgs, test_labels) = mnist.load_data()

import numpy as np
from keras.utils import to_categorical

print("The shape of the train images are %s \n and that of train labels are %s" % (train_imgs.shape,train_labels.shape))
print("The shape of the test images are %s \n and that of test labels are %s" % (test_imgs.shape,test_labels.shape))

plt.figure(figsize=(5,5))
for i in range(25):
  plt.subplot(5,5,i+1)
  plt.grid(False)
  plt.imshow(train_imgs[i], cmap=plt.get_cmap('gray'))
plt.show()



# laoding and preparing pixel 
(train_imgs, train_labels) , (test_imgs, test_labels) = mnist.load_data()
train_imgs = train_imgs.astype('float32')
test_imgs = test_imgs.astype('float32')
train_imgs = train_imgs / 255.0
test_imgs = test_imgs / 255.0
train_imgs = train_imgs.reshape(train_imgs.shape[0],28,28,1)
test_imgs = test_imgs.reshape(test_imgs.shape[0],28,28,1)
train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)

#buiding model
from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D, MaxPool2D
from keras.optimizers import SGD
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras import Model
early_stopping = EarlyStopping(monitor='val_loss',patience=5)
model_save= ModelCheckpoint('best_model.hdf5',save_best_only=True)
model = Sequential()
model.add(Conv2D(32, kernel_size=(3,3), kernel_initializer='he_uniform',
                 input_shape=(28,28,1)))
model.add(MaxPool2D(2))
model.add(Conv2D(64, kernel_size=(3,3), kernel_initializer='he_uniform'))
model.add(Conv2D(64, kernel_size=(3,3), kernel_initializer='he_uniform'))
model.add(MaxPool2D(2))
model.add(Flatten())
model.add(Dense(100,kernel_initializer='he_uniform',
                activation='relu'))
model.add(Dense(10, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer=SGD(lr=0.01, momentum=0.9),metrics=['accuracy'])
scores, history = [] , []
h = model.fit(train_imgs,train_labels,epochs=10,batch_size=32,validation_split=0.2,
              callbacks=[early_stopping,model_save])
_,acc = model.evaluate(test_imgs,test_labels, verbose=0)
print('%.3f' % (acc * 100.0))
scores.append(acc)
history.append(h)

#plotting loss curve
for i in range(len(history)):
  plt.subplot(2, 2, 1)
  plt.plot(h.history['loss'], color = 'orange', label= 'train')
  plt.plot(h.history['val_loss'], color = 'blue', label= 'test')
  plt.title('Classification loss')
  plt.subplot(2,1,2)
  plt.plot(h.history['accuracy'], color = 'orange', label= 'train')
  plt.plot(h.history['val_accuracy'], color = 'blue', label= 'test')
  plt.title('Classification Accuracy')
plt.show()

print('Accuracy: mean=%.3f std=%.3f, n=%d' % (np.mean(scores)*100, np.std(scores)*100, len(scores)))
# box and whisker plots of results
plt.boxplot(scores)
plt.show()

from keras.models import load_model
model.save('my_model.h5')
my_model = load_model('my_model.h5')
preds = my_model.predict(test_imgs)
my_model.summary()

# make a prediction for a new image.
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.models import load_model
 
# load and prepare the image
def load_image(filename):
	# load the image
	img = load_img(filename, grayscale=True, target_size=(28, 28))
	# convert to array
	img = img_to_array(img)
	# reshape into a single sample with 1 channel
	img = img.reshape(1, 28, 28, 1)
	# prepare pixel data
	img = img.astype('float32')
	img = img / 255.0
	return img
 -
# load an image and predict the class
def run_example():
	# load the image
	img = load_image('/content/drive/MyDrive/sample_image.png')
	# load model
	my_model = load_model('my_model.h5')
	# predict the class
	digit = my_model.predict_classes(img)
	print(digit[0])
 
# entry point, run the example
run_example()





