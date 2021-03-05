package project1;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Stack;

/**
 * This is the driver of the game, where the initial state is generated and the
 * searched towards the goal state is performed.
 *
 * @author Allen Westgate, Bernardo Santos, and Ryan Farrell
 */
public class Project1 {

    /**
     * This is the main class of the program.
     *
     * @param args the command line arguments
     */
    public static void main(String[] args) throws CloneNotSupportedException {

        // Generate initial game state based on the number of freecells from 
        // the command line.
        GameState gb = new GameState();
        int numFreecells=4;
        if(args[0].matches("\\d*"))
            numFreecells = Integer.parseInt(args[0]);
        else
            System.out.println("Number of free cells must be non-negative whole number!"
                    + "\nDefaulting to 4 free cells!");
        
        gb.generateInitialState(numFreecells);
        gb.printState();

        ArrayList<ArrayList<String>> forbidden = new ArrayList<>(); // List of paths that lead to an infinite loop/dead end.
        ArrayList<Action> acts = new ArrayList<>(); // List to store the possible actions of a given state temporarily.
        Stack<Action> stack = new Stack<>(); // Stack used to put the actions from the initial state until the goal state.
        int smallestHeuristic = 1000; // Initialize the heuristic value.
        GameState bestState = null; // Variable used to store the best state found from a previous state.
        Action tmpAction = null; // Temporary best action found.
        Map<String, Integer> visitedStates = new HashMap<>(); // Hash map containing the unique ids of the states (key) and the maximum number of times it can be visited (value).

        // Initialize the current variable to be the same as the initial state.
        GameState current = new GameState(gb.getFoundation(), gb.getFreecells(), gb.getPiles(), gb.getPath());

        int count = 0;
        // Search for the goal state given an initial one and print the path to it.
        while (count < 50000) {
            count += 1;
            if(count % 450 == 0){
                System.out.println("Calculating...");
            }
            // Initialize the temporary state that is going to be used to get
            // the possible actions.
            GameState tmpState = new GameState(current.getFoundation(), current.getFreecells(), current.getPiles(), current.getPath());
            acts = tmpState.getPossibleActions(); // Get possible actions.
            smallestHeuristic = 1000; // Initialize heuristics.

            // Search for the best action from the current state and pick the
            // best one according to the heuristic value of it.
            for (Action possibleAction : acts) {
                // Do not allow moving from a freecell to another, as it does
                // not change the state of the game.
                if (!(possibleAction.getDestination().equals("freecell") && possibleAction.getDestination().equals(possibleAction.getOrigin()))) {

                    // Initialize a new temporary state to test the given action.
                    GameState tmpState2 = new GameState(tmpState.getFoundation(),
                            tmpState.getFreecells(), tmpState.getPiles(), tmpState.getPath());
                    tmpState2.performAction(possibleAction);

                    // If the path to the state created is not in the forbidden
                    // lsit, then check if the action is a move to a foundation.
                    if (!forbidden.contains(tmpState2.getPathAsString())) {

                        // If moving to a foundation, then update the heuristic
                        // value, push the action to the stack of actions, and 
                        // update the best state to be the one created by this
                        // action.
                        if (possibleAction.getDestination().equals("foundation")) {
                            tmpAction = possibleAction;
                            smallestHeuristic = tmpState2.getHeuristics();
                            stack.push(possibleAction);
                            bestState = tmpState2;
                            break;
                        } else {

                            // If not a move to a foundation, then check if the
                            // heuristic value of the state produced by the
                            // action is less than the smallest found so far (h).
                            // If so, then update it.
                            if (tmpState2.getHeuristics() < smallestHeuristic) {
                                smallestHeuristic = tmpState2.getHeuristics();
                                tmpAction = possibleAction;
                                bestState = tmpState2;
                            }
                        }
                    }
                }

            }

            // if game has finished print the path to the solution and terminate the program.
            if (bestState.isGameFinished()) {
                System.out.println("FINISHED!");
                bestState.PrintPathToSolution(gb);
                System.exit(0);
            } else {
                // If no path found.
                if (smallestHeuristic == 1000) {

                    // Add the path to the state to the forbidden list.
                    ArrayList<String> tmpForbidden = new ArrayList<>();
                    for (Action actions : current.getPath()) {
                        tmpForbidden.add(actions.toString());
                    }
                    forbidden.add(tmpForbidden);

                    // If stack of actions is not empty, then pop it.
                    if (!stack.isEmpty()) {
                        stack.pop();
                    }

                    // Recreate the previous state from the initial one, based on
                    // the actions stored in the stack.
                    current = null;
                    current = new GameState(gb.getFoundation(), gb.getFreecells(), gb.getPiles(), gb.getPath());

                    ArrayList<Action> arr = new ArrayList<>();
                    stack.forEach(o -> {
                        arr.add((Action) o);
                    });

                    for (int i = 0; i < arr.size(); i++) {
                        if (i != arr.size() - 1) {
                            if (!arr.get(i).toString().equals(arr.get(i + 1).toString())) {
                                current.performAction(arr.get(i));
                            }
                        } else {
                            current.performAction(arr.get(i));
                        }
                    }
                } // If dead end found.
                else if (bestState.isDeadEnd()) {
                    //System.out.println("Dead end!");
                    ArrayList<String> f = new ArrayList<>();
                    for (Action actions : bestState.getPath()) {
                        f.add(actions.toString());
                    }
                    forbidden.add(f);
                } // If a viable path has been found.
                else {
                    //System.out.println("Path found(1): " + tmpAction);
                    //bestState.printState();
                    
                    // Check the hash map to see if it contains the unique id
                    // of the state. If it does not, then put the unique id as 
                    // a key and the number of possible actions as a value.
                    if (!visitedStates.containsKey(bestState.id())) {
                        visitedStates.put(bestState.id(), bestState.getPossibleActions().size() + 1);
                    } 
                    // Else, decrease the value of the unique id by 1.
                    else {
                        Integer val = visitedStates.get(bestState.id());
                        visitedStates.replace(bestState.id(), val - 1);
                    }
                    
                    // If the hash map's value of the unique id is greater than
                    // zero, it means that we still can look for more actions
                    // from that state.
                    if (visitedStates.get(bestState.id()) > 0) {
                        stack.add(tmpAction);
                        current = null;
                        current = new GameState(bestState.getFoundation(), bestState.getFreecells(), bestState.getPiles(), bestState.getPath());
                        if (current.isGameFinished()) {
                            System.out.println("FINISHED!");
                            bestState.PrintPathToSolution(gb);
                            System.exit(0);
                        }
                    } // If the hash map's value of the unique id is equal to
                    // zero, it means that we cannot look for more actions from
                    // that state, so we should treat it as if an infinite loop
                    // was found.
                    else {
                        //System.out.println("Infinite loop!");
                        //bestState.printState();
                        
                        // Add the current path to the forbidden list of paths.
                        ArrayList<String> f = new ArrayList<>();
                        for (Action actions : bestState.getPath()) {
                            f.add(actions.toString());
                        }
                        forbidden.add(f);
                        if (!stack.isEmpty()) {
                            stack.pop();
                        }
                        
                        // Update the current state to be the previous one.
                        current = null;
                        current = new GameState(gb.getFoundation(), gb.getFreecells(), gb.getPiles(), gb.getPath());

                        // Recreate the previous state based on the initial states
                        // and the actions from the stack.
                        ArrayList<Action> arr = new ArrayList<>();
                        stack.forEach(o -> {
                            arr.add((Action) o);
                        });

                        for (int i = 0; i < arr.size(); i++) {
                            if (i != arr.size() - 1) {
                                if (!arr.get(i).toString().equals(arr.get(i + 1).toString())) {
                                    current.performAction(arr.get(i));
                                }
                            } else {
                                current.performAction(arr.get(i));
                            }
                        }
                    }
                }
            }

        }
        System.out.println("Cannot solve this game. Goodbye!");
    }
}