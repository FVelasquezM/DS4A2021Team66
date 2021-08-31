import tensorflow as tf
#from tensorflow import keras.backend as K
from keras import backend as K
from io import BytesIO
from PIL import Image
import base64
import json
import numpy as np
import tifffile as tiff
import numpy as np
import pandas as pd
import cv2
from shapely.geometry import MultiPolygon, Polygon
from shapely.wkt import loads as wkt_loads
import shapely.wkt
import shapely.affinity
from collections import defaultdict
import pickle
import boto3
import os
import uuid
import mysql.connector


size = 160
s = 835
smooth = 1e-12

def store_to_s3(binary_data, keyname):
    """
    Stores binary_data to s3

    Parameters
    ----------
    binary_data : ByteStream
        the ByteStream to be written in S3
    keyname : string
        the name which will be used to save the object
    """

    print('environ')
    print(os.environ)
    client = boto3.client('s3')
    client.put_object(Body=binary_data, Bucket= os.environ['BUCKET_NAME'], Key=keyname)

def store_to_db(uid, file_name):
    """
    Stores uid and filename to rds.

    Parameters:
    -----------
    uid : string
        The resource's uid
    filename : string
        The resource's filename in AWS 
    """

    mydb = mysql.connector.connect(
        host="database-2.c0a84dqmckxu.us-east-1.rds.amazonaws.com",
        user="admin",
        password="12345678",
        database="images"
    )

    mycursor = mydb.cursor()

    sql = "INSERT INTO images (id, fileName) VALUES (%s, %s)"
    val = (uid, file_name)
    mycursor.execute(sql, val)

    mydb.commit()
    mydb.close()



def mask_to_polygons(mask, epsilon=5, min_area=1.):
    """
    Converts a binary mask of shape (size, size, 1) into a shapely Polygon

    Parameters
    ----------
    mask : ndarray
        The mask to convert
    epsilon : int, optional
        The epsilon factor for cv2's approxPolyDP function.
    min_area : int, optional
        The minimum number of contiguous pixels for a Polygon to be generated.
    """
    
    contours, hierarchy = cv2.findContours(((mask == 1) * 255).astype(np.uint8), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_KCOS)
    approx_contours = [cv2.approxPolyDP(cnt, epsilon, True)
                       for cnt in contours]
    if not contours:
        return MultiPolygon()

    cnt_children = defaultdict(list)
    child_contours = set()
    assert hierarchy.shape[0] == 1

    for idx, (_, _, _, parent_idx) in enumerate(hierarchy[0]):
        if parent_idx != -1:
            child_contours.add(idx)
            cnt_children[parent_idx].append(approx_contours[idx])

    # create actual polygons filtering by area (removes artifacts)
    all_polygons = []
    for idx, cnt in enumerate(approx_contours):
        if idx not in child_contours and cv2.contourArea(cnt) >= min_area:
            assert cnt.shape[1] == 1
            poly = Polygon(
                shell=cnt[:, 0, :],
                holes=[c[:, 0, :] for c in cnt_children.get(idx, [])
                       if cv2.contourArea(c) >= min_area])
            all_polygons.append(poly)
    # approximating polygons might have created invalid ones, fix them
    all_polygons = MultiPolygon(all_polygons)
    if not all_polygons.is_valid:
        all_polygons = all_polygons.buffer(0)
        # Sometimes buffer() converts a simple Multipolygon to just a Polygon,
        # need to keep it a Multi throughout
        if all_polygons.type == 'Polygon':
            all_polygons = MultiPolygon([all_polygons])
    return all_polygons

def adjust_contrast(bands, lower_percent=2, higher_percent=98):
    """
    Adjusts an image's contrast using the formula

    (pixel_value - lower_percentile)/(higher_percent - lower_percentile)

    Parameters
    ----------
    mask : ndarray
        The mask to convert
    lower_percent : int, optional
       The lower percent to be used for the contrast adjustment.
    higher_percent : int, optional
        The higher percent to be used for the contrast adjustment.
    """


    out = np.zeros_like(bands).astype(np.float32)
    n = bands.shape[2]
    for i in range(n):
        a = 0  # np.min(band)
        b = 1  # np.max(band)
        c = np.percentile(bands[:, :, i], lower_percent)
        d = np.percentile(bands[:, :, i], higher_percent)
        t = a + (bands[:, :, i] - c) * (b - a) / (d - c)
        t[t < a] = a
        t[t > b] = b
        out[:, :, i] = t

    return out.astype(np.float32)

def jaccard_coef(y_true, y_pred):
    """
    Computes the Jaccard Index: Intersection over Union.
    J(A,B) = |A∩B| / |A∪B| 
         = |A∩B| / |A|+|B|-|A∩B|

    Parameters
    ----------
    y_true : ndarray
        The ground truth.
    y_pred : ndarray
        The predicted values.
    """

    intersection = K.sum(y_true * y_pred, axis=[0, -1, -2])
    total = K.sum(y_true + y_pred, axis=[0, -1, -2])
    union = total - intersection

    jac = (intersection + smooth) / (union+ smooth)

    return K.mean(jac)

