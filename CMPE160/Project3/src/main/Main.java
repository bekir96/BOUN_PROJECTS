package main;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.net.URI;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;
import java.util.Scanner;
import java.util.Stack;

import project.MerkleTree;

public class Main {

	public static void main(String[] args) {
		try {
			MerkleTree m0 = new MerkleTree("data/1.txt");
			String hash = m0.getRoot().getLeft().getLeft().getLeft().getLeft().getData();
			System.out.println(hash);

			boolean valid = m0.checkAuthenticity("data/3meta.txt");
			System.out.println(valid);

			// The following just is an example for you to see the usage.
			// Although there is none in reality, assume that there are two corrupt chunks
			// in this example.
			ArrayList<Stack<String>> corrupts = m0.findCorruptChunks("data/9meta.txt");

			System.out.println("Corrupt hash of first corrupt chunk is: " + corrupts.get(0).pop());
			System.out.println("Corrupt hash of second corrupt chunk is: " + corrupts.get(1).pop());
			download("secondaryPart/data/download_from_trusted.txt");

		}

		catch (NullPointerException e) {

			download("secondaryPart/data/download_from_trusted.txt");

		}

	}

	public static void download(String path) {
		try {
			File file = new File(path);
			Scanner sc = new Scanner(file);

			List<List<String>> allDownload = new ArrayList<List<String>>();
			List<String> tempTxList = new ArrayList<String>();
			int count = 0;
			while (sc.hasNextLine()) {

				String h = sc.nextLine();
				if (h.contains("meta")) {
					tempTxList.add(h);
					count++;

				} else if (h.contains("alt")) {
					tempTxList.add(h);
					count++;

				} else if (h.contains(".txt")) {
					tempTxList.add(h);
					count++;
				}

				if (count == 3) {
					allDownload.add(tempTxList);
					count = 0;
					tempTxList = new ArrayList<String>();
				}

			}

			sc.close();
			allDownloadFile(allDownload);

		} catch (FileNotFoundException e) {

			System.out.println("File not found.");

		}

	}

