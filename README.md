## FARM_ML_infra
 This repo is a Machine learning infrastructure and operation demo project using published electrolyte formulation data to optimize Coulombic efficiency (often abbreviated as CE) of batteries. The repo currently consists of a MongoDB backend for data storage, fastAPI Python framework to connect to MongoDB and React.js with D3 and plotly for user and electrolyte formulation data management, user login and authentication/authorization and data visualization.
 The current repo demonstrates the following technology based on FARM (FastAPI-React-MongoDB) framework: 
 +  MongoDB to store formulation data, where a fixed schema is not possible due to the different number of compounds contained in each formulation
 +  Object Document Mapping (ODM) by Pydantic and Beanie to validate data
 +  FastAPI for DML operations to add, delete, update and query formulation data from MongoDB backend
 +  User authentication of React and FastAPI by JWT using localstorage on user's browser and user credentials stored in MongoDB
 +  Cheminformatics utility to calcuate the elemental ratios for each formulation using RDKit
 +  React.js frontend that allows users to login and manage MongoDB backend, and visualize data by D3.js and plotly.js
Components that will be added:
 + unit tests for frontend and backend
 + PCA of 13 element ratio features and data visualization of how the first two PCs are correlated to battery performance evaluated by CE
 + Dockerfiles of frontend and backend for deployment
 + a Jenkinsfile that will automatically run unit tests and package frontend and backend code to docker images, and push to docker registry for deployment on K8s
 + RandomForest and XGBoost model training code to predict CE by elemental ratios with model registration to MLFlow after models are trained
 + Airflow code for scheduled model training

