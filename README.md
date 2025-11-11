## FARM_ML_infra
 This repo is a Machine learning and AI infrastructure and applications demo project using published electrolyte formulation data to optimize Coulombic efficiency (often abbreviated as CE) of batteries. The repo currently consists of a MongoDB backend using atlas host for data storage, fastAPI Python framework to connect to MongoDB and React.js with D3 and plotly for user and electrolyte formulation data management, user login and authentication/authorization and data visualization. 
 
 In addition, it contains a Qdrant vector database as the backend database for RAG, a Langchain agent workflow that includes several advanced RAG techniques (CRAG, self RAG) to reduce the hallucination and irrelavant answers to questions, a fastAPI middle layer to provide REST API endpoints to answer and rephrase questions using Langraph agentic workflow, and a streamlit client that provides an interactvie chatbot for users to upload pdf files for vector search and ask questions. The purpose is to provide a framework with the corresponding tech stack for hosting prod level internal knowledge base storage that can be queried with valid answers. 

 The current repo demonstrates the following technology based on FARM (FastAPI-React-MongoDB) framework: 
 +  MongoDB to store formulation data, where a fixed schema is not possible due to the different number of compounds contained in each formulation
 +  Object Document Mapping (ODM) by Pydantic and Beanie to validate data
 +  FastAPI for DML operations to add, delete, update and query formulation data from MongoDB backend
 +  User authentication of React and FastAPI by JWT using localstorage on user's browser and user credentials stored in MongoDB
 +  Cheminformatics utility to calcuate the elemental ratios for each formulation using RDKit
 +  React.js frontend that allows users to login and manage MongoDB backend, and visualize data by D3.js and plotly.js
 +  Dockerfiles of frontend and backend for deployment
 +  K8s code to deploy frontend with nginx and backend with gunicorn/uvicorn services in prod system clusters
 +  K8s ingress to expose frontend(react.js using /webfront prefix) and backend(fastapi using /fastapi prefix)
 +  Communications between frontend and backend using backend ingress by /fastapi prefix. This is done by providing --build-arg http://<domain-name>/fastapi when building frontend docker image
 + commands to provision local qdrant docker for hosting a vector database for internal knowledge base
 + a langgraph workflow for information retrieval from vector database and internet search using several advanced RAG techniques to delivery validated answers
 + FastAPI that provide REST API endpoints to memorize and answer questions using the langchain RAG workflow
 + a streamlit that provide a chatbot frontend for users to ask questions
                                 
Components that will be added:
 + unit tests for frontend and backend
 + PCA of 13 element ratio features and data visualization of how the first two PCs are correlated to battery performance evaluated by CE
 + a Langgraph workflow that implement ReACT agent that can integrate the predictions of CE values and PCA bipolar plot information give an electrolyte composition. It should find out which tools to use in order to get prediction results.
 + a Jenkinsfile that will automatically run unit tests and package frontend and backend code to docker images, and push to docker registry for deployment on K8s
 + RandomForest and XGBoost model training code to predict CE by elemental ratios with model registration to MLFlow after models are trained
 + Airflow or Jenkins pipelines for scheduled model training



