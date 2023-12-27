This page shows the work of 
[Dunne et al., 2015](https://doi.org/10.1016/j.artint.2015.07.006
"Dunne, P. E., Dvořák, W., Linsbichler, T., & Woltran, S. (2015). 
Characteristics of multiple viewpoints in abstract argumentation. 
Artificial Intelligence, 228, 153-178.") on _realisability_: given a set of 
sets $S$ and some semantics, does any argumentation framework $\textit{AF}$ 
exist such that the extensions of $\textit{AF}$ are exactly $S$?
The answer to this question is dependent on the properties of $S$, that is, 
whether $S$ is tight, conflict-sensitive, downward-closed, incomparable, 
DCL-tight, containing an empty set, nonempty and/or unary.

If you generate a set of argument sets (i.e. extensions) in the textbox, 
the algorithms in PyArg will automatically compute which properties apply 
to $S$. The result is shown in the table. In this table, one can also see 
which properties are required for specific semantics. For those semantics 
for which all properties are fulfilled, the "Generate" button is activated. 
By pressing this button, an argumentation framework $\textit{AF}$ is generated 
and visualised on the right. The extensions of $\textit{AF}$ are exactly the 
sets that were specified in the text box.