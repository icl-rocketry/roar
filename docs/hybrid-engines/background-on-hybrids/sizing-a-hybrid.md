---
description: Detailed explanation of the equations used in Roar
---

# Sizing a Hybrid \(in detail\)

There are two linked, but separate tools within Roar. 

1. Preliminary Design/Initial Sizing \(ie. make a guess of a design\)
2. Simulation \(ie. check if it works\)

This section answers point 1. 

It generally follows the table by Humble, but flips the orders around a bit

{% page-ref page="./" %}

## Initial Design `roar.size`

Note, here, the inputs and the computations are defined in the order they are needed, but the code imports all requirements first. 

NOTE: 

`INPUT SPEC` : input a user defined performance requirement

`INPUT PROP`: input a physical constant/property that is not user defined, but may be user estimated.

### 1. Choose propellant combination

`CHOOSE` fuel species

`CHOOSE` oxidiser species

See section on choosing an oxidiser and fuel combination for details. Some of the later inputs depend on this choice.

{% page-ref page="fuel-and-oxidiser-selection-and-thermodynamics.md" %}

### 2. Compute Burn Time

`INPUT SPEC` Total impulse the engine must provide, $$I_t$$ \[N s\]

This should be estimated from the rockets mission requirements \(not covered here\)

`INPUT SPEC` Thrust requirement, $$\bar F$$\[N\]

This is the average thrust.

`COMPUTE` Burn Time, $$t_{burn}$$ \[s\]

$$
I_t = \int F dt \approx \bar F \cdot t_{burn}
$$

$$
\therefore t_{burn} = \frac{I_t}{\bar F}
$$

### 3. Determine Oxidiser and Fuel Mass

`INPUT PROP` Estimated specific impulse of propellant combination, $$I_{sp}$$ \[s\]

`INPUT PROP` Design oxidiser to  fuel ratio $$OF$$ \[-\]

Implicitly, this means mass of oxidiser to mass of fuel ratio.

These are both based on the propellant choice and semi-empirical analysis.

{% page-ref page="fuel-and-oxidiser-selection-and-thermodynamics.md" %}



`INPUT PROP` standard acceleration due to gravity, $$g_0 = 9.81$$m/s

`COMPUTE` Total Propellant mass, $$m_{prop}$$\[kg\]

$$
m_{prop} = \frac{I_t}{I_{sp} g_0}
$$

`COMPUTE` Oxidiser mass, $$m_{ox}$$\[kg\]

$$
OF = \frac{m_{ox}}{m_{fuel}} \quad, \quad m_{prop} = m_{ox} + m_{fuel}
$$

$$
\therefore m_{ox} = \frac{m_{prop} \cdot OF}{ OF + 1}
$$

`COMPUTE` Fuel mass, $$m_{fuel}$$\[kg\]

$$
m_{fuel} = m_{prop} - m_{ox} =  \frac{m_{prop}}{OF+1}
$$

`CORRECT` fuel and oxidiser masses based on ullage, $$\varepsilon$$

Don't forget you can't get to the end of the entire fuel tank. As such, you need to account for 'ullage.' The amount of ullage you include is an important design decision but with very few good ways to estimate. Starting with ~ 5% might be a decent starting point. 

$$
m_{fuel} = m_{fuel} \cdot (1 + \varepsilon_{fuel})
$$

$$
m_{ox} = m_{ox} \cdot (1 + \varepsilon_{ox})
$$

### 

### 4. Estimate initial flow rate requirements

A rocket might have an initial thrust requirement in addition to the average thrust requirement. If it doesn't, perhaps just use the average thrust, or \(typically\) a value ~ 20% greater is often used, such that the average thrust requirement is better met. 

`INPUT SPEC` Initial thrust requirement, $$F_{init}$$ \[N\]

`INPUT PROP` Initial specific impulse, based on initial OF ratio and nozzle expansion ratio $$I_{sp, init}$$ \[s\]

`COMPUTE` Initial propellant mass flow rate, oxidiser mass flow rate and fuel flow rates:

$$
\dot m_{prop, init} = \frac{F_{init}}{I_{sp, init} g_0}
$$

$$
\dot m_{fuel, init} = \frac{\dot m_{prop, init}}{OF_{init} +1 }
$$

$$
\dot m_{ox, init} = \dot m_{prop, init} - \dot m_{fuel, init}
$$



### 5. Determine Oxidiser Properties

`INPUT SPEC` Combustion chamber pressure $$P_{cc}$$\[Pa\]

`INPUT PROP` Oxidiser tank temperature, $$T_{ox}$$ \[K\] 

`INPUT PROP` Combustion efficiency \(often guessed to be 98%\) $$\eta_c$$ \[-\]

\(whether this is a physical property or a design parameter is a bit of a debate - in my code I assume it is a physical property\)

`COMPUTE` Vapour pressure, $$P_{vap}$$\[Pa\]

