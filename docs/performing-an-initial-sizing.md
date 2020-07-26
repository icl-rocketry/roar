---
description: How to use Roar to get an initial engine design
---

# Performing an Initial Sizing

## Looking into Initial Sizing

When you run `initialSizing.py` its really just doing three easy steps. 

```python
engine = SizingEngine()
engine.size()
engine.printTable()
```

First, an instance of SizingEngine is created. This is a class that holds all the \(many\) parameters needed to do a sizing. For instance, here is the first part SizingEngine:

{% code title="roar/src/initialSizing.py" %}
```python
...
class SizingEngine:

    def __init__(self):
        self.choiceFuel = 'wax'
        self.choiceOx = 'nitrous'

        self.specTotalImpulse = 13500 * u.N * u.s
        self.specThrustAvg = 1500 * u.N

        self.inputOFDesign = 6
        self.inputIspDesign = 300 * u.s

        self.constg0 = 9.81 * u.m * u.s**-2
        
        ...

```
{% endcode %}

The `__init__` method is called when we first create a `SizingEngine`. Since we need to define so many parameters, I decided to basically make it a class where you can see all the parameters and tweak it easily. 

Next, we call `engine.size()` which performs all the necessary computations for sizing. These outputs are saved back as properties of `engine`.

Finally, `engine.printTable()` prints \(and returns\) a `pandas.DataFrame` simply because the formatting is easiest using Pandas. Every parameter is listed in the table. 

#### Variable Naming:

* `choice` refers to cases where you need to choose an option. Its not often used in the sizing directly, but are very often important to justifying some of the other numbers you will be defining. 
* `spec` refer to inputs that are the specifications of the rocket. These are essentially the main variables you can/should tweak to get the engine you want.
* `input` is used to define parameters that are inputs, but based on the choices youve defined above, materials used, or physical constraints. These define the key underlying assumptions in the model so pay attention to them!
* `const` are for physical constants that really dont depend on anything. 
* `comp` variables are those that have been computed by `roar`

Variables follow `camelCase` and try to be as descriptive as possible, such that additional documentation isn't really needed.

#### Units

When doing a project like this, there are a lot of units flying around, and its very easy to miss a bracket or something and get very wrong answers. or to simply forget if something was in centi-meters or milimeters and end up with something very wrong. To solve this, I'm using a library called astropy.units, and all functions that interact with units are strict about only accepting the correct physical type. 

