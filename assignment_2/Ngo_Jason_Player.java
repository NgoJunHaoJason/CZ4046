/**
 * The Player that I am using for this assignment.
 * 
 * Results quite stable; tend to make it to top-5 among my custom Players. 
 * Emerges as top-1 occasionally.
 * 
 * Combination of Tit-for-tat and Tolerant.
 */
public class Ngo_Jason_Player { // extends Player
    int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
        // cooperate on first round
        if (n == 0)
            return 0;

        // https://www.sciencedirect.com/science/article/abs/pii/S0096300316301011
        // If other players both cooperate, do the same.
        // Likewise if they defect.
        if (oppHistory1[n-1] == oppHistory2[n-1])
            return oppHistory1[n-1];

        // else: one cooperate while the other defect
        // Use TolerantPlayer's strategy.
        int opponentCoop = 0;
        int opponentDefect = 0;

        for (int i = 0; i < n; i++) {
            if (oppHistory1[i] == 0)
                opponentCoop += 1;
            else
                opponentDefect += 1;

            if (oppHistory2[i] == 0)
                opponentCoop += 1;
            else
                opponentDefect += 1;
        }

        // Unless others have defected more than they cooperated in total,
        // cooperate along with them.
        return (opponentDefect > opponentCoop) ? 1 : 0;
    }
}
