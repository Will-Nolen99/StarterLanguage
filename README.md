# StarterLanguage
Basic custom Programming Language




# BNF Grammar

Program ::= {Feature} {Program} | {Feature}
Feature ::= {Function} | {Class}               class will not be implemented initially but I am keping here for now

             
Function ::= define {name} = {Function Declaration Sequence} -> { {Statement Sequence} } {return type}


Statement Sequence ::= {Statement} {Statement Sequence} | {Statement}
Declaration Sequence ::= {Declaration}, {Declaration Sequence} | {Declaration}
Statement ::= {Declaration Sequence} | {Assignment} | {If} | {While} | {Do while} | {For} | {Input} | {Output}
Declaration ::= {Type} {Name} | {Type} {Assignment}
Assignment ::= {Name} = {Expression}
Type ::= int | float | boolean | string | array


If ::= if {Expression} { {Statement Sequence} } | if {Expression} { {Statement Sequence} } else { {Statement Sequence} } | if {Expression} { {Statement Sequence} } else {If}

While ::= while expression { {Statement Sequence} }
Do While ::= do { {Statement Sequence} } while expression

For ::= for {Declaration Sequence} | {Expression} | {Expression} {{Statement Sequence}}

Expression ::= {term} | {expression} + {term} | {expression} - {term} | {creation}
term ::= {atom} | {term} * {atom} | {term} / {atom} | {term} % {atom} | term ~ {atom}                                      ~ is the floor after division operator 
atom ::= {var} | {atom} ^ {var}

var ::= {literal} | {name} | ( {expression} )

literal ::= {int} | {float} | {boolean} | {string} | {array}

int ::= some regular expression
float ::= some regular expression
boolean ::= true | false
string ::= " some regular expression surrounded in quotes "
array ::= [{array contents}]
array contents ::= {literal} | {literal}, {array contents}

creation ::= array[{num}]       used to make arrays of certain size. Can be changed to make different classes or structs in the future




Name ::= Some regular expression

