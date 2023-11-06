# azureai

Project structure is described as below

## data

./data/speech keep wav files

## src

./src/app.py is sample python scirpt

./src/sample_notebook.ipynb is sample jupyter notebook

## Environment setup

A. How to setup miniconda virtual environment \
setup_miniconda.md

B. How to setup Visual Studio and Jupyter in VS (skip Anaconda setup since we did above) \
https://www.youtube.com/watch?v=h1sAzPojKMg

C. How to upload VS code to Github,

1. Adding a new SSH key to your GitHub account \
   https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account

2. Using Git with Visual Studio Code \
   https://www.youtube.com/watch?v=i_23KUAEtUM

## Switch Python Interpreter
To work with Python in Jupyter Notebooks, you must activate an Anaconda environment in VS Code, or another Python environment in which you've installed the Jupyter package. To select an environment, use the <strong>Python: Select Interpreter</strong> command from the Command Palette (Ctrl+Shift+P).

Once the appropriate environment is activated, you can create and open a Jupyter Notebook, connect to a remote Jupyter server for running code cells, and export a Jupyter Notebook as a Python file.

## Create or open a Jupyter Notebook
You can create a Jupyter Notebook by running the <strong>Create: New Jupyter Notebook</strong> command from the Command Palette (Ctrl+Shift+P) or by creating a new .ipynb file in your workspace.

## Access to Azure OpenAI

1.  Register Domain and email in [GoDaddy](https://www.godaddy.com/en-ca), first year is around C$42
2.  Apply for Azure free trial account using the email above
3.  Submit [a registration form](https://aka.ms/oai/access) to access to Azure OpenAI.
