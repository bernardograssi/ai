# Frecell Sollitaire Solver
Authors: Ryan Farrell, Bernardo Santos, Allen Westgate

## Description
This project creates a random game of Freecell Sollitaire and outputs it to the screen before moving to solve the game in the shortest time possible.

## Implementation
The game board is divided in the following way:

A list of lists represent the 7 central columns, also known as piles. Each inner list contains the cards, which are represented by the Card object.
A list representing the freecells spots.
A list of stacks representing the foundations spots, also known as the goal spots.

## Algorithm to Find Path
In order to find the path from the initial setup, the program creates a initial state, which represents the initial setup, with all the objects related to it,
such as the piles, the freecells, the foundations etc. 

Given an initial state, the program calculates all the possible actions in that state and calculate a heuristic
value for each state. A heuristic value is an attribute of each state object (GameState). For each of those states, the program calculates each possible action from it
and keeps searching until a goal state is found. 

The program uses Alpha-Beta prunning to perform a search over all the possible states, keeps a stack containing the 
path to the current state, keeps a list of forbidden paths, in order to escape dead-ends and infinite loops. 

## Results
The program gets the path in 85-90% of the times. In the situations that it does not, it outputs to the screen a message saying that the path could not be found.
Program run time should be between 0 seconds and 2 minutes. 

## Usage
Input the number of free cells as a command line argument.
Number of free cells may be any whole number greater than or equal to 0. Invalid input will default to 4 free cells. 
