# How the env was set up

Create an environment using conda

```
src $ conda create --name roarEnv python=3.8
```

Activate the environment

```
src $ conda activate roarEnv
```

Installing the packages

```
src $ conda install numpy scipy matplotlib astropy
```

Exporting the environment as a yaml file

```
conda env export > environment.yaml
```

# Recreate the environment

Run

```
src $ conda env create -f environment.yaml
```

which should create an environment called `roarEnv` on your computer.

Now just active it:

```
src $ conda activate roarEnv
```

and you should be ready to go.
