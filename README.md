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

For the sake of presentation, we recommend you use 2-space width tabs in your editor.

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

To identify the type of attack(s), if any, against a protocol, say ```my_protocol.spthy```, here are 2 alternatives:

1. Run Tamarin in interactive mode 
  ```
  tamarin-prover interactive my_protocol.spthy
  ```
  and inspect the trace that invalidates ```dbsec```. Be aware that Tamarin gives you just one attack trace, so with this approach you might miss valid attacks.

2. Each lemma in ```generic``` has a column in the table depicted in ```results.html```. So, locate the entry for ```my_protocol.spthy``` and follow the (independent) observations:
  * If lemma ```dbsec``` holds then there's **no** attack.
  * If lemma ```dbsec_on_honest_prover``` fails then there is a *mafia fraud*.
  * If lemma ```dbsec_on_compromised_prover``` fails then there is a *distance fraud*, or a *distance hijacking*, or both.

## On exclusive-OR operations

Here's what we recommend you do to deal with exclusive-OR operations (and indeed the approach we took):

1. Define a function for modeling exclusive-OR, let's call it ```XOR```. Do not define any equational theory for it.

2. Run the verification. If lemma ```dbsec``` fails, then go to step 5. Otherwise, go to step 3.

3. If you have exhausted the equational theory for exclusive-OR go to step 4. Otherwise, add an equation into your set of equations for ```XOR``` and go to step 2.

4. The distance bounding protocol is **secure**.

5. The distance bounding protocol is **not secure** and thus an attack exists.

Alternatively, if you have a Tamarin version 1.4.0 or later (see [releases](https://github.com/tamarin-prover/tamarin-prover/releases)), you can use the built-in ```xor``` as to handle exclusive-OR with its equational theory. Be aware that this induces a substantial delay in the verification. We **did not** use such built-in to model the protocols of this repository.

## Contact

Should you have any inquiries, email me at ```jorgeXtoroYuniXlu``` (where ```X``` is dot and ```Y``` is at).


