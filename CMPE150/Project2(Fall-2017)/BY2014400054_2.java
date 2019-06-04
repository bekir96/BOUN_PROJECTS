import java.util.*;

public class BY2014400054 {

	public static void main(String[] args) {
		Scanner console = new Scanner(System.in);
		System.out.println("   Welcome to MARS Interviewing Systems");
		System.out.print("Can I learn your name?");
		String name = console.nextLine();               // name represents user's name. //
		String first = name.substring(0, 1);			// first represents first letter of user's name. //
		String last = name.substring(1);				// last represents other letters of user's name. //
		last = last.toLowerCase();						
		first = first.toUpperCase();
		String aName = first + last;					// aName represents upper case of first letter and also other letters of user's name. //
		System.out.print("Hello " + aName + ". How old are you?");
		int age = console.nextInt();					// age represents user's age. //
		console.nextLine();								
		if (age < 18) {									// this if else statements control user's age above or under 18. //
			System.out.print("Your age is not allowed to hire for this job.");
		} else {
			System.out.print("For which position are you applying?");
			String jobRole = console.nextLine();
			if (jobRole.equalsIgnoreCase("Software Engineer")) {		// this if else statement determines which job role users want. //
				softwareEngineer(aName);
			} else if (jobRole.equalsIgnoreCase("Accountant")) {
				accountant(aName);
			} else if (jobRole.equalsIgnoreCase("Academic")) {
				academic(aName);
			}
		}

	}

	public static void softwareEngineer(String softName) {			// this method eases to write asking questions for users who want to software engineer. //
		System.out.print("Great. Do you have a university degree?");
		Scanner console = new Scanner(System.in);
		String answer = console.nextLine();							// answer represents user's input which answer yes-no question. //
		if (answer.equalsIgnoreCase("no")) {						// this if else statement determines user's answer for yes-no question. //
			System.out.println("Thank you for applying.");

		} else if (answer.equalsIgnoreCase("yes")) {
			System.out.print("In which field?");
			String field = console.nextLine();
			if (field.equalsIgnoreCase("Computer Engineering") || field.equalsIgnoreCase("Software Engineering")		//this if else statement determines graduate field for the field which is desired.//
					|| field.equalsIgnoreCase("Computer Science")) {
				knowProgram(softName);

			} else {
				System.out.println("You don't have the skills we're looking for this job.");
			}
		}

	}

	public static void accountant(String accName) {					// this method eases to write asking questions for users who want to accountant. //
		System.out.print("Great. Do you have a university degree?");
		Scanner console = new Scanner(System.in);
		String answer = console.nextLine();							// answer represents user's input which answer yes-no question. //	
		if (answer.equalsIgnoreCase("no")) {						// this if else statement determines user's answer for yes-no question. //
			System.out.println("You should have university degree for this job.");

		} else if (answer.equalsIgnoreCase("yes")) {
			System.out.print("In which field?");
			String field = console.nextLine();						// field represents what field user graduated from. //
			if (field.equalsIgnoreCase("Accounting") || field.equalsIgnoreCase("Accounting Degree")) {		//this if else statement determines graduate field for the field which is desired.//
				System.out.print("Do you know Excel well?");
				String excel = console.nextLine();					// excel represents user's input which answer yes-no question. //	
				if (excel.equalsIgnoreCase("Yes")) {				// this if else statement determines user's answer for yes-no question. //
					System.out.print("Do you speak English?");
					String englishAns = console.nextLine();			// englishAns represents user's input which answer yes-no question. //
					if (englishAns.equalsIgnoreCase("No")) {		// this if else statement determines user's answer for yes-no question. //
						System.out.print("Do you have a friend who can translate for you?");
						String tAnswer = console.nextLine();		// tAnswer represents user's input which answer yes-no question. //	
						if (tAnswer.equalsIgnoreCase("Yes")) {		// this if else statement determines user's answer for yes-no question. //
							questAcc(accName);

						} else if (tAnswer.equalsIgnoreCase("No")) {
							System.out.println("Sorry " + accName
									+ ". You should speak English or have r have a friend who can translate for you for this job.");
						}
					} else if (answer.equalsIgnoreCase("Yes")) {
						questAcc(accName);
					}

				} else if (excel.equalsIgnoreCase("No")) {
					System.out.println("Sorry " + accName + ". You should know Excel well for this job.");
				}

			} else {
				System.out.println("Sorry " + accName + ". You should have a university degree for this job.");
			}
		}

	}

	public static void academic(String acaName) {				// this method eases to write asking questions for users who want to academic. //
		Scanner console = new Scanner(System.in);
		System.out.print("Do you speak English?");
		String answer = console.nextLine();						// answer represents user's input which answer yes-no question. //
		if (answer.equalsIgnoreCase("No")) {
			System.out.println("Sorry " + acaName + ". You should speak English for this job.");

		} else if (answer.equalsIgnoreCase("Yes")) {			// this if else statement determines user's answer for yes-no question. //
			System.out.print("How many papers do you publish? ");
			int paper = console.nextInt();						// paper represents how many paper user publish.//
			console.nextLine();
			if (paper < 3) {									// this if else statement determine paper's number above or under 3. //
				if ((3 - paper) <= 1) {							// this if else statement determine paper's number that should be published odd or even. //
					System.out.println(
							"Sorry " + acaName + ". You should publish " + (3 - paper) + " more paper for this job.");
				} else {
					System.out.println(
							"Sorry " + acaName + ". You should publish " + (3 - paper) + " more papers for this job.");
				}

			} else {
				System.out.print("Do you love to teach?");
				String teachAns = console.nextLine();			// teachAns represents user's input which answer yes-no question. //	
				if (teachAns.equalsIgnoreCase("Yes")) {			// this if else statement determines user's answer for yes-no question. //
					military(acaName);
				} else if (teachAns.equalsIgnoreCase("No")) {
					System.out.println("Sorry " + acaName + ". You should love to teach for this job.");
				}
			}

		}

	}

