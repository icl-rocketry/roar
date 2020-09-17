# Time-Based Simulation

So we have just found the specs of a rocket engine. Now we must check that its reasonable, and that it meets our main goals. To do this, we perform a time-based simulation, ie we step through from the start to the end, making more reasonable assumptions. 

### Outline

1. Set up the simulation \(ie load parameters etc\)
2. Determine $$\dot{r}$$ and total mass flow throught the engine \(assuming some oxidiser mass flow\)
3. Use thermochemistry to estimate the temperature and pressure inside the combustion chamber
4. Use flow equations to determine the nozzle flow and the exit mach numbers
5. Estimate force, $$I_{sp}$$
6. Update the geometry to account for burnt fuel
7. Check if rocket has finished burning. If it has, save and exit. If not, step forward in time and return to step 2.

This is solved using a super-basic Netwon-Euler method, ie we just take fixed steps forward in time and update everything, instead of using something like `scipy.solve_ivp`. This should make it easier to understand, hack into and develop. It also gets around the need to write the differential equations explicitly :D





### Step 2

We previously assumed that the regression rate is given by 

$$
\dot{r} = a G_{ox}^n L^m
$$

But now, we want to have \(the probably more accurate\)

$$
\dot r = a G_{prop}^n L ^m
$$

but this introduces a problem:

$$
G_{prop} = G_{ox} + G_{fuel} = G_{ox} + \frac{\dot{m}_{fuel}}{A_{port}} =  G_{ox} + \frac{\rho_{fuel} \dot{r} A_{port}  L}{A_{port}}
$$

$$
\therefore G_{prop} = G_{ox} + \rho_{fuel}   L ( a  G_{prop}^n L^m)
$$

which means that the total propellant mass flux depends on itself. ugh. To solve this problem, we must numerically solve for G\_prop, and using Scipy this isnt difficult. We use `scipy.optimize.root` to find this root. 

### Step 3

Something similar happens with the thermochemistry

$$
OF = \frac{\dot{m}_{ox}}{\dot{m}_{fuel}}
$$

we assume the stagnation temperature inside the combustion chamber is close to the flame temperature \(WHICH IS LIKELY A POOR ASSUMPTION, I just dont know how to fix it\)

then the pressure in the combusion chamber, for choked flow is 

$$
P_{cc} = \frac{\dot{m}_{prop} c^*}{A_{throat}}
$$

where $$c^*$$is the characteristic speed of the propellants chosen, but

$$
c^* = c^* (P_{cc})
$$

is some non-linear function of the combustion chamber pressure. We need this data, and we get it from sources like PROPEP. 

To find $$c^*$$, we need to load data, and we perform a 2D interpolation \(using `scipy.interpolate.interp2d`\)

$$
T_{flame} = T_{flame} (P_{cc}, OF)\\
\gamma =\gamma (P_{cc}, OF)\\
\mathcal{M} = \mathcal{M}(P_{cc}, OF)\\
R = 8.314/\mathcal{M}
$$

where $$\mathcal{M}$$is the molecular mass of the gas, kg/mol, and R is the specific gas constant. The 8.314 is the universal gas constant. Now we can solve for $$c^*$$

$$
c^* = \eta_c \frac{\sqrt{\gamma R T_{flame}}}{\left(\gamma\left(\frac{2}{\gamma+1}\right)^{(\gamma+1)/(2\gamma-2)}\right)}
$$

\[SPAD eq 7.71\] where $$\eta_c$$is the combustion efficiency, usually 0.95 according to SPAD.

Richard Nakka has an example: [http://www.nakka-rocketry.net/techs.html](http://www.nakka-rocketry.net/techs.html)

So, we perform a second root finding, this time trying to find the $$P_{cc}$$ that is consistent with the above formulae. 

{% hint style="danger" %}
The default data in roar is for some a fuel and oxidiser, but I cant remember which ones I had used!! I would recommend gathering the data from PROPEP again. 
{% endhint %}

{% hint style="warning" %}
Note, we have just assumed that the pressure has become high enough for it to choked. This isnt true when the rocket is about to fire! I dont know how to fix this issue, unless we pay much closer attention to the startup of the engine. This also makes it clear that for the rocket to work, we need both high heat \(to vapourise the solid fuel\) and enough gas pressure to cause a choke as early as possible in the firing. 
{% endhint %}

{% hint style="info" %}
Fun fact - one of the significant delays we experienced was that the US Government was shut down - this made RPOPEP unavailable for that duration, and it stalled us. I would recommend collecting and saving the data whenever possible. 
{% endhint %}

### Step 4





 





















