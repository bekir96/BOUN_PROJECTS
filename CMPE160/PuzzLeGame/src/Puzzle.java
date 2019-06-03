package puzzleGame;

import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.HashMap;
import java.util.Map;
import java.util.Map.Entry;
import java.util.LinkedList; 
import java.util.Queue;
import java.util.TreeMap; 

public class Puzzle<T> {
	
	public Tree tree;
	public static final int indent1 = 19;
	public static final int indent2 = 14;
	public static int count = 1;
	public static int countNode = 0;
	public static int count13 = 0;
	Queue<Tuple<LinkedHashMap<Integer, Tuple<Integer, Integer>>, String>> q = new LinkedList<>();
	HashMap<String, Integer> controlQ = new HashMap<>();
	
	boolean allCheck = false;
	
	public static <T, E> T getKeyByValue(Map<T, E> map, E value) {
	    for (Entry<T, E> entry : map.entrySet()) {
	    	if((((Tuple) entry.getValue()).x == ((Tuple) value).x ) &&  (((Tuple) entry.getValue()).y == ((Tuple) value).y)){
	    		return entry.getKey();
	    	}
	    }
	    return null;
	}
	
	public <T>void temporaryFunc(T head, String control, boolean check, int controlNo) {

		if(controlNo == 3) {
			if(count <= indent1) {
				count++;
				if(check) {
					String hashing = checkFunc((Map<Integer, Tuple<Integer, Integer>>) head);
					controlQ.put(hashing,1);
					puzzleSolver(head, control, check, controlNo);
					check = false;
				}
				int size = q.size();
				int i = 0;
				
				while(i < size) {
					if(!allCheck) {
						puzzleSolver(q.remove(), control, check, controlNo);
					}
					else {
						System.exit(0);
						break;
					}
					i++;
				}
				temporaryFunc(head, control, check, controlNo);
			} else {
				
				System.out.println("N");
			}
		} else {
			if(count <= indent2) {
				count++;
				if(check) {
					String hashing = checkFunc((Map<Integer, Tuple<Integer, Integer>>) head);
					controlQ.put(hashing,1);
					puzzleSolver(head, control, check, controlNo);
					check = false;
				}
				int size = q.size();
				int i = 0;
				while(i < size) {
					if(!allCheck) {
						puzzleSolver(q.remove(), control, check, controlNo);
					}
					else {
						System.exit(0);
						break;
					}
					i++;
				}
				temporaryFunc(head, control, check, controlNo);
			} else {
				System.out.println("N");
			}
		}
	}
	
	public String checkFunc(Map<Integer, Tuple<Integer, Integer>> map) {
		
		TreeMap<Integer, Integer> newMap = new TreeMap();
		
		for (Map.Entry<Integer, Tuple<Integer, Integer>> entry : map.entrySet()) {	
			int y = (int) ((Tuple)entry.getValue()).y * 100;
			int x = (int) ((Tuple)entry.getValue()).x + y;
			newMap.put(x, entry.getKey());
		}
		String checkString = "";
		for (Map.Entry<Integer, Integer> entry : newMap.entrySet()) {
			checkString = checkString.concat(String.valueOf(entry.getValue()));
		}
		return checkString;
	}
	