	public static void allDownloadFile(List<List<String>> allDownload) {
		try {
			int size = allDownload.size();
			for (int i = 0; i < size; i++) {

				String temp = "";
				String tempAlt = "";
				Queue<Integer> corruptLeaves = new LinkedList<Integer>();

				for (int j = 0; j < 3; j++) {

					URL url = new URL(allDownload.get(i).get(j));
					Scanner urlSc = new Scanner(url.openStream());

					List<String> tempUrlList = new ArrayList<String>();
					String text = "";

					if (j == 0) {
						while (urlSc.hasNextLine()) {

							tempUrlList.add(urlSc.nextLine());

						}

						int range = tempUrlList.size();
						for (int control = 0; control < range; control++) {

							text += tempUrlList.get(control) + "\n";

						}

						String exampleName = fileName(allDownload.get(i).get(j));

						String fileCopy = "secondaryPart/data/" + exampleName + ".txt";
						temp = fileCopy;

						File f = new File(fileCopy);
						if (!f.exists()) {

							f.createNewFile();
						}

						BufferedWriter out = new BufferedWriter(new FileWriter(fileCopy));
						out.write(text);
						out.close();
					}
					if (j == 1) {

						while (urlSc.hasNextLine()) {

							tempUrlList.add(urlSc.nextLine());

						}

						int range = tempUrlList.size();
						for (int control = 0; control < range; control++) {

							text += tempUrlList.get(control) + "\n";

						}

						String exampleName = fileName(allDownload.get(i).get(j));
						tempAlt = exampleName;

						String fileCopy = "secondaryPart/data/" + exampleName + ".txt";
						File f = new File(fileCopy);
						if (!f.exists()) {

							f.createNewFile();
						}

						BufferedWriter out = new BufferedWriter(new FileWriter(fileCopy));
						out.write(text);
						out.close();

						File file = new File(fileCopy);
						Scanner scanner = new Scanner(file);

						List<String> tempTxList = new ArrayList<String>();
						while (scanner.hasNextLine()) {

							tempTxList.add(scanner.nextLine());

						}

						scanner.close();
						int sizeUrl = tempTxList.size();
						int rangeUrl = 0;

						String temp2 = "";
						String fileCopy2 = "secondaryPart/data/split/" + exampleName;

						File files = new File(fileCopy2);
						if (!files.exists()) {
							if (files.mkdirs()) {

							} else {

							}
						}

						while (rangeUrl < sizeUrl) {

							String splitName = splitName(tempTxList.get(rangeUrl));

							String fileCopySplit = "secondaryPart/data/split/" + exampleName + "/" + splitName;
							temp2 += fileCopySplit + "\n";

							File f2 = new File(fileCopySplit);
							if (!f2.exists()) {
								urlDownload(tempTxList.get(rangeUrl), fileCopySplit);
							} else {
								f2.delete();
								urlDownload(tempTxList.get(rangeUrl), fileCopySplit);
							}

							rangeUrl++;
						}

						BufferedWriter out3 = new BufferedWriter(new FileWriter(fileCopy));
						out3.write(temp2);
						out3.close();

						MerkleTree downloadTree = new MerkleTree(fileCopy);
						downloadTree.checkAuthenticity(temp);
						corruptLeaves.addAll(downloadTree.getLeavesNo());
					}
					if (j == 2) {
						while (urlSc.hasNextLine()) {

							tempUrlList.add(urlSc.nextLine());

						}

						int range = tempUrlList.size();
						for (int control = 0; control < range; control++) {

							text += tempUrlList.get(control) + "\n";

						}
						String exampleName = fileName(allDownload.get(i).get(j));
						String fileCopy = "secondaryPart/data/" + exampleName + ".txt";

						File f = new File(fileCopy);
						if (!f.exists()) {

							f.createNewFile();
						}

						BufferedWriter out = new BufferedWriter(new FileWriter(fileCopy));
						out.write(text);
						out.close();
						File file = new File(fileCopy);
						Scanner scanner = new Scanner(file);
						List<String> tempTxList = new ArrayList<String>();

						while (scanner.hasNextLine()) {

							tempTxList.add(scanner.nextLine());

						}

						scanner.close();
						int sizeUrl = tempTxList.size();
						int rangeUrl = 0;

						String temp2 = "";
						while (rangeUrl < sizeUrl) {
							String splitName = splitName(tempTxList.get(rangeUrl));

							if (!corruptLeaves.isEmpty()) {
								if (corruptLeaves.peek() == rangeUrl) {

									splitName = splitName(tempTxList.get(rangeUrl));
									String fileCopyTemp = "secondaryPart/data/split/" + tempAlt + "/" + splitName;

									File fileDelete = new File(fileCopyTemp);
									fileDelete.delete();
									urlDownload(tempTxList.get(rangeUrl), fileCopyTemp);

									corruptLeaves.poll();
								}

							}

							String fileCopy2 = "secondaryPart/data/split/" + tempAlt + "/" + splitName;
							temp2 += fileCopy2 + "\n";

							rangeUrl++;
						}

						BufferedWriter out3 = new BufferedWriter(new FileWriter(fileCopy));
						out3.write(temp2);
						out3.close();

					}

					urlSc.close();
				}

			}

		} catch (IOException e) {

			System.out.println("File cannot created.");
		}

	}

	public static void urlDownload(String url, String fileName) {
		try (InputStream in = URI.create(url).toURL().openStream()) {
			Files.copy(in, Paths.get(fileName));
		} catch (Exception e) {

			System.out.println("Url or file name has not found.");
		}

	}

	public static String fileName(String findPath) {

		String tempPath = findPath;
		Stack<Integer> slashChar = new Stack<Integer>();
		Stack<Integer> dotChar = new Stack<Integer>();
		for (int charL = 0; charL < tempPath.length(); charL++) {
			char c = tempPath.charAt(charL);
			if (c == '/') {

				slashChar.add(charL);

			} else if (c == '.') {

				dotChar.add(charL);

			}
		}

		String exampleName = tempPath.substring((slashChar.pop() + 1), dotChar.pop());
		return exampleName;
	}

	public static String splitName(String findPath) {

		String tempPath = findPath;
		Stack<Integer> slashChar = new Stack<Integer>();
		for (int charL = 0; charL < tempPath.length(); charL++) {

			char c = tempPath.charAt(charL);
			if (c == '/') {

				slashChar.add(charL);

			}

		}

		String splitName = tempPath.substring((slashChar.pop() + 1));
		return splitName;
	}

}