# Mini Rag

This the minimal implementation of the RAG model for question  answering 

## requirements

python 3.8 or later 

#### install python miniconda or anaconda

1) download and install [miniconda](https://docs.anaconda.com/free/miniconda/#quick-commmend-line-install)

2) create a new environment:
```bash
$ conda create -n rag python=3.8 
```
3) activate the environment:
```bash
$ conda activate rag
```

## Installation 

### install the requirements packages

```bash
pip install -r requirements.txt
```

### setup the environment variables

```bash
cp .env.example .env
```
and set your environment variables in `.env` file.


## run the FastAPI server
```bash
uvicorn main:app --reload
```



