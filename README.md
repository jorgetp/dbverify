# DBVerify

This repository contains [Tamarin](https://tamarin-prover.github.io/)-based symbolic models for a number of state-of-the-art **distance bounding protocols**, which are cryptogrphic protocols that, in addition to authentication, are meant to guarantee physical proximity between the principals.

For further details see our **IEEE S\&P'18** paper [Distance-Bounding Protocols: Verification without Time and Location](https://drive.google.com/file/d/1VtMDUKLYr8BTgKy8aSjLG-UBS8VcKcuR/view).

## Folder layout
* ```msc```: contains the message sequence charts of the protocols
* ```model```: contains the Tamarin models (```.spthy``` files), their proofs (```.proof``` files), and
  * ```generic```: the generic Tamarin code (includes the security lemmas)
  * ```Makefile```: to verify all protocols in this folder
  * ```collect.py```: a Python script to collect the results of the verification
  * ```results.html```: the ouput of the Python script

## How to DBVerify
Execute the ```Makefile``` which does the following:

1. The content of ```generic``` is written right after the line ```//GENERIC CODE AFTER THIS LINE``` in each one of the ```.spthy``` files. *Be aware that this overrides whatever is thereafter!!!*.
2. The Tamarin proof of each one of the files from step above is written into the corresponding ```.proof``` file.

## DBVerify your own protocol

You can code down your own Tamarin model for a given protocol. Take into account that this verification framework is generic and consequently for it to work, the following requirements must be met:

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
   
* Every **verifier rule** that models a **secure distance-bounding** claim is of the form
  ```
  [...]-[..., DBSec(V, P, ch, rp), ...]->[...]
  ```
  where ```V``` is the verifier's name, ```P``` is the prover's name, ```ch``` is the challenge, and ```rp``` is the response.

Once you have coded your protocol, say into ```my_protocol.spthy```, add the line ```//GENERIC CODE AFTER THIS LINE``` right before ```end```. Then run ```Makefile``` which outputs the proof in ```my_protocol.proof```. Finally, run ```python collect.py``` to gather the results in ```results.html```. 

## Read the results

Each lemma in ```generic``` has a column in the table depicted in ```results.html```. To identify the type of attack(s), run Tamarin in interactive mode 
```
tamarin-prover interactive my_protocol.spthy
```
and inspect the trace that invalidates ```dbsec```.

Here a few hints:
* If lemma ```dbsec_on_honest_prover``` fails then there is a **mafia fraud**.
* If lemma ```dbsec_on_corrupt_prover``` fails then there is a **distance fraud**, or a **distance hijacking**, or both.

## On wellformedness warnings

The warnings reported here are due to equational theory of ```xor```.

## Contact

Should you have any inquiries, email me at ```jorgeXtoroYuniXlu``` (where ```X``` is dot and ```Y``` is at).


