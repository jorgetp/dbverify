# DBVerify

**Will add the models soon!!!**

This repository contains [Tamarin](https://tamarin-prover.github.io/)-based symbolic models for a number of state-of-the-art **distance bounding protocols**. Those are cryptogrphic protocols that, in addition to authentication, are meant to guarantee physical proximity between the principals.

For further details see our **IEEE S\&P'18** paper [Distance-Bounding Protocols: Verification without Time and Location](https://drive.google.com/file/d/1VtMDUKLYr8BTgKy8aSjLG-UBS8VcKcuR/view).

## Folder layout
* ```msc```
  * ```proto1.pdf```: message sequence chart of protocol ```proto1```
  * ```proto2.pdf```: message sequence chart of protocol ```proto2```
  * ...
* ```model```
  * ```proto1.spthy```: Tamarin model of protocol ```proto1```
  * ```proto2.spthy```: Tamarin model of protocol ```proto2```
  * ...
  * ```proto1.proof```: the Tamarin proof for ```proto1.spthy```
  * ```proto2.proof```: the Tamarin proof for ```proto2.spthy```
  * ...
  * ```generic```: contains the generic Tamarin code, including the lemmas to be verified
  * ```Makefile```: the makefile to verify all protocols in this folder
  * ```collect.py```: a Python script to collect the results of the verification
  * ```results.html```: the ouput of the Python script

## How to DBVerify
Execute the ```Makefile``` which does the following:

1. The content of ```generic``` is written after the line ```//GENERIC CODE AFTER THIS LINE``` in each one of the ```.spthy``` files. *Be aware that this DOES overwrite whatever is thereafter*.
2. The Tamarin proof of each one of the files from step above is written into the corresponding ```.proof``` file.

## DBVerify your own protocol

You can code down your own Tamarin model for a given protocol. Take into account that this verification framework is generic and consequently for it to work, it must hold the following requirements:

* No protocol rule (other than those in ```generic```) models adversary actions, or the network, or long-term keys registering.
* Every **prover rule** is of the form
  ```
  [...]-[..., Action(P), ...]->[...]
  ```
  where ```P``` is the prover's name.
* Every **prover rule** that models a **sending event** is of the form
  ```
  [...]-[...]->[..., Send(P, m), ...]
  ```
  where ```P``` is the prover's name and ```m``` is the message being sent.
* Every **verifier rule** that models a **sending event during the fast phase** is of the form
   ```
   [...]-[..., Send(V, m), ...]->[...]
   ```
   where ```V``` is the verifier's name and ```m``` is the message being sent.
* Every **verifier rule** that models a **receive event during the fast phase** is of the form
   ```
   [..., Recv(V, m), ...]-[...]->[...]
   ```
   where ```V``` is the verifier's name and ```m``` is the message being received.
   
* Every **verifier rule** that models the claim **secure distance-bounding** is of the form
  ```
  DBSec(V, P, ch, rp)
  ```
  where ```V``` is the verifier's name, ```P``` is the prover's name who the claim is being made about, ```ch``` is the fast phase challenge, and ```rp``` is the fast phase response.

Once you have coded your protocol into, say, ```my_protocol.spthy```, add the line ```//GENERIC CODE AFTER THIS LINE``` right before ```end```. Then run ```Makefile``` which will put the proof in ```my_protocol.proof```.
