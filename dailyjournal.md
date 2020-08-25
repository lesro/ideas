# Daily Journal Entry

**DAY 1:**
- wrote script to organize the train, validation, and test data into relative folders using os library. Became familiar with os functions for future use. 
- spending large portion of the my day reading and understanding keras API. Notes on things i've read:
    * image_dataset_from_directory is a tf.nightly function and I needed to pip install to use, this was to convert the complete path for each data set (train, valid, test) into grayscale, without doing it image by image. 
    * ImageDataGenerator is an augmentation, data generator that allows you to make subtle changes that can occure in real situtions without needing to go throuhg the arduous process of collecting new images.
        * rotation_range; not used in initial train
        * shear_range; not used in initial train
        * hori & vert flip; not used in initial train
        * fill_mode; not used in initial train 
        * and many more... above are some I will use when iterating through my model
- built the first baseline CNN model: (still grappling with what each layer in CNN does)
    * Sequential model
    * 3 Conv2D hidden layers
        * first 2 layers had filter=32, kernel_size=(5,5), activation='relu' and used maxpooling window pool_size=(2,2)
        * third layer used filter=64, kernel_size=(5,5), activation='relu' and used maxpooling window pool_size=(2,2)
    * applying reshaping of the data using flatten
    * applying 2 Dense layers 
        * first dense layer used unit=24, activation=relu.
        * second dense layer used unit=24, activation=tanh.
        * learned that using a unit=(less than # of classes) will return imcompatiable shape size [batch_size, unit] vs. [batch_size, classes], this comparison occurs between the train and validation set. 
    * applied a dropout rate between the 2 dense layers dropout=.5, helps prevent overfitting. 

- compiled the model using the following:
    * optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'
- finally I fit the model and used epoch=2 and the results were TERRIBLE!! (batch_size was 100)
- **1st attempt:** <br>
    RESULTS: <br>
    * Epoch 1/2 60/60 - 246s 4s/step - loss: nan - accuracy: 0.0530 - val_loss: nan - val_accuracy: 0.0536
    * Epoch 2/2 60/60 - 249s 4s/step - loss: nan - accuracy: 0.0539 - val_loss: nan - val_accuracy: 0.0536
- **2nd attempt:** <br>
    * changed all Conv2D layers kernel_size=(2,2)
    * changed 2nd dense layer activation='softmax' <br>
    RESULTS:
    * 60/60 - 118s 2s/step - loss: 11.0343 - accuracy: 0.0525 - val_loss: 3.1642 - val_accuracy: 0.0536
    60/60 - 118s 2s/step - loss: 3.1604 - accuracy: 0.0500 - val_loss: 3.1510 - val_accuracy: 0.0536
- **3rd attempt:** <br>
    * changed epoch to 5, did not yield different results. Exactly the same val_accuracy with slight decrease in loss.   

- **nth attempt:** <br>
    * after several iterations of the model, modifying image_size to (100,100), simplifying to 2 hidden layers, adding a dropout rate of .15 at each Conv2D layer, removing 1 dense layer and converting activation at dense layer to sigmoid, increased batch_size to 500, set featurewise_std_normalization=True;  the model kept giving me a validation accuracy of .0536.
    * finally after implementing rescaling when using the ImageDataGenerator 1./255, the model finally started to show a quicker learning rate and resulted in the following:
    RESULTS:
    Epoch 1/2: 12/12 - 76s 6s/step - loss: 3.0013 - accuracy: 0.1200 - val_loss: 2.2403 - val_accuracy: 0.3552
    Epoch 2/2: 12/12 - 88s 7s/step - loss: 1.5180 - accuracy: 0.5890 - val_loss: 0.5528 - val_accuracy: 0.8405
- **last attempt for the day** <br>
Model: "sequential_3"
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
_________________________________________________________________
_________________________________________________________________
conv2d_6 (Conv2D)            (None, None, None, 32)    896       
_________________________________________________________________
max_pooling2d_6 (MaxPooling2 (None, None, None, 32)    0         
_________________________________________________________________
dropout_3 (Dropout)          (None, None, None, 32)    0         
_________________________________________________________________
conv2d_7 (Conv2D)            (None, None, None, 32)    9248      
_________________________________________________________________
max_pooling2d_7 (MaxPooling2 (None, None, None, 32)    0         
_________________________________________________________________
dropout_4 (Dropout)          (None, None, None, 32)    0         
_________________________________________________________________
flatten_3 (Flatten)          (None, None)              0         
_________________________________________________________________
dense_3 (Dense)              (None, 24)                62232     
_________________________________________________________________
_________________________________________________________________
Total params: 72,376
Trainable params: 72,376
Non-trainable params: 0
_________________________________________________________________
    RESULTS:
    Epoch 1/5: 12/12 - 77s 6s/step - loss: 0.4625 - accuracy: 0.8461 - val_loss: 0.2824 - val_accuracy: 0.9169
    Epoch 2/5: 12/12 - 77s 6s/step - loss: 0.2573 - accuracy: 0.9133 - val_loss: 0.1631 - val_accuracy: 0.9477
    Epoch 3/5: 12/12 - 73s 6s/step - loss: 0.1581 - accuracy: 0.9486 - val_loss: 0.1048 - val_accuracy: 0.9759
    Epoch 4/5: 12/12 - 78s 6s/step - loss: 0.1105 - accuracy: 0.9649 - val_loss: 0.0796 - val_accuracy: 0.9799
    Epoch 5/5: 12/12 - 75s 6s/step - loss: 0.0988 - accuracy: 0.9701 - val_loss: 0.0591 - val_accuracy: 0.9853

**MODEL EVALUATION**
24/24 - 3s 123ms/step - loss: 0.0591 - accuracy: 0.9853
Test accuracy 98.53%