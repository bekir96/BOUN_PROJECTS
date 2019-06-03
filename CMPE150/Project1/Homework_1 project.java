public class Project {

	public static void main(String[] args) {
		writingAltCizgi(12);
		writingDollar(13);
		writingSpace1();
		writingSpace2();
		line2(8,7);
		line3(5,9);
		line4(4,2);
		line5(3,1);
		line6(2,1);
	}
	public static void writingAltCizgi(int count){
		for(int i=1 ; i<= count ; i++){
			System.out.print("_");
		}
	}
	public static void writingDollar(int count){
		for(int i=1 ; i<= count ; i++){
			System.out.print("$");
		}
	}
	public static void writingSpace1(){
		System.out.print(" ");
	}
	public static void writingSpace2(){
		System.out.println(" ");
	}
	public static void line2(int countAltCizgi, int countDollar){
		writingAltCizgi(countAltCizgi);
		writingDollar(countDollar);
		writingSpace1();
		for(int i=1 ; i<=countAltCizgi+1 ; i++){
			System.out.print("_");
		}
		for(int i=1 ; i<=countDollar-4 ; i++){
			System.out.print("$");
		}
		writingSpace2();
	}
	public static void line3(int countAltCizgi, int countDollar){
		writingAltCizgi(countAltCizgi);
		writingDollar(countDollar);
		writingSpace1();
		for(int i=1 ; i<=countAltCizgi*2+1 ; i++){
			System.out.print("_");
		}
		writingSpace1();
		for(int i=1 ; i<=countDollar-5 ; i++){
			System.out.print("$");
		}
		writingSpace2();
	}
	public static void line4(int countAltCizgi, int countDollar){
		writingAltCizgi(countAltCizgi);
		writingDollar(countDollar);
		for(int i=1 ; i<=countAltCizgi/4 ; i++){
			System.out.print("_");
		}
		for(int i=1 ; i<=countDollar+1 ; i++){
			System.out.print("$");
		}
		writingAltCizgi(countAltCizgi);
		writingDollar(countDollar);
		writingSpace1();
		for(int i=1 ; i<=countAltCizgi*2 ; i++){
			System.out.print("_");
		}
		writingSpace1();
		for(int i=1 ; i<=countDollar/2 ; i++){
			System.out.print("$");
		}
		for(int i=1 ; i<=countAltCizgi-1 ; i++){
			System.out.print("_");
		}
		writingDollar(countDollar);
		writingSpace2();
	}
	public static void line5(int countAltCizgi, int countDollar){
		writingAltCizgi(countAltCizgi);
		writingDollar(countDollar);
		writingAltCizgi(countAltCizgi);
		writingDollar(countDollar);
		for(int i=1 ; i<=countAltCizgi*3-1 ; i++){
			System.out.print("_");
		}
		writingDollar(countDollar);
		writingSpace1();
		for(int i=1 ; i<=countAltCizgi*2 ; i++){
			System.out.print("_");
		}
		writingSpace1();
		writingDollar(countDollar);
		for(int i=1 ; i<=countAltCizgi*2 ; i++){
			System.out.print("_");
		}
		for(int i=1 ; i<=countDollar*2 ; i++){
			System.out.print("$");
		}
		writingSpace2();
	}
	public static void line6(int countAltCizgi, int countDollar){
		writingAltCizgi(countAltCizgi);
		writingDollar(countDollar);
		for(int i=1 ; i<=countAltCizgi+1 ; i++){
			System.out.print("_");
		}
		writingDollar(countDollar);
		writingSpace1();
		for(int i=1 ; i<=countAltCizgi*4+1 ; i++){
			System.out.print("_");
		}
		writingSpace1();
		for(int i=1 ; i<=countDollar*8 ; i++){
			System.out.print("$");
		}
		for(int i=1 ; i<=countAltCizgi*4-1 ; i++){
			System.out.print("_");
		}
		for(int i=1 ; i<=countDollar*2 ; i++){
			System.out.print("$");
		}
		writingSpace2();
	}
}
	