(* Razonamiento automatizado 2020-2
   Alumnas: Ibarra Moreno Gisselle y 
   Sánchez Salgado Alma Rocío
   Tarea 4, Tácticas básicas y negación clásica*)


Variables p q r s t x l m:Prop.
Variables U:Type.
Variables P Q: U -> Prop.
Variables R : U -> U -> Prop.
Variables a b : U.


Section LPyLPO.

Theorem DilemaC : (p -> q) -> (r -> s)-> p \/ r -> q \/ s.
Proof.
intros.
destruct H1.
left.
apply(H H1).
right.
apply(H0 H1).
Qed.

Theorem Distrib : p \/ (q  /\ r)->(p \/ q) /\ (p \/ r).
Proof.
intros.
destruct H.
split.
left.
assumption.
left.
assumption.
split.
destruct H.
right.
assumption.
destruct H.
right.
assumption.
Qed.

Theorem Argumento1: ((x \/ p) /\ q -> l) /\
                    (m \/ q -> s /\ t) /\
                    ((s /\ t) /\ l -> x) /\
                    (p -> q) ->
                    (m /\ p -> x).
Proof.
intros.
destruct H.
destruct H1.
destruct H2.
apply H2.
split.
apply H1.
destruct H0.
left.
assumption.
apply H.
split.
destruct H0.
right.
assumption.
apply H3.
destruct H0.
assumption.
Qed.

Theorem Socrates: (forall x:U, P x -> Q x) /\ P a -> Q a.
Proof.
intro.
destruct H.
apply H.
assumption.
Qed.

Theorem DistrExistsConj: (exists x:U, P x /\ Q x) -> (exists x:U, P x) /\ (exists x:U, Q x).
Proof.
intro.
split.
destruct H.
destruct H.
exists x0.
assumption.
destruct H.
exists x0.
destruct H.
assumption.
Qed.

Theorem Argumento2: (forall y:U, P y -> Q y) -> (forall x:U, (exists y:U, P y /\ R x y) -> exists z:U, Q z /\ R x z).
Proof.
intros.
destruct H0.
destruct H0.
exists x1.
split.
apply H.
assumption.
assumption.
Qed.

End LPyLPO.


Section LogConst.
Require Import Classical.

Parameters (u v C:Prop)
           (A: Set)
           (i z:A)
           (S: A -> Prop).


Check classic.

Check classic u.

Check classic (u\/v).

Check NNPP.

Check NNPP v.

Check NNPP (u -> v).


Theorem NegImp: (p -> q) -> (p -> ~q) -> ~p.
Proof.
intros.
contradict H0.
unfold not.
intros.
destruct H1.
assumption.
apply (H H0).
Qed.

Theorem nonoTExc: ~~(p \/ ~p).
Proof.
unfold not.
intros.
apply H.
exact (classic p).
Qed.

Theorem dmorganO : ~ ( p \/ q ) <-> ~p /\ ~q.
Proof.
unfold iff.
split.
unfold not.
intros.
split.
intros.
apply H.
left.
assumption.
intro.
apply H.
right.
assumption.
intros.
unfold not.
intros.
destruct H.
destruct H0.
contradiction.
contradiction.
Qed.

Theorem Argumento3: (forall x:U, P x -> Q x) /\
              (~ exists x:U, P x /\ Q x) ->
              ~ exists x:U, P x.
Proof.
intros.
destruct H.
unfold not.
contradict H0.
destruct H0.


