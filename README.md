This branch serves as the central place to store all the scripts we used in COMMA 2024 Demonstration

### Local Set-up

We recommend you use `conda` ([Conda Installation](https://docs.anaconda.com/free/miniconda/index.html)) to help manage all packages

You first need to clone the repo and switch to `explanation_visualisation` branch
```
git clone https://github.com/DaphneOdekerken/PyArg
cd pyarg
git checkout explanation_visualisation
```

Within the `pyarg` folder, you can run the following scripts to set up the environment
```
conda create -n pyarg python=3.11
conda activate pyarg
pip install -r requirement.txt
pip install -e .
python wsgi.py
```
Then you can go to tab `visualization -> abstract` to explored the **layered visualization**