	public static void knowProgram(String knowName) {	// this method eases to write asking other questions for users who want to software engineer. //
		Scanner console = new Scanner(System.in);
		int countYesNo = 0;						// countYesNo represents how many 'Yes' input user write to ask yes-no question. //
		System.out.print("Do you know how to program in Java?");
		String yesNo1 = console.nextLine();				// yesNo1 represents user's input which answer yes-no question. //	
		System.out.print("Do you know how to program in C?");
		String yesNo2 = console.nextLine();				// yesNo2 represents user's input which answer yes-no question. //	
		System.out.print("Do you know how to program in Prolog?");
		String yesNo3 = console.nextLine();				// yesNo3 represents user's input which answer yes-no question. //	
		System.out.print("Do you know how to program in Python?");
		String yesNo4 = console.nextLine();				// yesNo4 represents user's input which answer yes-no question. //	
		if (yesNo1.equalsIgnoreCase("Yes")) {			// this if else statement determines user's answer for yes-no question. //
			countYesNo++;

		}
		if (yesNo2.equalsIgnoreCase("Yes")) {			// this if else statement determines user's answer for yes-no question. //
			countYesNo++;
		}
		if (yesNo3.equalsIgnoreCase("Yes")) {			// this if else statement determines user's answer for yes-no question. //
			countYesNo++;

		}
		if (yesNo4.equalsIgnoreCase("Yes")) {			// this if else statement determines user's answer for yes-no question. //
			countYesNo++;

		}
		if (countYesNo < 2) {							// this if else statement determines countYesNo's number above or under 2. //
			System.out
					.println("Sorry " + knowName + ". You should know at least two programming languages for this job");
		} else if (countYesNo == 2 || countYesNo == 3) {			// this if else statement determines countYesNo's number to equal 2 or 3. //
			System.out.print("Great. How many years do you work as a software engineer?");
			int workYear = console.nextInt();					// workYear represents how many years user work as a software engineer. //
			console.nextLine();
			if (workYear < 3) {								// this if else statement determines workYear's number above or under 3. //
				System.out.print("Do you have a graduate degree in software engineering?");
				String yesNo5 = console.nextLine();					// yesNo5 represents user's input which answer yes-no question. //			
				if (yesNo5.equalsIgnoreCase("Yes")) {			// this if else statement determines user's answer for yes-no question. //
					military(knowName);
				} else if (yesNo5.equalsIgnoreCase("No")) {
					System.out.println(
							"Sorry " + knowName + ". You should have a graduate degree in software engineering.");
				}
			} else {
				military(knowName);

			}

		} else {
			System.out.print("Awesome. How many years do you work as a software engineer?");
			int workYear = console.nextInt();
			console.nextLine();
			if (workYear < 3) {
				System.out.print("Do you have a graduate degree in software engineering?");
				String yesNo6 = console.nextLine();			// yesNo6 represents user's input which answer yes-no question. //	
				if (yesNo6.equalsIgnoreCase("Yes")) {		// this if else statement determines user's answer for yes-no question. //
					military(knowName);
				} else if (yesNo6.equalsIgnoreCase("No")) {
					System.out.println(
							"Sorry " + knowName + ". You should have a graduate degree in software engineering.");
				}
			} else {
				military(knowName);

			}
		}

	}


	public static void military(String miliName) {			// this method eases to write asking questions for users to determine military statement. //
		Scanner console = new Scanner(System.in);
		System.out.print("Are you a male?");
		String gender = console.nextLine();					// gender represents user's input which answer yes-no question. //
		if (gender.equalsIgnoreCase("Yes")) {				// this if else statement determines user's answer for yes-no question. //
			System.out.print("Did you complete your military service?");
			String answer = console.nextLine();				// answer represents user's input which answer yes-no question. //	
			if (answer.equalsIgnoreCase("Yes")) {			// this if else statement determines user's answer for yes-no question. //
				System.out.println("Congratulations " + miliName + "! You got the job!");
			} else if (answer.equalsIgnoreCase("No")) {		
				System.out.println("Sorry " + miliName + ". You should complete your military service for this job.");
			}

		} else if (gender.equalsIgnoreCase("No")) {
			System.out.println("Congratulations " + miliName + "! You got the job!");
		}

	}

	public static void questAcc(String questName) {			// this method eases to write asking other questions for users who want to accountant. //
		Scanner console = new Scanner(System.in);
		System.out.print("How many people working do you know in the company?");
		int workingPeople = console.nextInt();				// workingPeople represents how many people working user know in the company. //
		console.nextLine();
		if (workingPeople < 2) {							// this if else statement determines workingPeople's number above or under 2. // 
			System.out.println(
					"Sorry " + questName + ". You should know at least two people who already working in the company.");

		} else {
			System.out.print("Do you have a driving license?");
			String licenseAns = console.nextLine();			// licenseAns represents user's input which answer yes-no question. //
			if (licenseAns.equalsIgnoreCase("Yes")) {		// this if else statement determines user's answer for yes-no question. //
				military(questName);
			} else if (licenseAns.equalsIgnoreCase("No")) {
				System.out.println("Sorry " + questName + ". You should have a driving license.");
			}
		}
	}

}
