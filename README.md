# DBVerify

This repository contains a set of [Tamarin](https://tamarin-prover.github.io) models and (in)security proofs of a number of distance-bounding protocols. The verification accounts for the sophisiticated *terrorist fraud* attack by reasoning on *post-collusion security*.

This is the complementary material for our papers *Distance-Bounding Protocols: Verification without Time and Location*, published at [S&P'18](https://www.ieee-security.org/TC/SP2018/), and *Post-Collusion Security and Distance Bounding*, to be published at [CCS'19](https://www.sigsac.org/ccs/CCS2019/). If you were directed here because of the first paper, simply ignore the lemmas `dbsec_hnst_collusion` and `dbsec_hnst_star` as they're to do with post-collusion security and terrorist fraud.

For the sake of presentation, we recommend you use **2**-space tab indent in your editor when viewing our Tamarin code.

## Folder layout
* [/msc/](/msc/) contains
  * `*.pdf` files which are the *message sequence chart* representations of the protocols
* [/tamarin/](/tamarin/) contains
  * `*.spthy` files which are the Tamarin models
  * `*.proof` files which are Tamarin proofs
  * `*.flag` files which are the \[optional\] Tamarin verification flags
  * `generic.txt` which contains the generic Tamarin code
  * `Makefile` to verify all protocols in this folder
  * `collect.py` which is a Python script to collect the results of the verification
  * `results.html` which is the ouput of the Python script
* [/xtras/](/xtras/) contains the folders
  * [/toy/](/xtras/toy/) contains Tamarin model for the `Toy` protocol
  * [/chothia/](/xtras/chothia/) contains the ProVerif models and proofs of some protocols, as per Chothia et al.'s [framework](http://www.cs.bham.ac.uk/~tpc/distance-bounding-protocols/)

## How to verify

Follow the steps:

1. Open a terminal at [/tamarin/](/tamarin/).

1. Run `make` which does the following, for each outdated target `protocol.proof`:
   * Writes the content of `generic.txt` into `protocol.spthy` right after the line `//GENERIC CODE AFTER THIS LINE`. **WARNING: this overrides whatever is thereafter!!!**
   * Runs
     ```
     tamarin-prover FLAGS protocol.spthy --prove
     ```
     where `FLAGS` are the Tamarin execution flags located in `protocol.flag` if this file exists, or `FLAGS` equals the empty string otherwise. This can be used for Tamarin heuritics or oracles. See e.g. `SwissKnife.flag`.
   * Writes the Tamarin proof along with the verfication time in `protocol.proof`.

1. Run `python collect.py` to gather the results in `results.html`.

## Read the results

Each `.proof` file has a row in `results.html`. The columns are composed of the lemmas `generic.txt`, the (individual) lemmas in the `*.spthy` files, the number of lines of Tamarin code `LoC`, and the verification time `Time`. This last one corresponds to the **real** time as per the Unix-command `time`.

To identify the type of attack(s), if any, against a given protocol, locate the protocol's entry in the table and follow the hints:
  * If lemma `dbsec_hnst` fails, then a **mafia fraud** exists.
  * If lemma `dbsec_hnst` holds and `dbsec` does not, then a **distance fraud** and/or a **distance hijacking** attack exist \* (trace inspection is recommended, details in step 6 later on).
  * If lemma `dbsec_hnst_collusion` fails and `dbsec_hnst_star` holds, then a **terrorist fraud** exists.

Alternatively, you can run Tamarin in interactive mode
```
tamarin-prover interactive protocol.spthy
```
and inspect the trace that falsifies the desired lemma (`dbsec` is recommended). *Be aware that Tamarin gives you the first attack trace it finds, thus this might not be the only attack*.

## Verify your own protocol

Follow the steps:

1. Code down the Tamarin model for your protocol, say into `protocol.spthy` (inside the folder [/tamarin/](/tamarin/)). Your model must meet the following requirements:
   * No protocol rule, other than those in `generic.txt`, models adversary actions, or the network, or long-term key registering.
   * Every **transmission** of a message `msg` by a prover `P` is modeled with a rule of the form
     ```
     [...]-[...]->[..., Send(P, msg), ...]
     ```
   * Every **transmission** of a message `msg` by a verifier `V`, during the **fast phase**, is modeled with a rule of the form
     ```
     [...]-[..., Send(V, msg), ...]->[ ... ]
     ```
   * Every **reception** of a message `msg` by a verifier `V`, during the **fast phase**, is modeled with a rule of the form
     ```
     [..., Recv(V, msg), ...]-[...]->[...]
     ```
   * Every **secure distance-bounding** claim by a verifier `V` about a prover `P` for a fast phase delimited by the challenge `chal` and the response `resp` is modeled with a rule of the form
     ```
     [...]-[..., DBSec(V, P, chal, resp), ...]->[...]
     ```
1. Add the line `//GENERIC CODE AFTER THIS LINE` into `protocol.spthy` right before the keyword `end`.

1. Open a terminal at [/tamarin/](/tamarin/).

1. Run `make`.

1. Run `python collect.py` to gather the results in `results.html`.

1. \*Inspect the trace that falsifies the `dbsec` lemma, if any, in order to confirm the attack, specially if it's about distance hijacking. This inspection is required for *uncommon* protocols in which the aforementioned requirements in step 1 are not sufficient to label every adversary action with an `Action` fact.

## Contact

Should you have any inquiries on the Tamarin stuff or should you want to report bugs, please [contact me](https://jorgetp.github.io/contact/). For ProVerif stuff please contact [Zach Smith](https://satoss.uni.lu/members/zach/).

## Acknowledgment

This work was supported by Luxembourg [FNR](https://www.fnr.lu/)'s grant **AFR-PhD-10188265**. Also, thanks to [S. Delaune](https://people.irisa.fr/Stephanie.Delaune/) and [A. Debant](http://people.irisa.fr/Alexandre.Debant/) for providing us with interesting protocols, which led to the step 6 above about the need for trace inspection.
