public class CustomThreePrisonersDilemma {

	/*
	 * This Java program models the two-player Prisoner's Dilemma game. We use the
	 * integer "0" to represent cooperation, and "1" to represent defection.
	 * 
	 * Recall that in the 2-players dilemma, U(DC) > U(CC) > U(DD) > U(CD), where we
	 * give the payoff for the first player in the list. We want the three-player
	 * game to resemble the 2-player game whenever one player's response is fixed,
	 * and we also want symmetry, so U(CCD) = U(CDC) etc. This gives the unique
	 * ordering
	 * 
	 * U(DCC) > U(CCC) > U(DDC) > U(CDC) > U(DDD) > U(CDD)
	 * 
	 * The payoffs for player 1 are given by the following matrix:
	 */

	static int[][][] payoff = { 
		{ { 6, 3 }, // payoffs when first and second players cooperate
		{ 3, 0 } }, // payoffs when first player coops, second defects
		{ { 8, 5 }, // payoffs when first player defects, second coops
		{ 5, 2 } }  // payoffs when first and second players defect
	};

	/*
	 * So payoff[i][j][k] represents the payoff to player 1 when the first player's
	 * action is i, the second player's action is j, and the third player's action
	 * is k.
	 * 
	 * In this simulation, triples of players will play each other repeatedly in a
	 * 'match'. A match consists of about 100 rounds, and your score from that match
	 * is the average of the payoffs from each round of that match. For each round,
	 * your strategy is given a list of the previous plays (so you can remember what
	 * your opponent did) and must compute the next action.
	 */

	abstract class Player {
		// This procedure takes in the number of rounds elapsed so far (n), and
		// the previous plays in the match, and returns the appropriate action.
		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			throw new RuntimeException("You need to override the selectAction method.");
		}

