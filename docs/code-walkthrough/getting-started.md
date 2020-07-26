# Getting Started

## Getting Roar to Roar

Roar is based in Python, and as it is in active development, it is not provided as a python package. Instead, the core functionality is offered as a set of `.py` files, that can be imported, and used in your experiments.

## Setting Up \(TLDR\)

Clone the repository to a local folder. Next:

```text
roar $ cd src
roar/src $ conda env create -f environment.yaml
roar/src $ conda activate roarEnv
roar/src (roarEnv) $ python initialSizing.py
```

Will print to the terminal screen the sizing for a rocket, with the default parameters that I had already specified. See the next page to understand how to use the script properly.

## Setting up

{% hint style="info" %}
If you are comfortable with setting up Github and Python on your computer, feel free to skip this section!
{% endhint %}

{% hint style="info" %}
The commands below follow for macs/linux. Windows commands might be slightly different.
{% endhint %}

Make a directory to hold everything

```text
$ mkdir roar
$ cd roar
```

Clone/fork the Github repository \([https://github.com/icl-rocketry/roar](https://github.com/icl-rocketry/roar)\) into this folder. This should be your directory structure

```text
roar
├── LICENSE
├── docs
│   ├── ...
└── src
    ├── environment.yaml
    ├── initialSizing.py
    ├── roarCore
    │   └── sizing.py
    └── setup.md
```

The docs folder generates this `gitBook` project, and `src` contains all the code. `roarCore` contains the main files that have the functionality of sizing, simulating etc.  

I recommend using `Conda` to manage dependencies and requirements. I have used `Python3.8, numpy, scipy, matplotlib, astropy` for this project. `astropy.units` handles all the units in this project as is extremely easy to use. 

Check that `conda` is working:

```text
roar/src $ conda 
```

\(its working if you can see some help text\)

To use the exact `conda` environment that I used for development, run the following within the src folder:

```text
roar/src $ conda env create -f environment.yaml

roar/src $ conda activate roarEnv
```

The first line creates a virtual environment on your computer \(not in this folder\) with all the necessary dependencies. Next, we activate the environment, such that \(in this terminal\) all the following commands use this virtual environment.

You should now have access to the exact python environment that I was using. Test this, by running

```bash
roar/src $ python
```

You should see an output like:

```text
Python 3.8.3 (default, Jul  2 2020, 11:26:31)
[Clang 10.0.0 ] :: Anaconda, Inc. on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

which means that you have Python 3.8.3 running, like me. 

You can exit by running `exit()` or pressing `Ctrl-D`

Check that `roar.sizing` is working:

```bash
roar/src $ python initialSizing.py
```

This will produce an output something like:

```text
~~ Roar Sizing Tool ~~
Starting Sizing...
Sizing Successful !!
                                                                 0
choiceFuel                                                     wax
choiceOx                                                   nitrous
choicePortType                                            circular
compAreaCombustionChamber                 0.0022148195058482546 m2
compAreaExit                                0.20588040980042585 m2
compAreaRatioExit                                          778.042
...
```

In the next section, we will understand what this means and how to use it. 



If you are interested, see the notes in `/src/setup.md` to see how I made my environment.



