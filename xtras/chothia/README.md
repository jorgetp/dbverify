# Introduction

These files contains ProVerif implementations of
various distance bounding protocols, as per the
model of Chothia et al. in their USENIX 2018 paper:

https://www.usenix.org/system/files/conference/usenixsecurity18/sec18-chothia.pdf

The intent of these implementations is to demonstrate
some inconsistencies between the results of their paper
and accepted definitions regarding the security of various
protocols.

# Organisation

The files are split into three main folders. The `uncompiled` folder contains files created in an extension of the ProVerif language. These files are the input to the checkDB tool created in the above mentioned paper.

In order to analyse a protocol, a different compiled file must be made for each individual security property. This is done by commenting in/out specific segments.

The `output` folder contains the results of running the files in the `uncompiled` folder through the checkDB tool. For convenience, the python script `MassCompileCheckDB.py` (runs in Linux) will perform this process for you if `checkdb` is in the same folder.

Finally, the `distance-hijacking` folder contains a toy implementation demonstrating that the checkdb tool struggles with identifying distance hijacking attacks without some help. This is discussed later here.

A readme can be found in the checkDB repository

Note that the files here for 'CRCS', 'hk_perf',
'mad' and 'meadows' correspond to the (uncompiled) versions
given in the original checkDB repository.
The compiled versions are not given in
their original repository. Note that the Hancke-Kuhn protocol
was renamed - an explanation follows.

# Terrorist Fraud

The paper erroneously reports that the HK protocol admits
no terrorist fraud attack. This could be for several reasons.
The first is that the HK protocol is improperly modeled:
in the original paper of this protocol, the challenge response
is built using a PRNG generated from the nonces exchanged
in the initialization phase. This means that it can be generated
(and thus leaked) before the challenge phase begins. We model
this using the hk_imperf files.

We note that the definition of terrorist fraud given in our paper also differs from that of Chothia et al., which could lead to inconsistencies when analysing other protocols. This is because our definition of terrorist fraud considers **non-repeatability** as a required component - a one-time collusion must lead to a one-time attack. In comparison, Chothia et al. report that a protocol admits an attack if collusion is possible at all. We discuss this in more detail in our paper.

We modelled the dbToy paper following the instructions given in the paper.
The checkDB tool differs in our judgement in that it reports a terrorist
fraud attack exists.

# Distance Hijacking

The paper of Chothia et al. includes definition for many classes of attack on distance bounding protocols, including distance hijacking. However, their implementation of the checkDB tool does not include an implementation of distance hijacking attacks.

As a result, their paper implies that the MAD and Meadows protocols do not admit non-terrorist fraud attacks. However, there exist known distance hijacking attacks on both of these protocols.

In the `distance-hijacking` folder, we attempt to naively add distance hijacking to the checkDB tool by adding a new test process, applying it to the toy protocol "bc-symm". bc-symm can be described in Alice and Bob notation as:


```
P -> V: h(m)

V -> P: c

P -> V: g(c, m)

P -> V: m, senc(m, k_pv)
```

This is a simple variant on the famous Brands-Chaum protocol. The fast phase consists of the middle 2 messages. We attempt to model this by adding the test process:

```process
  [ !Verifier | (new id2; let idP = id2 in !Prover) ]
| [ !(new id; let idP = id in !DishonestProver) ]

```

, which models a local prover and a dishonest prover. The compiled output can be found in

`bc-symm-dh-df-out.pi`. Note that we must compile in no-local-adversary mode.

Running Proverif on the output file reports no attack. However, we claim that there is one. An attacker can intercept the last message from the prover to the verifier, read off `m`, and then re-encrypt the message before sending to the verifier.

We provide also the file `bc-symm-dh-df-handwritten`. The intent of this handwritten version is to demonstrate that ProVerif is capable of finding distance hijacking attacks. In the file, we manually make changes to the compiled output as follows:

* Add some formatting
* Delete many unneeded processes (in this case, since we know the cause of the attack, we can identify the minimal processes needed to indicate it)
* Change the specification of the local honest prover so that the commit unwrapper message (4) is sent on the channel `c` instead of `priv`. CheckDB fails to correctly produce a prover process which satisfies this.
* Change the specification of the overall process, so that the verifier only confirms sessions if they come from the dishonest remote prover. This prevents ProVerif from reporting some trivial attacks consisting of purely honest sessions that are introduced from the previous step.

We discuss some of the reasoning more in Appendix B of our paper. The handwritten ProVerif file correctly reports the attack.