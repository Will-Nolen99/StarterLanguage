# StarterLanguage
Basic custom Programming Language




# BNF Grammar

Program ::= {Feature} {Program} | {Feature}
Feature ::= {Function} | {Class}               class will not be implemented initially but I am keping here for now. Same with Struct. Some things are left in the Grammar but will not be implemented

             
Function ::= define {name} = {Function Declaration Sequence} -> { {Statement Sequence} } {return type}


Statement Sequence ::= {Statement} {Statement Sequence} | {Statement}
Declaration Sequence ::= {Declaration}, {Declaration Sequence} | {Declaration}
Statement ::= {Declaration Sequence} | {If} | {While} | {Do while} | {For} | {Input} | {Output}
Declaration ::= {Type} {Name} | {Type} {Assignment Expression}
Type ::= int | float | boolean | string | array


If ::= if {Expression} { {Statement Sequence} } | if {Expression} { {Statement Sequence} } else { {Statement Sequence} } | if {Expression} { {Statement Sequence} } else {If}

While ::= while expression { {Statement Sequence} }
Do While ::= do { {Statement Sequence} } while expression

For ::= for {Declaration Sequence} | {Expression} | {Expression} {{Statement Sequence}}


Expression = {Or} | {Assignment Expression}

Assignment Expression ::= {left} {Assignment Operator} {Resolve Expression} | {left} = {Array Creation}
left ::= {Struct Access} | {Aray Access} | {Name} 
Assignment Operator ::= = | *= | += | -= | \= | ~= | %= | ^= | :=     
Array Creation ::= Array[{int}]


Or ::= {And} | {Or} || {And}
And ::= {Equality} | {And} && {Equality}
Equality ::= {Relational} | {Equality} == {Relational} | {Equality} != {Relational}
Relational ::= {Additive} | {Relational} > {Additive} | {Relational} >= {Additive} | {Relational} < {Additive} | {Relational} <= {Additive} | {relational} isType {Type}
Additive ::= {Multiplicitive} | {Additive} + {Multiplicitive} | {Additive} - {Multiplicitive}
Multiplicitive ::= {Exponential} | {Multiplicitive} * {Exponential} | {Multiplicitive} / {Exponential} | {Multiplicitive} % {Exponential} | {Multiplicitive} ~ {Exponential}            ~ is the floor after division operator  returns int
Exponential ::= {unary} | {Exponential} ^ {unary} | {exponential} : {unary}    : is for nth root
Unary ::= {postfix} | ++{unary} | --{unary} |!{unary}
Postfix ::= {Term} | {Postfix}++ | {Postfix}--
Term ::= {literal} | ({Or}) | {Struct Access} | {Array Access} | {Function call} | {Name}           Class access and method invocation would occur here

Array Access ::= {name}[Or]


var ::= {literal} | {name} | ( {expression} )

literal ::= {int} | {float} | {boolean} | {string} | {array}


int ::= some regular expression
float ::= some regular expression       This will match and number with a decimal and value on the right of the decimal   1.2  .3 .34 0.11231  are all valid  1. 1 are not valid
boolean ::= true | false
string ::= " some regular expression surrounded in quotes "
array ::= [{array contents}]
array contents ::= {literal} | {literal}, {array contents}

creation ::= {type}[{num}]       used to make arrays of certain size. Can be changed to make different classes or structs in the future

Single line Comment = #
Multiline Comment = 
$

Hello world this is a multiline quote

$
 

Name ::= Some regular expression     Capital letters lowercase letters digits and underscore