	public <T> void puzzleSolver(T root, String control, boolean check, int size) {
		boolean up = false;
		boolean down = false;
		boolean left = false;
		boolean right = false;
		
		
		LinkedHashMap<Integer, Tuple<Integer, Integer>> leftMap = new LinkedHashMap<>(); 
		LinkedHashMap<Integer, Tuple<Integer, Integer>> rightMap = new LinkedHashMap<>();
		LinkedHashMap<Integer, Tuple<Integer, Integer>> upMap = new LinkedHashMap<>();
		LinkedHashMap<Integer, Tuple<Integer, Integer>> downMap = new LinkedHashMap<>();
		Iterator<Entry<Integer, Tuple<Integer, Integer>>> it ;
		
		if(check) {
			it = ((Map) root).entrySet().iterator();
		} else {
			
			it = ((Map) ((Tuple) root).x).entrySet().iterator();
		}
		
		int changeU = -1;
		int changeL = -1;
		int changeR = -1;
		int changeD = -1;
		while (it.hasNext()) {
			Map.Entry<Integer, Tuple<Integer, Integer>> pair = (Map.Entry<Integer, Tuple<Integer, Integer>>) it.next();
			Tuple<Integer, Integer> tuple = new Tuple<Integer, Integer>(pair.getValue().x,pair.getValue().y) ;
			
			if(pair.getKey() == 0) {
				for (Direction dir : Direction.values()) {
		    	    if(dir == Direction.UP ) {
		    	    	int xCoor = pair.getValue().x;
		    	    	int yCoor = (int) (pair.getValue().y + dir.getY());
		    	    	Tuple<Integer, Integer> tupleTemp = new Tuple<Integer, Integer>(xCoor,yCoor) ;
		    	    			    	    	
		    	    	if(yCoor >= size || yCoor < 0) {
		    	    		
		    	    	}
		    	    	else {
		    	    		up = true;
		    	    		if(check) {
		    	    			changeU = (int) getKeyByValue((Map)root, tupleTemp);
		    	    		} else {
		    	    			
		    	    			changeU = (int) getKeyByValue((Map)((Tuple) root).x, tupleTemp);
		    	    		}
		    	    		upMap.put(changeU, pair.getValue());
		    	    		upMap.put(pair.getKey(), tupleTemp);
		    	    	}		    	    	
		    	    }
		    	    if(dir == Direction.DOWN) {
		    	    	int xCoor = pair.getValue().x;
		    	    	int yCoor = (int) (pair.getValue().y + dir.getY());
		    	    	Tuple<Integer, Integer> tupleTemp = new Tuple<Integer, Integer>(xCoor,yCoor) ;
		    	    	
		    	    	if(yCoor >= size || yCoor < 0) {
		    	    		
		    	    	}
		    	    	else {
		    	    		down = true;
		    	    		if(check) {
		    	    			changeD = (int) getKeyByValue((Map)root, tupleTemp);
		    	    		} else {
		    	    			changeD = (int) getKeyByValue((Map)((Tuple) root).x, tupleTemp);
		    	    		}
		    	    		downMap.put(changeD, pair.getValue());
		    	    		downMap.put(pair.getKey(), tupleTemp);
		    	    	}		    	    	
		    	    }
		    	    if(dir == Direction.LEFT ) {
		    	    	
		    	    	int xCoor = (int) (pair.getValue().x + dir.getX());
		    	    	int yCoor = pair.getValue().y;
		    	    	Tuple<Integer, Integer> tupleTemp = new Tuple<Integer, Integer>(xCoor,yCoor) ;
		    	    	
		    	    	if(xCoor >= size || xCoor <0) {
		    	    	}
		    	    	else {
		    	    		left = true;
		    	    		if(check) {
		    	    			changeL = (int) getKeyByValue((Map)root, tupleTemp);
		    	    		} else {
		    	    			changeL = (int) getKeyByValue((Map)((Tuple) root).x, tupleTemp);
		    	    		}
		    	    		leftMap.put(changeL, pair.getValue());
		    	    		leftMap.put(pair.getKey(), tupleTemp);
		    	    	}
		    	    }
		    	    if(dir == Direction.RIGHT) {
		    	    	int xCoor = (int) (pair.getValue().x + dir.getX());
		    	    	int yCoor = pair.getValue().y;
		    	    	Tuple<Integer, Integer> tupleTemp = new Tuple<Integer, Integer>(xCoor,yCoor) ;
		    	    	
		    	    	if(xCoor >= size || xCoor <0) {
		    	    	}
		    	    	else {
		    	    		right = true;
		    	    		if(check) {
		    	    			changeR = (int) getKeyByValue((Map)root, tupleTemp);
		    	    		} else {
		    	    			
		    	    			changeR = (int) getKeyByValue((Map)((Tuple) root).x, tupleTemp);
		    	    		}
		    	    		rightMap.put(changeR, pair.getValue());
		    	    		rightMap.put(pair.getKey(), tupleTemp);
		    	    	}
		    	    }
		    	}
			}
			else {
				
				if(up) {
					if(pair.getKey() == changeU) {	
					} 
					else {
						upMap.put(pair.getKey(), tuple);
					}
				} else {
					upMap.put(pair.getKey(), tuple);
				}
				if(down) {
					if(pair.getKey() == changeD) {	
					} 
					else {
						downMap.put(pair.getKey(), tuple);
					}
				} else {
					downMap.put(pair.getKey(), tuple);
				}
				if(left) {
					if(pair.getKey() == changeL) {	
					} 
					else {
						leftMap.put(pair.getKey(), tuple);
					}
				} else {
					leftMap.put(pair.getKey(), tuple);
				}
				if(right) {
					if(pair.getKey() == changeR) {	
					} 
					else {
						rightMap.put(pair.getKey(), tuple);
					}
				} else {
					rightMap.put(pair.getKey(), tuple);
				}
			}
		}
		if(right == true) {
			String temp = "R" ;
			if(check) {
				temp = "R";
			} else {
				String x = (String) ((Tuple)root).y;
				temp = x.concat(temp);
			}
			Tuple<LinkedHashMap<Integer, Tuple<Integer, Integer>>, String> tupleRight = new Tuple<LinkedHashMap<Integer, Tuple<Integer, Integer>>, String>(rightMap,temp);
			String hashing = checkFunc(rightMap);
			if(!controlQ.containsKey(hashing)) {
				controlQ.put(hashing,1);
				if(hashing.equals(control)) {
					allCheck = true;
					System.out.println(temp);
					System.exit(0);
				}
				q.add(tupleRight);
				tree.addLeaf(root, tupleRight);
			} 
		}
		if(down == true) {
			String temp = "D" ;
			if(check) {
				temp = "D";
			} else {
				String x = (String) ((Tuple)root).y;
				temp = x.concat(temp);
			}
			Tuple<LinkedHashMap<Integer, Tuple<Integer, Integer>>, String> tupleDown = new Tuple<LinkedHashMap<Integer, Tuple<Integer, Integer>>, String>(downMap,temp) ;
			String hashing = checkFunc(downMap);
			if(!controlQ.containsKey(hashing)) {
				controlQ.put(hashing,1);
				if((hashing).equals(control)) {
					this.allCheck = true;
					System.out.println(temp);
					System.exit(0);
				}
				q.add(tupleDown);
				tree.addLeaf(root, tupleDown);
			} 
		}
		if(up == true) {
			String temp = "U" ;
			if(check) {
				temp = "U";
			} else {
				String x = (String) ((Tuple)root).y;
				temp = x.concat(temp);
			}
			Tuple<LinkedHashMap<Integer, Tuple<Integer, Integer>>, String> tupleUp = new Tuple<LinkedHashMap<Integer, Tuple<Integer, Integer>>, String>(upMap,temp) ;
			String hashing = checkFunc(upMap);
			if(!controlQ.containsKey(hashing)) {
				controlQ.put(hashing, 1);
				if((hashing).equals(control)) {
					allCheck = true;
					System.out.println(temp);
					System.exit(0);
				}
				q.add(tupleUp);
				tree.addLeaf(root, tupleUp);
			} 
		}
		if(left == true) {
			String temp = "L" ;
			if(check) {
				temp = "L";
			} else {
				String x = (String) ((Tuple)root).y;
				temp = x.concat(temp);
			}
			Tuple<LinkedHashMap<Integer, Tuple<Integer, Integer>>, String> tupleLeft = new Tuple<LinkedHashMap<Integer, Tuple<Integer, Integer>>, String>(leftMap,temp) ;
			String hashing = checkFunc(leftMap);
			if(!controlQ.containsKey(hashing)) {
				controlQ.put(hashing,1);
				if((hashing).equals(control)) {
					allCheck = true;
					System.out.println(temp);
					System.exit(0);
				}
				q.add(tupleLeft);
				tree.addLeaf(root, tupleLeft);
			}
		}
	}
}
