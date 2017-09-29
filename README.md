# Boolang interpreter

Implementation of Boolang - Boolean Logic Language

Boolang is a simple language that consumes array of pre-defined variables, and
returns boolean value if constraints on these variables are met.

## Features

1. Case in-sensitive variable names and keywords

TODO: list features
TODO: describe operators associativity and precedence

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