		// Used to extract the name of this player class.
		final String name() {
			String result = getClass().getName();
			return result.substring(result.indexOf('$') + 1);
		}
	}

	/* Here are four simple strategies: */

	class NicePlayer extends Player {
		// NicePlayer always cooperates
		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			return 0;
		}
	}

	class NastyPlayer extends Player {
		// NastyPlayer always defects
		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			return 1;
		}
	}

	class RandomPlayer extends Player {
		// RandomPlayer randomly picks his action each time
		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			if (Math.random() < 0.5)
				return 0; // cooperates half the time
			else
				return 1; // defects half the time
		}
	}

	class TolerantPlayer extends Player {
		// TolerantPlayer looks at his opponents' histories, and only defects
		// if at least half of the other players' actions have been defects
		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			int opponentCoop = 0;
			int opponentDefect = 0;
			for (int i = 0; i < n; i++) {
				if (oppHistory1[i] == 0)
					opponentCoop = opponentCoop + 1;
				else
					opponentDefect = opponentDefect + 1;
			}
			for (int i = 0; i < n; i++) {
				if (oppHistory2[i] == 0)
					opponentCoop = opponentCoop + 1;
				else
					opponentDefect = opponentDefect + 1;
			}
			if (opponentDefect > opponentCoop)
				return 1;
			else
				return 0;
		}
	}

	class FreakyPlayer extends Player {
		// FreakyPlayer determines, at the start of the match,
		// either to always be nice or always be nasty.
		// Note that this class has a non-trivial constructor.
		int action;

		FreakyPlayer() {
			if (Math.random() < 0.5)
				action = 0; // cooperates half the time
			else
				action = 1; // defects half the time
		}

		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			return action;
		}
	}

	class T4TPlayer extends Player {
		// Picks a random opponent at each play,
		// and uses the 'tit-for-tat' strategy against them
		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			if (n == 0)
				return 0; // cooperate by default
			if (Math.random() < 0.5)
				return oppHistory1[n - 1];
			else
				return oppHistory2[n - 1];
		}
	}

	/**
	 * Switch choice if unsure
	 */
	class T4TSwitchPlayer extends Player {
		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			// cooperate by default
			if (n == 0)
				return 0;

			// https://www.sciencedirect.com/science/article/abs/pii/S0096300316301011
			if (oppHistory1[n-1] == oppHistory2[n-1])
				return oppHistory1[n-1];

			return (myHistory[n-1] == 0) ? 1 : 0;
		}
	}

	/**
	 * Stay with using the previous choice if unsure.
	 */
	class T4TStayPlayer extends Player {
		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			// cooperate by default
			if (n == 0)
				return 0;

			// https://www.sciencedirect.com/science/article/abs/pii/S0096300316301011
			if (oppHistory1[n-1] == oppHistory2[n-1])
				return oppHistory1[n-1];

			return myHistory[n-1];
		}
	}

	/**
	 * Cooperates if unsure.
	 */
	class T4TCoopPlayer extends Player {
		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			// cooperate by default
			if (n == 0)
				return 0;

			// https://www.sciencedirect.com/science/article/abs/pii/S0096300316301011
			if (oppHistory1[n-1] == oppHistory2[n-1])
				return oppHistory1[n-1];

			return 0;
		}
	}

	/**
	 * Defects if unsure.
	 */
	class T4TDefectPlayer extends Player {
		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			// cooperate by default
			if (n == 0)
				return 0;

			// https://www.sciencedirect.com/science/article/abs/pii/S0096300316301011
			if (oppHistory1[n-1] == oppHistory2[n-1])
				return oppHistory1[n-1];

			return 1;
		}
	}

	/**
	 * Compares player history, then cooperates if score is >= others, else defect
	 */
	class HistoryPlayer extends Player {
		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			int myScore = 0;
			int oppScore1 = 0;
			int oppScore2 = 0;

			for (int index = 0; index < n; ++index) {
				myScore += myHistory[index];
				oppScore1 += oppHistory1[index];
				oppScore2 += oppHistory2[index];
			}

			return (myScore >= oppScore1 && myScore >= oppScore2) ? 0 : 1;
		}
	}

	/**
	 * Less-tolerant than TolerantPlayer
	 */
	class LessTolerantPlayer extends Player {
		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			// cooperate by default
			if (n == 0)
				return 0;

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

			return (opponentDefect >= opponentCoop) ? 1 : 0;
		}
	}

	/**
	 * Always switches choice.
	 */
	class SwitchPlayer extends Player {
		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			// cooperate by default
			if (n == 0)
				return 0;
			
			return (myHistory[n-1] == 0) ? 1 : 0;
		}
	}

	/**
	 * Combination of T4T and Tolerant
	 */
	class T4TTolerantPlayer extends Player {
		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			// cooperate by default
			if (n == 0)
				return 0;

			// https://www.sciencedirect.com/science/article/abs/pii/S0096300316301011
			if (oppHistory1[n-1] == oppHistory2[n-1])
				return oppHistory1[n-1];

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
	}

	/**
	 * Combination of T4T and LessTolerant
	 */
	class T4TLessTolerantPlayer extends Player {
		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			// cooperate by default
			if (n == 0)
				return 0;

			// https://www.sciencedirect.com/science/article/abs/pii/S0096300316301011
			if (oppHistory1[n-1] == oppHistory2[n-1])
				return oppHistory1[n-1];

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

			return (opponentDefect >= opponentCoop) ? 1 : 0;
		}
	}

	/**
	 * Combination of T4T and History
	 */
	class T4THistoryPlayer extends Player {
		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			// cooperate by default
			if (n == 0)
				return 0;

			// https://www.sciencedirect.com/science/article/abs/pii/S0096300316301011
			if (oppHistory1[n-1] == oppHistory2[n-1])
				return oppHistory1[n-1];

			// HistoryPlayer
			int myScore = 0;
			int oppScore1 = 0;
			int oppScore2 = 0;

			for (int index = 0; index < n; ++index) {
				myScore += myHistory[index];
				oppScore1 += oppHistory1[index];
				oppScore2 += oppHistory2[index];
			}

			return (myScore >= oppScore1 && myScore >= oppScore2) ? 0 : 1;
		}
	}

	/**
	 * Combination of T4T, Tolerant and History
	 */
	class T4TTolerantHistoryPlayer extends Player {
		private int numRoundsThreshold = 5;

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
			int myScore = 0;
			int oppScore1 = 0;
			int oppScore2 = 0;

			for (int index = 0; index < n; ++index) {
				myScore += myHistory[index];
				oppScore1 += oppHistory1[index];
				oppScore2 += oppHistory2[index];
			}

			return (myScore >= oppScore1 && myScore >= oppScore2) ? 0 : 1;
		}
	}

	/**
	 * Combination of T4T and Tolerant; also tries to take advantage of NicePlayer
	 */
	class T4TTolerantTakeAdvantagePlayer extends Player {
		private int numRoundsThreshold = 10;

		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			// cooperate by default
			if (n == 0)
				return 0;

			if (n >= numRoundsThreshold) {
				int iDefect = 0;
				int oppDefect1 = 0;
				int oppDefect2 = 0;

				for (int index = n - 1; index > n - 1 - numRoundsThreshold; --index) {
					iDefect += myHistory[index];
					oppDefect1 += oppHistory1[index];
					oppDefect2 += oppHistory2[index];
				}
	
				if (iDefect == 0 && oppDefect1 == 0 && oppDefect2 == 0)
					return 1; // take advantage
			}

			if (oppHistory1[n-1] == 0 && oppHistory2[n-1] == 0)
				return 0; // cooperate along

			if (oppHistory1[n-1] == 1 && oppHistory2[n-1] == 1 && myHistory[n-1] != 1)
				return 1; // both defect while i cooperate

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
	}

	/*
	 * In our tournament, each pair of strategies will play one match against each
	 * other. This procedure simulates a single match and returns the scores.
	 */
	float[] scoresOfMatch(Player A, Player B, Player C, int rounds) {
		int[] HistoryA = new int[0], HistoryB = new int[0], HistoryC = new int[0];
		float ScoreA = 0, ScoreB = 0, ScoreC = 0;

		for (int i = 0; i < rounds; i++) {
			int PlayA = A.selectAction(i, HistoryA, HistoryB, HistoryC);
			int PlayB = B.selectAction(i, HistoryB, HistoryC, HistoryA);
			int PlayC = C.selectAction(i, HistoryC, HistoryA, HistoryB);
			ScoreA = ScoreA + payoff[PlayA][PlayB][PlayC];
			ScoreB = ScoreB + payoff[PlayB][PlayC][PlayA];
			ScoreC = ScoreC + payoff[PlayC][PlayA][PlayB];
			HistoryA = extendIntArray(HistoryA, PlayA);
			HistoryB = extendIntArray(HistoryB, PlayB);
			HistoryC = extendIntArray(HistoryC, PlayC);
		}
		float[] result = { ScoreA / rounds, ScoreB / rounds, ScoreC / rounds };
		return result;
	}

	// This is a helper function needed by scoresOfMatch.
	int[] extendIntArray(int[] arr, int next) {
		int[] result = new int[arr.length + 1];
		for (int i = 0; i < arr.length; i++) {
			result[i] = arr[i];
		}
		result[result.length - 1] = next;
		return result;
	}

	/*
	 * The procedure makePlayer is used to reset each of the Players (strategies) in
	 * between matches. When you add your own strategy, you will need to add a new
	 * entry to makePlayer, and change numPlayers.
	 */

	int numPlayers = 16; // includes custom Players

	Player makePlayer(int which) {
		switch (which) {
			// Not using RandomPlayer, FreakyPlayer and given T4TPlayer,
			// as randomness makes it difficult to judge outcome.
			// Non-T4T variants have duplicates to even so that half are T4T.
			case 0:
				return new NicePlayer();
			case 1:
				return new NastyPlayer();
			case 2:
				return new RandomPlayer();
			case 3:
				return new TolerantPlayer();
			case 4:
				return new T4TSwitchPlayer();
			case 5:
				return new T4TStayPlayer();
			case 6:
				return new T4TCoopPlayer();
			case 7:
				return new T4TDefectPlayer();
			case 8:
				return new HistoryPlayer();
			case 9:
				return new LessTolerantPlayer();
			case 10:
				return new SwitchPlayer();
			case 11:
				return new T4TTolerantPlayer();
			case 12:
				return new T4THistoryPlayer();
			case 13:
				return new T4TLessTolerantPlayer();
			case 14:
				return new T4TTolerantHistoryPlayer();
			case 15:
				return new T4TTolerantTakeAdvantagePlayer();
		}
		throw new RuntimeException("Bad argument passed to makePlayer");
	}

	/* Finally, the remaining code actually runs the tournament. */

	public static void main(String[] args) {
		CustomThreePrisonersDilemma instance = new CustomThreePrisonersDilemma();
		instance.runTournament();
	}

	boolean verbose = true; // set verbose = false if you get too much text output

	void runTournament() {
		float[] totalScore = new float[numPlayers];

		// This loop plays each triple of players against each other.
		// Note that we include duplicates: two copies of your strategy will play once
		// against each other strategy, and three copies of your strategy will play
		// once.

		for (int i = 0; i < numPlayers; i++)
			for (int j = i; j < numPlayers; j++)
				for (int k = j; k < numPlayers; k++) {

					Player A = makePlayer(i); // Create a fresh copy of each player
					Player B = makePlayer(j);
					Player C = makePlayer(k);
					int rounds = 90 + (int) Math.rint(20 * Math.random()); // Between 90 and 110 rounds
					float[] matchResults = scoresOfMatch(A, B, C, rounds); // Run match
					totalScore[i] = totalScore[i] + matchResults[0];
					totalScore[j] = totalScore[j] + matchResults[1];
					totalScore[k] = totalScore[k] + matchResults[2];
					if (verbose)
						System.out.println(A.name() + " scored " + matchResults[0] + " points, " + B.name() + " scored "
								+ matchResults[1] + " points, and " + C.name() + " scored " + matchResults[2]
								+ " points.");
				}
		int[] sortedOrder = new int[numPlayers];
		// This loop sorts the players by their score.
		for (int i = 0; i < numPlayers; i++) {
			int j = i - 1;
			for (; j >= 0; j--) {
				if (totalScore[i] > totalScore[sortedOrder[j]])
					sortedOrder[j + 1] = sortedOrder[j];
				else
					break;
			}
			sortedOrder[j + 1] = i;
		}

		// Finally, print out the sorted results.
		if (verbose)
			System.out.println();
		System.out.println("Tournament Results");
		for (int i = 0; i < numPlayers; i++)
			System.out.println(makePlayer(sortedOrder[i]).name() + ": " + totalScore[sortedOrder[i]] + " points.");

	} // end of runTournament()

} // end of class PrisonersDilemma
