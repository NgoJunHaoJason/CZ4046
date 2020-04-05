/**
 * The Player that I am using for this assignment.
 * 
 * Results quite stable; tend to make it to top-5 among my custom Players. 
 * Emerges as top-1 occasionally.
 * 
 * Combination of Tit-for-tat and Tolerant.
 */
public class Ngo_Jason_Player { // extends Player
    private int numRoundsThreshold = 50;

    int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
        // cooperate by default
        if (n == 0)
            return 0;

        // https://www.sciencedirect.com/science/article/abs/pii/S0096300316301011
        if (oppHistory1[n-1] == oppHistory2[n-1])
            return oppHistory1[n-1];

        if (n < numRoundsThreshold) {
            // TolerantPlayer
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

            return (opponentDefect > opponentCoop) ? 1 : 0;
        }

        // else: more than numRoundsThreshold rounds have been played

        // HistoryPlayer
        int myNumDefections = 0;
        int oppNumDefections1 = 0;
        int oppNumDefections2 = 0;

        for (int index = 0; index < n; ++index) {
            myNumDefections += myHistory[index];
            oppNumDefections1 += oppHistory1[index];
            oppNumDefections2 += oppHistory2[index];
        }

        if (myNumDefections >= oppNumDefections1 && myNumDefections >= oppNumDefections2)
            return 0;
        else
            return 1;
    }
}
