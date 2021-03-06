---
description: Start here
---

# Introduction

![Roar is a set of python files to aid in sizing and simulating a hybrid rocket engine.](.gitbook/assets/roar.png)



## Roar?

`Roar` is my latest update to a hybrid engine design code, moving from MATLAB to Python. And to provide \(much\) better documentation on how it works.

### It allows you to:

\(given the performance targets of an engine\)

* perform an initial sizing for an engine \(ie. give you a decent guess on how big/heavy etc your engine needs to be\)
* analyse the expected performance of an engine, running a full time-domain simuation. 

### What it does not do:

* build an engine. Thats your job
* guarantee that it works - if you 'accidentally' use a diameter instead of a radius \(or vice versa\) it _will_ give you an answer, but the answer will not work in real life - use your brain, use your engineering judgement.
* make the right assumptions - I've put in the best assumptions that I had available when I wrote the code. Please update the code to make it better. 

{% hint style="success" %}
The primary objective of this code is to be a guide to sizing an engine, as its a rather involved process. It is not meant to be a single source of truth.
{% endhint %}

This entire project is based on "Space Propulsion Analysis and Design" \[SPAD\] by Ronald Humble.



Documentation: [https://devanshinspace.gitbook.io/roar/](https://devanshinspace.gitbook.io/roar/)

Github Repo: [https://github.com/icl-rocketry/roar](https://github.com/icl-rocketry/roar)

Enjoy,  
Dev



## Get Started:

Read Background on Hybrids

{% page-ref page="hybrid-engines/background-on-hybrids.md" %}

Get into the code! 

{% page-ref page="code-walkthrough/getting-started.md" %}

I assume a basic understanding of python, but not much more. The level of physics/thermo background needed is also low to use the tool, but not insignificant to develop new models.

## How to make it better:

\(This is a scratchpad of features to add\)

* [ ] better mathematical/thermo models for hybrid
  * [ ] better nitrous modelling.
* [ ] a module to integrate experimental test results

