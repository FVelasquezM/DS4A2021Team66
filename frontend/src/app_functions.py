import pickle
import requests
import pandas as pd
from pathlib import Path


def api_request(file, thresh=0.5):
    """
    Post request to serverless backend api where our model is lcoated
    Receives a csv with the classes and polygons classified by our model 

    Parameters
    ----------
    file: .tiff file
        Tiff file to be classified by our model
    thresh: float 
        Threshold applied. To be classified a prediction values has to be equal or greater than threshold 
    """
    try:
        req = requests.post('https://hxy1cn1sl8.execute-api.us-east-1.amazonaws.com/Prod/segment_tiff',
                            data=file, params={'threshold': thresh})

        polygons = pickle.loads(req.content)
        polygons.to_csv(f'src/data/polygons.csv', index=False)
    except:
        return api_request(file)


def save_send_img(file, path_='src/data/'):
    """
    Saves image locally and sends it to api backend. Image is then saved on the cloud

    Parameters
    ----------
    file: file storage
        Tiff file uploaded
    path: string
        Location of file

    """

    print(str(file))
    img_path = Path(f'{path_}img.tiff')
    file.save(img_path)
    file_img = open(img_path, 'rb').read()
    api_request(file_img)
