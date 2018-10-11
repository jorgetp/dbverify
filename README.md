# DBVerify

This repository contains [Tamarin](https://tamarin-prover.github.io/)-based symbolic models for a number of state-of-the-art **distance bounding protocols**. Those are cryptogrphic protocols that, in addition to authentication, are meant to guarantee physical proximity between the principals.

For further details see our [IEEE S\&P'18](https://www.ieee-security.org/TC/SP2018/) paper [Distance-Bounding Protocols: Verification without Time and Location](https://drive.google.com/file/d/1VtMDUKLYr8BTgKy8aSjLG-UBS8VcKcuR/view).

**Will fill up the repo soon**

Find installation guide and other helpful information on Tamarin [manual](https://tamarin-prover.github.io/manual/).

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
Execute the ```makefile``` which does the following:

* The content of ```generic``` is written after the line ```//GENERIC CODE AFTER THIS LINE``` in each one of the ```.spthy``` files.
* For each one of the files ```proto.spthy``` resulting from step above the file ```proto.proof``` is created, which contains the Tamarin proof of ```proto.spthy```. This is done by using
  ```
  tamarin-prover --prove proto.spthy > proto.proof
  ```
## DBVerify your own protocol

You can write down your own Tamarin model for a given protocol. Take into account that this verification framework is meant to be generic and consequently the following requirements are to be met:

* No protocol rule (other than those in ```generic```) models adversary actions, or the network, or long-term keys registering.
* The verifier's claim fact is of the form ```DBSec(V, P, ch, rp)``` where ```V``` is the verifier's name, ```P``` is the prover's name who the claim is being made about, ```ch``` is the fast-phase challenge message, and ```rp``` is the fast-phase response message.
* Every prover rule is of the form
  ```
  [...]-[..., Action(P), ...]->[...]
  ```
  where ```P``` is the prover's name.
* Every prover rule that models a sending event is of the form
  ```
  [...]-[...]->[..., Send(P, m), ...]
  ```
  where ```P``` is the prover's name and ```m``` is the message being sent.
* Every verifier rule that models a sending event during the fast phase is of the form
   ```
   [...]-[..., Send(V, m), ...]->[..., Send(V, m), ...]
   ```
   where ```V``` is the verifier's name and ```m``` is the message being sent.
* Every verifier rule that models a receive event during the fast phase must be of the form
   ```
   [..., Recv(V, m), ...]-[...]->[...]
   ```
   where ```V``` is the verifier's name and ```m``` is the message being received.
   
Once you have coded your protocol into ```myprotocol.spthy```, add the line ```//GENERIC CODE AFTER THIS LINE``` right before ```end```. Then run ```Makefile``` which will put the proof in ```myprotocol.proof```.
