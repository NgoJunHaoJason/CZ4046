/**
 * The Player that I am using for this assignment.
 * 
 * Combination of Tit-for-tat, Tolerant and History.
 */
public class Ngo_Jason_Player { // extends Player
    int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
        if (n == 0)
            return 0; // cooperate by default

        if (n >= 109)
            return 1; // opponents cannot retaliate

        // https://www.sciencedirect.com/science/article/abs/pii/S0096300316301011
        if (oppHistory1[n-1] == oppHistory2[n-1])
            return oppHistory1[n-1];

        // n starts at 0, so compare history first

        if (n % 2 != 0) { // odd round - be tolerant
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
        // else: even round - compare history
        
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
