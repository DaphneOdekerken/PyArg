#### Abstract argumentation framework
An abstract argumentation framework (AF) is a directed graph in which the 
arguments are represented by the nodes and the attack relation is 
represented by the arrows. Formally, an argumentation framework is a pair 
$\langle \mathcal{A}, \mathcal{C} \rangle$ in which $\mathcal{A}$ is a finite 
set of arguments and $\mathcal{C} \subseteq \mathcal{A} \times \mathcal{A}$.

We say that an argument $a \in \mathcal{A}$ _attacks_ an argument $b \in 
\mathcal{B}$ iff $(a, b) \in \mathcal{C}$. 

In order to identify the outcomes of the conflict that is encoded by an 
abstract argumentation framework, one can use some formal method called 
_argumentation semantics_. We here discuss the extension-based approach, 
where the idea is to identify sets of arguments (called _extensions_) that 
represent reasonable positions that an autonomous reasoner may take. In the 
next section we describe various semantics and the reasoners that PyArg 
uses to compute them.

For more information on abstract argumentation frameworks, we refer to [
(Dung, 1995)](https://doi.org/10.1016/0004-3702(94)00041-X "Dung, Phan Minh.
"On the acceptability of arguments and its fundamental role in nonmonotonic 
reasoning, logic programming and n-person games." Artificial intelligence 
77.2 (1995): 321-357.").

#### Evaluation: semantics and reasoners
In this section, we give an overview of the semantics and the reasoners 
that were implemented to compute them. For more information about these 
examples, we refer to [Chapter 4 of the Handbook of Formal Argumentation](
https://www.collegepublications.co.uk/downloads/handbooks00003.pdf).

In the visualisation, all arguments belonging to the extension are coloured 
green (or blue if one uses the color-blind friendly mode). The arguments 
that are attacked by those arguments are coloured red and all other 
arguments are yellow.

##### Conflict-free
Let $\textit{AF} = \langle \mathcal{A}, \mathcal{C} \rangle$ be an 
argumentation framework and let $A \subseteq \mathcal{A}$. The set $A$ is 
conflict-free iff there are no $a$ and $b$ in $A$ such that $a$ attacks $b$.

For computing the conflict-free extensions, we use a recursive procedure.

##### Admissible
Let $\textit{AF} = \langle \mathcal{A}, \mathcal{C} \rangle$ be an 
argumentation framework and let $A \subseteq \mathcal{A}$. The set $A$ 
_defends_ $a \in \mathcal{A}$ iff for each $b$ that attacks $a$, there is 
some $c$ in $A$ such that $c$ attacks $b$.

A set $A \subseteq{\mathcal{A}}$ is called an _admissible set_ iff $A$ is 
conflict-free and each $a$ in $A$ is defended by $A$.

For computing all admissible sets, we adapted the recursive algorithm
("Algorithm 1" for preferred semantics) from 
[(Nofal et al. 2014)](https://doi.org/10.1016/j.artint.2013.11.001
"Samer Nofal, Katie Atkinson, and Paul E. Dunne. "Algorithms for decision 
problems in argument systems under preferred semantics." Artificial 
Intelligence 207 (2014): 23-51.").

##### Naive
Let $\textit{AF} = \langle \mathcal{A}, \mathcal{C} \rangle$ be an 
argumentation framework and let $A \subseteq \mathcal{A}$. The set $A$ is 
called a _naive_ extension iff $A$ is a maximal conflict-free set.

For computing the naive extensions, we first compute all conflict-free 
extensions and then only select those extensions for which no superset is 
also conflict-free.

##### Complete
Let $\textit{AF} = \langle \mathcal{A}, \mathcal{C} \rangle$ be an 
argumentation framework and let $A \subseteq \mathcal{A}$. The set $A$ is 
called a _complete_ extension iff $A$ is conflict-free and $A$ is exactly 
the set defending $A$.

The algorithm used for computing the complete extensions is adapted from 
the recursive algorithm ("Algorithm 1" for preferred semantics) from 
[(Nofal et al. 2014)](https://doi.org/10.1016/j.artint.2013.11.001
"Samer Nofal, Katie Atkinson, and Paul E. Dunne. "Algorithms for decision 
problems in argument systems under preferred semantics." Artificial 
Intelligence 207 (2014): 23-51.").
The adjustment is based on Definition 3 from 
[(Modgil and Caminada, 2009)](http://dx.doi.org/10.1007/978-0-387-98197-0_6 
"Sanjay Modgil and Martin Caminada.
"Proof Theories and Algorithms for Abstract Argumentation Frameworks." In
Argumentation in Artificial Intelligence (2009): 105-132")

##### Grounded
Let $\textit{AF} = \langle \mathcal{A}, \mathcal{C} \rangle$ be an 
argumentation framework and let $A \subseteq \mathcal{A}$. The set $A$ is 
the _grounded_ extension of $\textit{AF}$ iff $A$ is a minimal (w.r.t. set 
inclusion) complete extension of $\textit{AF}$.
This is the same as the smallest fixed point of $F_{\textit{AF}}$, the 
_characteristic function_ which is defined as 
$F_{\textit{AF}}(S) = \{ s \in \mathcal{A} | S \text{ defends } s \}$.

Following this definition, we compute the grounded extension by iteratively 
applying the characteristic function until a fixed point is reached.

##### Preferred
Let $\textit{AF} = \langle \mathcal{A}, \mathcal{C} \rangle$ be an 
argumentation framework and let $A \subseteq \mathcal{A}$. The set $A$ is 
a _preferred_ extension of $\textit{AF}$ iff $A$ is a maximal (w.r.t. set 
inclusion) complete extension of $\textit{AF}$.

For computing all preferred extensions, we implemented the recursive algorithm
("Algorithm 1" for preferred semantics) from 
[(Nofal et al. 2014)](https://doi.org/10.1016/j.artint.2013.11.001
"Samer Nofal, Katie Atkinson, and Paul E. Dunne. "Algorithms for decision 
problems in argument systems under preferred semantics." Artificial 
Intelligence 207 (2014): 23-51.").

##### Stable
Let $\textit{AF} = \langle \mathcal{A}, \mathcal{C} \rangle$ be an 
argumentation framework and let $A \subseteq \mathcal{A}$.
A _stable_ extension of $\textit{AF}$ is a conflict-free set $A$ such that 
$A \cup \{b \in \mathcal{A} \mid \text{some } a \in A \text{ attacks } b\} 
= \mathcal{A}$.

The algorithm used for computing the stable extensions is adapted from 
the recursive algorithm ("Algorithm 1" for preferred semantics) from 
[(Nofal et al. 2014)](https://doi.org/10.1016/j.artint.2013.11.001
"Samer Nofal, Katie Atkinson, and Paul E. Dunne. "Algorithms for decision 
problems in argument systems under preferred semantics." Artificial 
Intelligence 207 (2014): 23-51.").
The adjustment is based on Definition 4 from 
[(Modgil and Caminada, 2009)](http://dx.doi.org/10.1007/978-0-387-98197-0_6 
"Sanjay Modgil and Martin Caminada.
"Proof Theories and Algorithms for Abstract Argumentation Frameworks." In
Argumentation in Artificial Intelligence (2009): 105-132").

##### Semi-stable
Let $\textit{AF} = \langle \mathcal{A}, \mathcal{C} \rangle$ be an 
argumentation framework and let $A \subseteq \mathcal{A}$. A _semi-stable_ 
extension of $\textit{AF}$ is a complete extension $A$ where 
$A \cup \{b \in \mathcal{A} \mid \text{some } a \in A \text{ attacks } b\}$ is 
minimal (w.r.t. set inclusion) among all complete extensions.

We implemented the algorithm from Section 6 in 
[(Modgil and Caminada, 2009)](http://dx.doi.org/10.1007/978-0-387-98197-0_6 
"Sanjay Modgil and Martin Caminada.
"Proof Theories and Algorithms for Abstract Argumentation Frameworks." In
Argumentation in Artificial Intelligence (2009): 105-132").

##### Ideal
Let $\textit{AF} = \langle \mathcal{A}, \mathcal{C} \rangle$ be an 
argumentation framework and let $A \subseteq \mathcal{A}$.
An admissible set is called _ideal_ iff it is a subset of each preferred 
extension. The ideal extension is of $\textit{AF}$ is a maximal (w.r.t. set 
inclusion) ideal set.

We compute the ideal extension by first computing the admissible and 
preferred extensions as described above, and then finding the maximal ideal 
set, quite literally applying the definition.

##### Eager
Let $\textit{AF} = \langle \mathcal{A}, \mathcal{C} \rangle$ be an 
argumentation framework and let $A \subseteq \mathcal{A}$.
The eager extension is of $\textit{AF}$ is the maximal (w.r.t. set 
inclusion) admissible set that is included in every semi-stable extension.

We compute the ideal extension by first computing the admissible and 
semi-stable extensions as described above, and then finding the maximal ideal 
set, again literally applying the definition.