def SegNet():
    """
    Creates a tensorflow convolutional neural network based on the u-net architecture. 
    For more information on the network architecture please refer to the documentation.
    """
    
    tf.random.set_seed(32)
    classes= 10
    img_input = tf.keras.layers.Input(shape=(size, size, 8))
    x = img_input

    # Encoder 
    
    x = tf.keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same', kernel_initializer = tf.keras.initializers.he_normal(seed= 23))(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same',  kernel_initializer = tf.keras.initializers.he_normal(seed= 43))(x)
    x = tf.keras.layers.MaxPooling2D((2, 2), strides=(2, 2))(x)
    x = tf.keras.layers.Dropout(0.25)(x)
    
    x = tf.keras.layers.Conv2D(128, (3, 3), activation='relu', padding='same', kernel_initializer = tf.keras.initializers.he_normal(seed= 32))(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Conv2D(128, (3, 3), activation='relu', padding='same', kernel_initializer = tf.keras.initializers.he_normal(seed= 41))(x)

    x = tf.keras.layers.Conv2D(128, (3, 3), activation='relu', padding='same', kernel_initializer = tf.keras.initializers.he_normal(seed= 33))(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.MaxPooling2D((2, 2), strides=(2, 2))(x)
    x = tf.keras.layers.Dropout(0.5)(x)

    x = tf.keras.layers.Conv2D(256, (3, 3), activation='relu', padding='same', kernel_initializer = tf.keras.initializers.he_normal(seed= 35))(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Conv2D(256, (3, 3), activation='relu', padding='same', kernel_initializer = tf.keras.initializers.he_normal(seed= 54))(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Conv2D(256, (3, 3), activation='relu', padding='same', kernel_initializer = tf.keras.initializers.he_normal(seed= 39))(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Dropout(0.5)(x)
    
    #Decoder
    
    x = tf.keras.layers.UpSampling2D(size=(2, 2))(x)
    x = tf.keras.layers.Conv2D(128, kernel_size=3, activation='relu', padding='same', kernel_initializer = tf.keras.initializers.he_normal(seed= 45))(x)
    x = tf.keras.layers.Conv2D(128, kernel_size=3, activation='relu', padding='same', kernel_initializer = tf.keras.initializers.he_normal(seed= 41))(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Conv2D(128, kernel_size=3, activation='relu', padding='same', kernel_initializer = tf.keras.initializers.he_normal(seed= 49))(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Dropout(0.25)(x)
      
    x = tf.keras.layers.UpSampling2D(size=(2, 2))(x)
    x = tf.keras.layers.Conv2D(64, kernel_size=3, activation='relu', padding='same', kernel_initializer = tf.keras.initializers.he_normal(seed= 18))(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Conv2D(64, kernel_size=3, activation='relu', padding='same', kernel_initializer = tf.keras.initializers.he_normal(seed= 21))(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Conv2D(classes, kernel_size=3, activation='relu', padding='same', kernel_initializer = tf.keras.initializers.he_normal(seed= 16))(x)
    x = tf.keras.layers.Dropout(0.25)(x)
  
    x = tf.keras.layers.Activation("softmax")(x)
    
    model = tf.keras.Model(img_input, x)
  
    model.compile(optimizer=tf.keras.optimizers.Adam(lr=1e-4),loss='binary_crossentropy', metrics=[jaccard_coef])
    return model

def lambda_handler(event, context):
    """
    AWS lamba function handler. Receives an API Gateway event, expecting it to contain a binary tiff file.
    Returns a python dictionary containing the response code and a base64 encoded pickle file with the image's polygons.

    Parameters
    ----------
    event : ApiGatewayEvent
        The ApiGatewayEvent. It's expected to contain a tiff file in its body.
    context : Context
        AWS Event context.
    """

    #Load image, roll axis so that channels end up on the last dimension and adjust image contrast.
    image_bytes = event['body'].encode('utf-8')
    print("EVENT")
    print(event)
    img = tiff.imread(BytesIO(base64.b64decode(image_bytes)))
    img = np.rollaxis(img, 0, 3)
    img = adjust_contrast(img).copy()

    #Create CNN and load previously trained weights.
    model = SegNet()
    model.load_weights("model-weights.hdf5")

    res = model.predict(img.reshape((1, 160, 160, 8)))

    #If the predicted logits for any class is greater than 0.5, the class is asigned to the pixel.
    threshold = 0.5
    pred_binary_mask = res >= threshold


    # Get all the predicted classes into a dataframe
    DF  = pd.DataFrame(columns=["image", "class", "poly", 'Multi'])
    image, cl , ploy, t_l = [],[],[], []
    i = 0
    for j in range(10):
        ab = mask_to_polygons(pred_binary_mask[0, :,:,j], epsilon=1)
        t = shapely.wkt.dumps(ab)
        t_l.append(t)
        image.append(i+1)
        cl.append(j+1)
        ploy.append(len(ab))
        df = pd.DataFrame(list(zip(image, cl, ploy, t_l)), columns = ['image', 'class', 'poly', 'Multi'])
    DF = pd.concat([DF,df], ignore_index=True)

    #Stores the results to s3 and RDS for future reference
    uid = uuid.uuid4()
    store_to_s3(pickle.dumps(DF), f'{str(uid)}.p')
    store_to_db(str(uid), f'{str(uid)}.p')


    #Return the dataframe as a pickle file to the frontend so that it can be easily displayed.
    return {
        'statusCode': 200,
        'body': base64.b64encode(pickle.dumps(DF)).decode('utf-8'),
        'isBase64Encoded': True
    }
    
