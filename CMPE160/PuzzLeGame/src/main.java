package puzzleGame;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.PrintStream;
import java.util.*; 
import java.util.regex.*; 

class Tuple<X, Y> { 
	public X x; 
    public Y y; 
    public Tuple(X x, Y y) { 
    	this.x = x; 
    	this.y = y; 
	}
} 

public class main {
	
	public static void main(String[] args) throws FileNotFoundException {
		
		Scanner argument = new Scanner(new File(args[0]));
		
		ArrayList<Integer> input = new ArrayList();
		
		while(argument.hasNext()) {
			Pattern pattern = Pattern.compile("\\d+");
			Matcher matcher = pattern.matcher(argument.next());
			while(matcher.find()) {
			    input.add(Integer.parseInt(matcher.group()) );
			}	
		}
		
		String control = "" ;
		
		int size = input.size();
		for(int m = 1; m < size ; m++ ) {
			
			control = control.concat(Integer.toString(m));
		}
		control = control.concat("0");
		int length = (int) Math.sqrt(size);
		int index = 0;
		LinkedHashMap<Integer, Tuple<Integer, Integer>> map = new LinkedHashMap<>(); 
		
		for(int i = 0 ; i < length ; i++) {
			for(int j = 0 ; j < length ; j++) {
				Tuple<Integer, Integer> tuple = new Tuple<Integer, Integer>(j,i) ;
				map.put(input.get(index), tuple);
				index++;
			}
		}
		Puzzle puzzle = new Puzzle();
		puzzle.tree = new Tree(map);
		boolean check = true;
		puzzle.temporaryFunc(puzzle.tree.getHead(), control, check, length);
		
	}
}