`COMPUTE` Liquid Ox Density, $$\rho_{ox, l}$$\[kg m-3\]

`COMPUTE` Vapour Ox Density, $$\rho_{ox, g}$$ \[kg m-3\]

`COMPUTE` Flame Temperature, $$T_{flame}$$\[K\]

`COMPUTE` Ratio of specific heats, $$\gamma$$\[-\]

`COMPUTE` Molar mass of oxidiser, $$\mathcal{M}_{ox}$$ \[kg/mol\]

`COMPUTE` Oxidiser specific gas constant $$R$$ \[J kg-1 K-1\]

`COMPUTE` characteristic speed of propellants $$c^*$$ \[m/s\] 

These calculations are based on the properties of the oxidiser used, discussed in the thermochemistry section.

### 6. Injector Sizing

Since we are trying to define a self-pressuring system, we must have that the static pressure must always be dropping in the system. This allows us to size the injector. 

{% hint style="warning" %}
Note there are other ways to do this part of the analysis, and they may be more suitable -  testing is absolutely critical here.
{% endhint %}

`INPUT SPEC` minimum pressure drop across injector, $$\Delta P_{inj}/P_{cc}$$. Usually set to 10-25% of the combustion chamber pressure, to protect against pressure spikes \[source: Rocket Propulsion Elements, Sutton and SPAD\]

