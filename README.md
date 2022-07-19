# StarterLanguage
Basic custom Programming Language




# BNF Grammar

Program ::= {Feature List} -
Feature List ::= {Feature} {Feature List} | {Feature}
Feature ::= {Function} | {Class}               class will not be implemented initially but I am keping here for now. Same with Struct. Some things are left in the Grammar but will not be implemented

             
Function ::= define {name} = {Function Declaration Sequence} -> { {Statement Sequence} } -> {return type}    -p

Function Declaration Sequence ::= {Function Declaration}, {Function Declaration Sequnce} | { Function Declaration}    -p
Statement Sequence ::= {Statement} {Statement Sequence} | {Statement}   -p
Declaration Sequence ::= {Declaration}, {Declaration Sequence} | {Declaration}   -p
Statement ::= {Declaration Sequence} | {Expression} | {If} | {While} | {Do while} | {For} | {Input} | {Output} | {return}    -p
Declaration ::= {Type} {Name} | {Type} {Name} = {Or} -p
Function Declaration ::= {Type} {Name}   -p
Type ::= int | float | boolean | string | array    # I am just doing this in place when needed instead of making it a non-terminal

Return := return {name} | return {Expression}

If ::= if {Expression} { {Statement Sequence} } | if {Expression} { {Statement Sequence} } else { {Statement Sequence} } | if {Expression} { {Statement Sequence} } else {If}      -

While ::= while {expression} { {Statement Sequence} }      -
Do While ::= do { {Statement Sequence} } while {expression}       -

For ::= for {Declaration Sequence} | {Expression} | {Expression} {{Statement Sequence}}      - 


Expression = {Or} | {Assignment}      - 

Assignment ::= let {left} {Assignment Operator} {Or} -
left ::= {Struct Access} | {Aray Access} | {Name} -
Assignment Operator ::= = | *= | += | -= | \= | ~= | %= | ^= | :=     -
Array Creation ::= Array[{int}]-


Or ::= {And} | {And} || {Or}         -
And ::= {Equality} | {Equality} && {And}     -
Equality ::= {Relational} | {Relational} == {Equality}   | {Relational} != {Equality} 
Relational ::= {Additive} | {Additive} > {Relational} | {Additive} >= {Relational} | {Additive} < {Relational} | {Additive} <= {Relational} 
Additive ::= {Multiplicitive} | {Multiplicitive} + {Additive} | {Multiplicitive} - {Additive}
Multiplicitive ::= {Exponential} | {Exponential} * {Multiplicitive} | {Exponential} / {Multiplicitive} |  {Exponential} % {Multiplicitive} | {Exponential} ~ {Multiplicitive}            ~ is the floor after division operator  returns int
Exponential ::= {unary} | {unary} ^ {Exponential} | {unary} : {exponential}    : is for nth root
Unary ::= {postfix} | ++{unary} | --{unary} |!{unary}                         # This is currently causing a bug I think it is fixed but I will leave this here as a not. The symbols in front were not recognized when using one token look ahead for expressions

Postfix ::= {Term} | {Term}++ | {Term}--    This will need to have a runtime check for the type of term that is a child
Term ::= {literal} | ({Or}) | {var} -

Array Access ::= {name}[Or]


var ::= {Struct Access} | {Array Access} | {Function call} | {Name}     -  to find type of access read in name first then look to see next symbol     Class access 

literal ::= {int} | {float} | {boolean} | {string} | {array}     -


int ::= some regular expression
float ::= some regular expression       This will match and number with a decimal and value on the right of the decimal   1.2  .3 .34 0.11231  are all valid  1. 1 are not valid
boolean ::= true | false
string ::= " some regular expression surrounded in quotes "
array ::= [{array contents}]
array contents ::= {literal} | {literal}, {array contents}

Input ::= input({or})
Output ::= print({or})

creation ::= {type}[{num}]       used to make arrays of certain size. Can be changed to make different classes or structs in the future

Single line Comment = #
Multiline Comment = 
$

Hello world this is a multiline quote

$
 

Name ::= Some regular expression     Capital letters lowercase letters digits and underscore






variables in scope will be stored in 2 dicts. One name value dict, one name type dict