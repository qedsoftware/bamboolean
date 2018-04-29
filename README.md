# Bamboolean interpreter

[![Build Status](https://travis-ci.org/qedsoftware/bamboolean.svg?branch=master)](https://travis-ci.org/qedsoftware/bamboolean)

Supported from Python >= 3.4

Implementation of Bamboolean - Boolean Logic Language

Bamboolean is a simple language that consumes array of pre-defined variables, and
returns boolean value if constraints on these variables are met.

[Exemplary expressions in the language](./bamboolean/tests/fixtures.py)

## Features

- Case in-sensitive variable names and keywords
- Comparison operators (listed below)
- Logic AND / OR
- Expressions with parentheses
- Types: Float, Int, String, Bool, Variable
- [Truth value testing same as in Python](https://docs.python.org/3/library/stdtypes.html#truth-value-testing)
- Implicit cast of variables to boolean when no relational operator is specified

##### Operators associativity

All operators are left-associative

##### Operators precedence (the higher number the higher priority)

1. OR
2. AND
3. == | != | < | <= | > | >=

## Testing

Run tests:

    `python run_tests.py`

## EBNF Grammar

```
compound_expr : expr
              | empty

expr : simple_expr (OR simple_expr)*

simple_expr : term (AND term)*

term : statement
     | LPAREN expr RPAREN

statement : value
          | constraint

constraint : variable (relational_operator value)?

relational_operator : ( EQ | NE | LT | LTE | GT | GTE )

value : INTEGER
      | FLOAT
      | STRING
      | BOOL

variable : ID

empty :

```
