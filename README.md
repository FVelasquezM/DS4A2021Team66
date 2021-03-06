# DS4A2021Team66

This repository contains the final project carried out by team 66 of DS4A Colombia 2021. The project, carried out with Bogota's economic development secretary (SDE), allows users to upload 160 x 160, 8 channel images from World View 3. The images are then segmented by a U-Net-like model and a visualization is shown to the user.

This repository contains two modules: a dash frontend and a serverless prediction backend.

# Flask/Dash Frontend

For our application, we use the Flask framework for rendering the different routes, uploading the image,
and making the requests to our serverless backend. 
We embeeded a dash app within our main app to visualize the segmentation of our AI, and for user to interact inside the app with the different functionalities.

Our application is deployed at: http://67.228.206.201:5000/

## Frontend usage

To use the frontend, start by accessing it at the url: http://67.228.206.201:5000/
### Uploading an image
Once on the website, you will be presented with the following screen:
![Entry data point](dash-1.PNG)

Click the *Give it a try* button and select a 160x160 8-channel World View 3 Satellite image, you can find some sample images [here](https://drive.google.com/drive/folders/1SGMgrAGDwpqEkLlEdxxWehlr7VeF9Eqc?usp=sharing).  Once uploaded, wait a few seconds for the application to process your image.

### Visualizing the segmentation
![Visualization of AI's results](dash-2.PNG)

The data visualization shows the image being labeled by the corine land cover parameters, identifying the ten classes that are visualized in the bar chart, fulfilling the interactivity of being able to update the image and specify which of those ten classes you want to visualize individually.

## Frontend deployment

In order to run this project locally, on your machine, follow these steps:

1. Install the frontend requirements

    `pip install -r requirements.txt`
 
2. Start app_dash.py with:

    `python app_dash.py`

3. Start app.py with:

    `python app.py`

# Serverless backend

The serverless backend is developed with AWS's Serverless Application Model (SAM), for more information on how it can be built and deployed, [please refer to the AWS documentation.](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-getting-started-hello-world.html)

## Backend Architecture

The backend serverless architecture uses AWS APIGateway to expose a lambda function that, upon being called, loads the previously trained model and segments a 160x160 8 channel tiff image into one of the model's 10 classes(Buildings, Misc. Manmade structures, Roads, Tracks, Trees, Crops, waterways, standing water, large vehicles and small vehicles). The model's predictions are then returned as a dataframe to the Dashfrontend and, additionally, are saved in an RDS and an S3 bucket for future reference.

The overall architecture is shown in the following image:

![Backend architecture](BackendArchitecture.png)

## Model Architecture and performance

The model used is a U-Net-like deep convolutional neural network, the model and its pipeline is based on the work of [Kazi Saiful Islam Shawon](https://www.kaggle.com/ksishawon/segnet-dstl), [Sergey Mushinskiy](https://www.kaggle.com/ceperaang/lb-0-42-ultimate-full-solution-run-on-your-hw) and [Konstantin Lopuhin](https://www.kaggle.com/lopuhin/full-pipeline-demo-poly-pixels-ml-poly). The model's architecture is shown in the following figure:

![Model architecture](ModelArchitecture.jpeg)

The model was trained using World View 3 sensor data, taken from Kaggle's [Dstl Satellite Imagery Feature Detection competition](https://www.kaggle.com/c/dstl-satellite-imagery-feature-detection), which are 8 band multispectral: (red, red edge, coastal, blue, green, yellow, near-IR1 and near-IR2) satellite images.

The trained model achieved a test jaccard score of 0.49.

## API

The backend API can be accessed on the following URL: https://hxy1cn1sl8.execute-api.us-east-1.amazonaws.com/Prod/segment_tiff
The API expects to receive a POST petition in which the message body is a base64 encoded 160 x 160 8-channel World View 3 satellite image. Optionally, you may include a threshold query param, which is a value between 0 and 1 specifiying the segmentation threshold to use, if none is specified, 0.5 will be used. 

A sample Postman collection can be found in the backend folder.


## Backend deployment

1. To deploy the backend, firstly install AWS SAM following [this guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)  and then,  configure your AWS credentials following [this guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html).
2. Modify app.py so that the store_to_db function contains your RDS credentials.
3. Build the backend with 

    `sam build`

4. Deploy the backend with 

    `sam deploy`
    
