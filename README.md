# Bamboolean interpreter

[![Build Status](https://travis-ci.org/qedsoftware/bamboolean.svg?branch=master)](https://travis-ci.org/qedsoftware/bamboolean)

Supported from Python >= 3.4

Implementation of Bamboolean - Boolean Logic Language

Bamboolean is a simple language that consumes array of pre-defined variables, and
returns boolean value if constraints on these variables are met.

[Exemplary expressions in the language](./bamboolean/tests/fixtures.py)

## Features

- Case in-sensitive variable names and keywords
- Comparison operators
- Logic AND / OR
- Expressions with parentheses
- Types: Floats, ints and string

##### Operators associativity

All operators are lef-associative

##### Operators precedence (the higher number the higher priority)

1. OR
2. AND
3. == | != | < | <= | > | >=

## Testing

Run tests:

    `python run_tests.py`

## BNF Grammar

```
expr : simple_expr (OR simple_expr)*

simple_expr : term (AND term)*

term : constraint
     | LPAREN expr RPAREN

constraint : variable relational_operator value

value : INTEGER
      | FLOAT
      | STRING
      | BOOL

variable: ID

relational_operator : ( EQ | NE | LT | LTE | GT | GTE )
```
