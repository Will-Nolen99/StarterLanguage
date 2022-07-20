# StarterLanguage
Basic custom Programming Language implemented in python


# Features
Interpreted Programming language.
Full arithmatic support: addition, subtraction, multiplication, division, modulus, floor division, exoponentiation, and nth root
Full flow control: if, if else, if else if ..., for loops, while loops, do while loops.
Input and output: Print and read from terminal.
5 Basic data types: int, float, boolean, string, array.
Pre/Post Increment/Decrement as well as assignment types for all arithmetic operators.
Define custom functions with paramaters and return types.

# Features soon to be added/partially implemented
command line arguments: Partially implemented
structs / basic class: Included in bnf grammar not yet implemented
import functions from other files: not yet implemented
Better type casting: Partially implemented based on python defaults
Better functions for interacting with strings / arrays: not yet implemented


# Instructions to run
Navigate to directory containing interpreter.py
To run in terminal use: python interpreter.py <source_file_path>


# Language Guide

### Declaration
Declare variables using their type then the name: int x
This may or may not be followed by initialization: int x = 5
Many variables may be declared in series using a comma. Unlike other languages the type must be specified each time but types can be mixed: int x = 5, float y, float z, int num

### Assignment
After declaration assignment is done using the let keyword: 

let x = 7

let y = x * 4
                                                            
There exist assignment operators for each arithmetic operator.

The the arithmetic operator simply is put in front of the equal sign: 

let x += 4
                                                                      
let z *= 3
### Arithmetic Operators
  
addition: +
   
subtraction: -
   
multilplication: *
   
division: /
   
modulus: %
   
floor division: ~
   
exponentiation:  ^
   
nth root: :

### Increment/Decrement
Increment and decrement operators work the same as in other languages.

To use these there is no need for the let keyword unless used in an assignment statement.

x++
++x
--x
x--

### flow control
In each example replace condition with the needed condition and statements with the body of the statement/loop.
Whitespace is not imported and each part may be on its own line

### if

if condition {
    statements
}

if condition {
    statements
} else {
    statements
}

if condition {
    statements
} else if condition {
    statments
}

These can be chained indefinetly

### while
while condition {
    statements
}

### do while

do{
    statements
} while condition

### for

for declaration | loop condition | expression ran at end of each loop iteration {
    statements
}


### binary and unary operators
&&    logical and

||    logical or

!     logical not

( and ) can be used to establish precedence


### functions

define name = paramater declaration -> {
    statements
} -> return type

Each function requires at least one parameter and must state a return type.

To return from a function use: 

return value_to_return

### main function
define main = array command_line_args, int arg_count -> {

} -> int

The names of the parameters above can be changed.
The first parameter will be an array containing the command line arguments.
The second will be the length of that array.

### comments
#is a single line comment

$ is a multiline comment $

Note the interpretter contains a printer that prints the read source file.
If enabled comments will be omitted as they are not held in the parse tree.
