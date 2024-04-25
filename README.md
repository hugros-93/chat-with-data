# langchain
Langchain POC to chat with data.

## Overview
This repo contains a dash app that you can run locally to chat with your data. This app relies on OpenAI API for embedding and LLM models.

In details, the app will allow you to:
- load PDF file(s)
- transform and store these files into a document store
- use natural language to ask a question about about your data
- answer your questions based on the files you loaded
- list you the references used to answer you

## Setup
In order to run the app, you need to follow these steps:
- create a virtual environemnt
- install requirements using the `requirements.txt` file
- add your OpenAI key as a local env variable `OPENAI_KEY`

## Repo structure
Overview of the folders and files in this repo:
- `assets/`: assets for the dash app
- `chroma/`: where ChromaDB files will be created
- `data/`: where the pdf files you load will be stored
- `mooc/`: some usefull ressources from the MOOC [Chat with your data](https://www.deeplearning.ai/short-courses/langchain-chat-with-your-data) from deeplearnin.ai
- `utils/`: utility python functions for RAGs and Dash app
- `app.py`: the main file to run the app
- `requirements.txt`: list of python requirements