{% hint style="info" %}
A really good primer on astropy.units is available at its documentation: [https://docs.astropy.org/en/stable/units/](https://docs.astropy.org/en/stable/units/)
{% endhint %}

The basic idea is that a `Quantity` is a `Value` \* `Unit`

```python
>>> from astropy import units as u
>>> L1 = 2.5 * u.cm
>>> L1
<Quantity 2.5 cm>
```

  defines the variable L to be 2.5 centimetres. The main utility is that you can do normal mathematical operations with these quantities:

```python
>>> L2 = 3 * u.m
>>> L1 + L2
<Quantity 302.5 cm>
```

When you multiply the quantities:

```python
>>> rho = 1000 * u.kg/u.m**3
>>> m = L1 ** 3 * rho
>>> m
<Quantity 15625. cm3 kg / m3>
```

it may not come out as the most simplified form. You can either call `decompose` which tries to make it simpler, or access the `si` property which is guaranteed to get the quantity in SI units.

```python
>>> m.decompose()
<Quantity 0.015625 kg>

>>> m.si
<Quantity 0.015625 kg>
```

Astropy.units will detect if two units cant be combined:

```python
>>> L1 + rho

Traceback (most recent call last):
...
raise UnitConversionError(
    astropy.units.core.UnitConversionError: 
        'kg / m3' (mass density) and 'cm' (length) are not convertible
...
raise UnitConversionError(
    astropy.units.core.UnitConversionError: 
        Can only apply 'add' function to quantities with compatible dimensions
```

If you look at the Traceback result, you can figure out where you did something wrong.

{% hint style="info" %}
There are some operations that `units` may not handle as expected. For instance taking the inverse of an matrix doesn't always invert the units. 

Also, when taking powers, I strongly encourage using powers directly, rather than calling something like `np.sqrt()`
{% endhint %}

That is, 

```python
>>> x = 0.5 * u.Kelvin
>>> x**0.5 # GOOD
>>> np.sqrt(x) # BAD
```

Similarly, when dealing with regression rates, there are non-integer powers, and in this case it is better to work with the numerical SI value, and then reintroducing the units at the end. 

\(technically, I think the newer/current version of astropy handles np.sqrt\(\) and similar functions properly, but I havent tested it rigourously. Seems better to just convert stuff\)

For example:

{% code title="src/roarCore/sizing.py" %}
```python
@si
@u.quantity_input
def computeRegressionRate(
        oxFlux: uFlux,
        grainLength: u.m,
        regressionParams) -> u.m/u.s:

    a = regressionParams['a']
    n = regressionParams['n']
    m = regressionParams['m']

    # covert to si
    oxFlux = oxFlux.si.value
    grainLength = grainLength.si.value

    r = a * oxFlux**n * grainLength ** m

    return r * u.m/u.s
```
{% endcode %}

Here I have used type-hinting to specify which physical types must be passed into the function. For instance the grain length is specified as `u.m`, so any quantity that is a length can be passed into the function. Note, standard python floats _will_ fail. 

### How to change the parameters

You have two main choices.

1. Modify the values in `SizingEngine.__init__` directly.
2. Create an instance of SizingEngine, and then modify the specific parameters you want to modify before calling `engine.size()`

Feel free to do either! I think the second version is easier when experimenting across parameters. For instance, you can do:

```python
roar/src/ (roarEnv) $ python
...
>>> import roarCore.sizing as roar
>>> import astropy.units as u
>>> import copy

# import the sizing engine class
>>> from initialSizing import SizingEngine

# create a base engine
>>> baseEng = SizingEngine()
# change some parameters in the base engine and size it
>>> baseEng.specTotalImpulse = 12000 * u.N*u.s
>>> baseEng.size()
...
# now make a copy and modify some parameters
>>> eng2 = copy.deepcopy(baseEng)
>>> eng2.specTotalImpulse = 12500 * u.N * u.s
>>> eng2.size()

# compare them by printing both tables
>>> baseEng.printTable()
...
>>> eng2.size()
...

```

### Sizing

Currently, it follows the documentation pretty much exactly.

{% page-ref page="hybrid-engines/background-on-hybrids/sizing-a-hybrid.md" %}

Everything computation is implemented as a simple function, so its modular, and not class specific. All the parameters needed for a calculation must be passed in. As mentioned above there is unit checking, and by default, the `.si` version is returned. You can easily change this for instance

```text
>>> L1 = 5 * u.cm
>> L1
<Quantity 5. cm>

>>> L1.to(u.m)
<Quantity 0.05 m>
```

In jupyter-notebooks these are rendered using latex and looks awesome!

Changing how the sizing works \(the methods called or the order\) is not as simple as above. Instead I would recommend copying the entire `initialSizing` file, and modifying it with your own implementation of `SizingEngine.size()` and running that



### PrintTable\(\)

This function just saves the engine's parameters into a datatable, using pandas since they render well. It internally also sorts the parameters so they are easier to find. 



### exportAsEngine\(\)

The idea is to then take all the outputs from the sizing process and return a `roar.Engine` object that be simulated, plotted, analysed and modified easily. 

Ill do this after Ive actually implemented the simulation suite.

TODO: document and implement



## Refactoring

There are a bunch of things that could be refactored to clean up the code and allow the code to be more modular. However that is really only explored for the simulation pipeline. As far as an initial sizing goes, I believe having the simpler \(possibly repetitive\) structure I have here will make it easier to work with. 

But feel free to refactor the code!

