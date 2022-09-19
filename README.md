# Code test

The idea behind this problem represents a common situation when dealing with software dependencies.

When you want to install a software package, sometimes the package might have dependencies with other software packages. This means that, for that package to be installed, the dependencies also need to be installed. For example, you cannot install a printing software package if you do not have certain fonts packages installed. (But you can have those font packages installed without the printing package.)  If you want to select one software package, then all the dependencies have to also be selected.

In another case, you might want to install a package that is in conflict with another package installation. You cannot have both installed at the same time. If you try to install one, the packages that are in conflict should be uninstalled.

## Rule Sets

Let's say we have a set of packages which the user can select to install. Packages can be
related between them in two ways: one can depend on another, and two packages
can be mutually exclusive. That means that these equalities must always hold
true (note: this is not code, those are logical equations):

* "A depends on B", or "for A to be selected, B needs to be selected"
```
ruleSet.AddDep(A, B) =>
if isSelected(A) then isSelected(B)
```

* "A and B are exclusive",  or "B and A are exclusive",  or "for A to be
selected, B needs to be unselected; and for B to be selected, A needs to be
unselected"

```
ruleSet.AddConflict(A, B) <=> ruleSet.AddConflict(B, A) =>
if isSelected(A) then !isSelected(B) && if isSelected(B) then !isSelected(A)
```

We say that a set of relations are _coherent_ if the laws above are valid for
that set. For example, this set of relations is coherent: 

```
AddDep(A, B) // "A depends on B"
AddDep(B, C) // "B depends on C"
AddConflict(C, D) // "C and D are exclusive"
```

And these sets are _not_ coherent:

```
AddDep(A, B)
AddConflict(A, B)
```

A depends on B, so it's a contradiction that they are exclusive. If A is selected, then B would need to be selected, but that's impossible because, by the exclusion rule, both can't be selected at the same time. 

```
AddDep(A, B)
AddDep(B, C)
AddConflict(A, C)
```

The dependency relation is transitive; it's easy to see, from the rules above,
that if A depends on B, and B depends on C, then A also depends on C. So this
is a contradiction for the same reason as the previous case.

## Questions

A.

Write a data structure (`RuleSet`) for expressing these rules between packages,
ie. for defining a rule set.  You also need to define a constructor and 2
methods:

* `NewRuleSet()`: Returns an empty rule set.
* `RuleSet.AddDep(A, B)`: a method for rule sets that adds a new dependency A
  between and B.
* `RuleSet.AddConflict(A, B)`: a method for rule sets that add a new conflict
  between A and B.

B.

Implement the algorithm that checks that an instance of that **data structure is
coherent, that is, that no option can depend, directly or indirectly, on
another package and also be mutually exclusive with it.**

* `RuleSet.IsCoherent()`: a method for rule sets that returns true if it is a
  coherent rule set, false otherwise.

C.

Implement the algorithm that, given the rules between packages, a package, and a
collection of selected packages coherent with the rules, adds the package to a
collection of selected pacakges, or removes it from the collection if it is
already there, selecting and deselecting pacakges automatically based on
dependencies and exclusions.

* `New(rs)`: returns a new (empty) collection of selected packages (`Pkgs`) for
  the rule set rs.
* `Pkgs.Toggle(p)`: a method for a collection of selected packages, to set or
  unset package p.
* `Pkgs.StringSlice()`: returns a slice of string with the current list of
  selected packages.

The algorithm for when a checkbox is selected is asked to you in section C,
based on the data structures you define in section A. In section B you should
provide an algorithm that 'tests' that sections A and C give a good solution.


## Test

`python -m unittest discover`