`INPUT PROP` the head loss coefficient of the injector, $$K$$ \[-\]. This number _must_ be obtained experimentally, and infact has a rather significant impact on the entire rocket. Here are some estimates for well designed injectors used in industry: K = 1.2 for injectors with radiused edges, 1.7 for sharp edges. \[Example Testing\]\([http://edge.rit.edu/edge/P18102/public/Testing/Subsystem%20Tests/Injector%20Testing](http://edge.rit.edu/edge/P18102/public/Testing/Subsystem%20Tests/Injector%20Testing)\)

`COMPUTE` area of injector holes required, $$A_{inj}$$\[m2\]

> Theory aside:  
> We model the pressure drop across a component as some fraction of the change in the dynamic pressure across it. If we assume the injector inlet is very slow compared to the exit speed \(which is definitely desired\), the  pressure can be modelled as

$$
\Delta P_{inj} = K \frac{1}{2} \rho_{ox, l} (v^2 - 0)
$$

> where $$K$$ is the head loss coefficient \[-\], $$\rho_{ox,l}$$ is the liquid oxidiser density \(assuming it hasnt changed across the injector\) and $$v$$is the exit speed of the liquid.
>
> We now use the continuity equation,

$$
\dot m_{ox} = \rho_{ox, l} v A_{inj}
$$

> to compute the area of all the holes in our injector,

$$
A_{inj} = \dot m_{ox} \sqrt{\frac{K}{2 \rho_{ox, l} \Delta P_{inj}}}
$$

Here, we can choose to make many small holes, or few large holes. But this is left upto the designer for further analysis. 

### 7. Port Sizing

Finally, we can estimate the size of the port. To do this, we need to know the maximum oxidiser mass flow rate allowed. 

`INPUT PROP` Maximum oxidiser mass flux $$G_{ox, max}$$\[kg m-2 s-1\]

This pretty much the second most important unknown parameter \(after the regression rate of the propellants\). If you set the value too low, there is too little oxygen for combustion, and either the flame will die out, or burn slowly. If the value is set too high, its like blowing out a candle - the air is moving too quickly to sustain combustion. Humble claimed the maximum oxidiser flux is a parameter between 350-700 kg m-2 s-1. 

`COMPUTE` Initial port cross-sectional area, $$A_{port, init}$$\[m^2\]

$$
A_{port, init} = \frac{\dot m_{ox, init}}{G_{ox,max}}
$$

`CHOOSE` Port type - the code was developed for two types of ports, circular and D-ports, which are essentially circular ports, but with a web running down the middle. 

#### For a circular port:

`COMPUTE` Required initial inner port diameter, $$D_{port, init}$$ \[m\]

$$
D_{port, init} = 2 \sqrt{\frac{A_{port, init}}{\pi}}
$$

`COMPUTE` port initial perimeter, $$\mathcal{P}_{init}$$ \[m\]

$$
\mathcal{P}_{init} = \pi D_{port, init}
$$

#### For a D port

`COMPUTE` Initial inner port diameter, $$D_{port, init}$$ \[m\]

`COMPUTE` Initial Central Fuel Web Thickness $$t_{web}$$\[m\]

Because this geometery is a bit more complex, a root finding method is used. 

`COMPUTE` port initial perimeter, $$\mathcal{P}_{init}$$ \[m\]

{% hint style="danger" %}
TODO: implementation details for D-port fuel web
{% endhint %}

#### For all port type:

Estimate the length of the fuel grain needed. 

> Theory Aside:
>
> We need to be producing the required amount of fuel, $$\dot m_{fuel}$$Therefore, there needs to be enough surface area that receeds at the regression rate. Ie.

$$
\dot m_{fuel, init} = 
\rho_{fuel} \dot r (L \mathcal{P}_{init})
$$

> but since the regression rate itself is a function of the length, $$\dot r = a G_{ox} ^ n L ^ m $$, we need to solve for $$L$$,

$$
L = \left({\frac{\dot m_{fuel}}{a \rho_{fuel} G_{ox}^n \mathcal{P}_{init}}}\right)^{1/(m+1)}
$$

Note: for different regression rate models, the length estimate will be different! Also, this model does not break for $$m=0$$which is rather helpful.

Now we can also estimate the final diameter of the fuel grains, since we know the total mass of 

`COMPUTE` Final diameter of fuel grains, based on how much fuel needs to be stored.

#### For a circular port:

$$
m_{fuel} = \rho_{fuel} L \pi \left(\frac{D_{port, final}^2 - D_{port, init}^2}{4}\right)
$$

$$
\therefore D_{port, final} = \sqrt{\frac{4 m_{fuel}}{\pi L \rho_{fuel}} + D_{port, init}^2}
$$

#### For a D-port

{% hint style="info" %}
Todo
{% endhint %}

`COMPUTE` Initial Regression Rate $$\dot r$$\[m/s\]

$$
\dot r = a G_{ox, max}^n L ^ m
$$

This number should be on the order of 0.5~3 milimeter per second, unless youve got some really awesome propellants. If you do, please let me know :D

### 8. Nozzle Sizing

Since we know the mass flow rate through the nozzle, we can determine the required throat area to choke the flow. 

`COMPUTE` Combustion chamber temperature, $$T_{cc}$$\[K\]

The static temperature \(very close to total temperature assuming the flow is slow\) in the combustion chamber needs to be estimated. I have not found a good method to do this, apart from assuming that we approach the flame temperature.

$$
T_{cc} \approx T_{flame}
$$

`COMPUTE` Characteristic Speed of the propellants \[m/s\]

This represents the combustion efficiency independent of nozzle performance.

$$
c^* = \frac{\sqrt{\gamma R T_{cc}}}{\eta_c \gamma \left(\frac{2}{\gamma+1}\right)^{\frac{\gamma+1}{2 \gamma-2}}}
$$

`COMPUTE` Throat Area $$A^* $$\[m^2\]

$$
A^* = \frac{\dot m_{prop}  c^*}{P_{cc}}
$$

`COMPUTE` The Mach number in the combustion chamber, $$M_{cc}$$ \[-\]

> Theory Aside:
>
> For a rocket to work, we need the gases within the combustion chamber to mix well. As such, we want the flow speed to be low, and usually ranges between M=0.1 ~ M=0.6, although 0.6 is really pushing it. SPAD suggests setting an upper bound at 0.2-0.4.
>
> In Roar, we compute this parameter assuming the port final diameter as a proxy for the post-combustion chamber diameter.

From isentropic flow equations, we have

$$
\frac{A_{cc}}{A^*} = \frac{1}{M_{cc}} \left(\frac{2}{\gamma+1} \left(1+\frac{\gamma-1}{2} M_{cc}^2\right)\right)^{\frac{\gamma+1}{2\gamma-2}}
$$

So now assuming A\_2 is the combustion chamber area, you can solve for the mach number. You will get two answers: one that is less than 1 and one that is greater than 1. 

The one that is less than one refers to the mach number in the combustion chamber.

`INPUT` Exit Pressure, $$P_e$$ \[Pa\]

Since we know that we want to expand the exiting gas ideally, this must be atmospheric pressure \(for our vehicles that are just getting off the ground. Not true for space rockets\)

`COMPUTE` Exit mach number $$M_e$$\[-\]

We compute the exit mach number using isentropic expansion theory,

$$
M_e^2 = \left(\frac{2}{\gamma-1}\right)\left(\left(\frac{P_{cc}}{P_{e}}\right)^{\frac{\gamma-1}{\gamma}} -1 \right)
$$

`COMPUTE` Exit Temperarte, $$T_e$$\[K\]

$$
T_e = T_{cc} \left(1 + \frac{\gamma-1}{2} M_e^2\right)^{-1}
$$

`COMPUTE` Required expansion ratio to acheive desired thrust, $$\epsilon$$ \[-\] and

`COMPUTE` Exit area, $$A_e$$\[m^2\]

$$
\epsilon = \frac{A_e}{A^*} = \frac{1}{M_e} \left[\left(\frac{2}{\gamma+1}\right) \left(1+\frac{\gamma-1}{2}M_e^2\right)\right]^{\frac{\gamma+1}{2\gamma-2}}
$$

### And thats it!

`RETURN` Everything

Now, we have a design for the rocket. All the key parameters are figured out, and now we need to check if the design will work for the specs that we want. To do this, we do a full time-domain simulation of the engine.

{% page-ref page="simulating-a-hybrid-engine.md" %}

















