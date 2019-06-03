import java.util.*;
public class stringer {
	public static void main(String[] args) {
		Scanner input = new Scanner(System.in);
		String board;
		int point = 0;
		System.out.println("Welcome to this weird game of SWAP");
		System.out.print("Do you want to use the default board configuration? ");
		String yN = input.next();
		
		if(yN.equalsIgnoreCase("no")){
			board = boardTaker();
		}else{
			board ="ABGERTFFAKEMGVJA";
		}
		board = board.toUpperCase();

		System.out.println("This is the board configuration now:");
		boardPrinter(board);

		System.out.print("How many moves do you want to make? ");
		int move = input.nextInt();
		
		System.out.println("Make a move and press enter. After each move, the board configuration and your total points will be printed. Input the coordinates to be swapped.");
		System.out.println();
		
		for(int i = 0 ; i < move ; i++){
			int x1 = input.nextInt();
			int y1 = input.nextInt();
			int x2 = input.nextInt();
			int y2 = input.nextInt();
			
			int firstPos = ((x1 - 1) * 4 + y1 - 1);
			int secondPos = ((x2 - 1) * 4 + y2 - 1);
			if(firstPos > secondPos){
				int temp = firstPos;
				firstPos = secondPos;
				secondPos = temp;
			}
			board = moveMaker(board, firstPos, secondPos);
			System.out.println("This is the board configuration now:");
			boardPrinter(board);
			
			point = pointCalculator(board);
			System.out.println("Your total score is " + point + ".");
			System.out.println();
		}
		System.out.println("Thank you for playing this game.");
	   
	}
	public static String boardTaker(){
		Scanner input = new Scanner(System.in);
		String board = "";
		for(int i = 1 ; i <= 4 ; i++){
			System.out.print("Enter row " + i + " of the board: ");
			String line = input.nextLine();
			board += line;
		}
		return board;
	}
	public static void boardPrinter(String board){
		for(int i = 0 ; i < 4 ; i++){
			System.out.println(board.substring((i * 4), ((i + 1) * 4)));
		}
		System.out.println();
	}
	public static String moveMaker(String board, int firstPos, int secondPos){
		String newBoard = board.substring(0, firstPos) + board.substring(secondPos, secondPos + 1) + board.substring(firstPos+1, secondPos) + board.substring(firstPos, firstPos + 1) + board.substring(secondPos+1);
		
		return newBoard;
	}
	public static int pointCalculator(String board){
		int point  = 0;
		for(int i = 0 ; i < board.length() - 1 ; i++){
			if((i+1) % 4 != 0){
				if(board.charAt(i) == board.charAt(i+1))
					point++;
			}	
		}
		
		return point;
	}
}
