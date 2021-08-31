# DS4A2021Team66

This repository contains the final project carried out by team 66 of DS4A Colombia 2021. The project, carried out with Bogota's economic development secretary (SDE), allows users to upload 160 x 160, 8 channel images from World View 3. The images are then segmented by a U-Net-like model and a visualization is shown to the user.

This repository contains two modules: a dash frontend and a serverless prediction backend.

# Dash Frontend

## Uploading an image

<TODO>

## Visualizing the segmentation

<TODO, mencionar que se usa estándar corine land cover y demás>

# Serverless backend

The serverless backend is developed with AWS's Serverless Application Model (SAM), for more information on how it can be built and deployed, [please refer to the AWS documentation.](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-getting-started-hello-world.html)

## Backend Architecture

The backend serverless architecture uses AWS APIGateway to expose a lambda function that, upon being called, loads the previously trained model and segments a 160x160 8 channel tiff image into one of the model's 10 classes(Buildings, Misc. Manmade structures, Roads, Tracks, Trees, Crops, waterways, standing water, large vehicles and small vehicles). The model's predictions are then returned as a dataframe to the Dashfrontend and, additionally, are saved in an RDS and an S3 bucket for future reference.

The overall architecture is shown in the following image:

![Backend architecture](BackendArchitecture.png)

<TODO>

## Model Architecture and performance

<TODO>
