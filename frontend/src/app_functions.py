import pickle
import requests
import pandas as pd
from pathlib import Path

## function to make request to backend
def api_request(file,thresh=0.5):
    try:        
        req=requests.post('https://hxy1cn1sl8.execute-api.us-east-1.amazonaws.com/Prod/segment_tiff',data=file,params={'threshold':thresh})
 
        polygons=pickle.loads(req.content)
        polygons.to_csv(f'src/data/polygons.csv',index=False)
    except:
        return api_request(file)
   
## function to save img locally, make the request and save the response locally
def save_send_img(file,path_='src/data/'):
    print(str(file))
    img_path=Path(f'{path_}img.tiff')
    file.save(img_path)
    file_img=open(img_path,'rb').read()   
    api_request(file_img)


