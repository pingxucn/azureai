# Create Python virtual environment

To create a virtual environment using Conda's "mini" environment, you can follow these step-by-step instructions. Conda mini is a minimal Conda installation that you can use to set up lightweight virtual environments.

## Windows setup

Step 1: Download in command window

```
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -o miniconda.exe
```

Step 2: Install Miniconda(default settings)

```
miniconda.exe
```

macOS or Linux, pls check: https://docs.conda.io/projects/miniconda/en/latest/index.html

Step 3: Start Miniconda \
From the Start menu, search for and open "Anaconda Prompt." \
Base command window displayed as below:

```
(base) C:\Users\{your name}>
```

Step 4: Create virtual environment that contains Python 3.9

```
conda create --name azure python=3.9 -y
```

Step 5: Activate virtual environment

```
conda activate azure
```

The active environment is also displayed in front of your prompt in (parentheses) or [brackets] like this:

```
(azure) C:\>
```

Verify which version of Python is in your current environment:

```
(azure) C:\>python --version
```

Step 6: Managing packages \
For example, install Jupyter in the current virtual environment

```
(azure) C:\>pip install ipykernel
```

Check to see if the newly installed program is in this environment:

```
(azure) C:\>conda list
```

Step 7: Deactivate

```
(azure) C:\>conda deactivate
```

output

```
(base) C:\>
```

More details, pls check: https://conda.io/projects/conda/en/latest/user-guide/getting-started.html
