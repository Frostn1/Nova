# Nova
The Nova Programming Language.<br>
Takes Nova code and either runs it using the compiler, or translates it into c code

## Docs

### Variables
The Nova language has a variable memory system, that lets you create new variables and assign them a value.
As you will see in Nova you don't assign the variable a type when creating a new variable,<br>
as the Nova compiler deducts the type of variable from the value you have assigned to it.<br>
In order to create a new variable in Nova we use the saved keyword `let`, as follows:
```js
let x = 1; // x will hold the value 1
let y = 2; // y will hold the value 2
```
You can even assign new values to existing variables, as follows:
```js
let x = 2.5; // x will hold the value 2.5
x = 15; // x will hold the value 15
```

### Operations
#### Arithmetic 
In Nova we have the various math operations in order to calculate different things.<br>
The most basics one are `+ - * /` ( add, subtract, multiply, divide ).<br>
We also have the `!` for factorial calculation.
Because of those features we can do the following:
```js
let x = 3;
let y = x * 5; // y will hold 15
```
#### Special
In Nova we can use the concat operator `..` in order to **connect** two numbers together to a single one.<br>
This lets us treat numbers as strings and join them together, as follows:
```js
let x = 1;
let y = 2;
let z = x .. y; // z will hold 12
```
For the ones of you that are curious on how this affects floating point numbers, the answer may be a surprise for you.<br>
As there isn't a clean solution for this that will make sense for all terms, we decided to cast the floating point number to int, and then concat the other number.<br>
This will result with the floating point dissapearing, as follows:
```js
let x = 3.5;
let y = 2;
let z = x .. y; // z will hold 32
```

### IO
In order to print expression to the screen, i.e. user, we have another special operator.<br>
Using the `>` we can print to screen various expression, as follows:
```js
> 3; // will print 3 to screen
> 3 .. 3.7; // will print 33 to screen
```

## Flags
- -cf --cformat compiles file to c
- -le --logerrors logs errors to file
- -r --run run code file inside a sandbox enviorment
- [WIP] -e --export exports functions for outer use


## TODO/Milestones
### Current
- [x] Concat operator
- [x] Runtime executing
- [x] CLI flags support
- [ ] Dynamic functions
### Future
- [ ] strings support
- [ ] Interpreter Version
- [ ] C lib for nova
- [ ] Link variables
- [ ] Functions

### Finished
- [x] Variable assignment
- [x] Error log support
- [x] Add Error Support
- [x] Convert to C
- [x] Type Deduction
- [x] Math Support
