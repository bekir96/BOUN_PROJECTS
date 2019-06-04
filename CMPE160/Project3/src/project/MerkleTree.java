package project;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.security.NoSuchAlgorithmException;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Scanner;
import java.util.Stack;

import util.HashGeneration;

public class MerkleTree {
	private String path;
	private Node root;
	private List<List<Node>> listOfLists;
	private List<Integer> leavesNo;

	public MerkleTree(String path) {
		try {
			this.path = path;
			listOfLists = new ArrayList<List<Node>>();
			leavesNo = new LinkedList<Integer>();
			createTree();

		} catch (Exception e) {

		}

	}

	public void createTree() {
		try {
			File file = new File(this.path);
			Scanner sc = new Scanner(file);
			List<String> tempTxList = new ArrayList<String>();

			while (sc.hasNextLine()) {

				tempTxList.add(sc.nextLine());

			}

			sc.close();

			List<String> tempHashList = new ArrayList<String>();

			while (tempTxList.size() != 0) {

				try {
					tempHashList.add(HashGeneration.generateSHA256(new File(tempTxList.get(0))));

				} catch (NoSuchAlgorithmException | IOException e) {
					e.printStackTrace();
				}

				tempTxList.remove(0);

			}

			List<String> rootHash = getNewHashList(tempHashList);
			while (rootHash.size() != 1) {
				rootHash = getNewHashList(rootHash);

			}

			List<Node> lastHash = new ArrayList<Node>();
			this.root = new Node(rootHash.get(0));

			lastHash.add(this.root);
			this.listOfLists.add(lastHash);

			rearrangeTree();

		} catch (FileNotFoundException e) {

			System.out.println("File not found.");
		}

	}

	public List<String> getNewHashList(List<String> tempHashList) {

		List<String> rootHash = new ArrayList<String>();
		try {
			int index = 0;
			int size = tempHashList.size();

			List<Node> tempHash = new ArrayList<Node>();

			while (index < size) {

				String left = tempHashList.get(index);
				Node nodeL = new Node(left);
				index++;

				String right = "";
				Node nodeR = null;

				if (index != tempHashList.size()) {

					right = tempHashList.get(index);
					nodeR = new Node(right);

				} else {

				}

				String newHashValue = HashGeneration.generateSHA256(left + right);

				rootHash.add(newHashValue);
				Node upperNode = new Node(newHashValue);

				upperNode.setLeft(nodeL);
				upperNode.setRight(nodeR);

				tempHash.add(nodeL);
				tempHash.add(nodeR);

				index++;

			}

			this.listOfLists.add(tempHash);

		} catch (Exception e) {

		}

		return rootHash;

	}

	public void rearrangeTree() {

		int change = 0;
		int range = this.listOfLists.size();
		while (range > 1) {

			change = 0;

			while (change < this.listOfLists.get(range - 1).size()) {

				if (this.listOfLists.get(range - 1).get(change) == null) {

				} else {
					this.listOfLists.get(range - 1).get(change)
							.setLeft(this.listOfLists.get(range - 2).get(change * 2));
					this.listOfLists.get(range - 1).get(change)
							.setRight(this.listOfLists.get(range - 2).get(change * 2 + 1));

				}

				change++;

			}

			range--;
		}

	}

	public boolean checkAuthenticity(String checkPath) {
		boolean check = true;
		try {
			this.leavesNo.clear();
			File file = new File(checkPath);
			Scanner sc = new Scanner(file);
			List<String> tempCheckList = new ArrayList<String>();
			while (sc.hasNextLine()) {

				tempCheckList.add(sc.nextLine());

			}

			sc.close();

			int i = 0;
			while (i < tempCheckList.size()) {
				if (tempCheckList.get(i).isEmpty()) {

					tempCheckList.remove(i);
					i--;
				}
				i++;

			}

			int sizeHeight = this.listOfLists.size();
			int sizeCheck = tempCheckList.size();
			int control = 0;

			while (control < sizeCheck) {

				while (sizeHeight > 0) {
					int sizeLine = 0;
					while (sizeLine < this.listOfLists.get(sizeHeight - 1).size() && control < sizeCheck) {

						Node last = this.listOfLists.get(sizeHeight - 1).get(sizeLine);

						if (last == null) {
							control--;

						} else {

							String controlHash = this.listOfLists.get(sizeHeight - 1).get(sizeLine).getData();
							String metaHash = tempCheckList.get(control);

							if (!controlHash.equals(metaHash)) {
								if (sizeHeight == 1) {
									this.leavesNo.add(sizeLine);
								}
								check = false;
							}

						}
						control++;
						sizeLine++;

					}

					sizeHeight--;
				}
				control++;

			}

		} catch (FileNotFoundException e) {

			System.out.println("File not found.");
		}
		return check;

	}

	public ArrayList<Stack<String>> findCorruptChunks(String corruptPath) {

		ArrayList<Stack<String>> tempArray = new ArrayList<Stack<String>>();
		try {
			boolean check = checkAuthenticity(corruptPath);
			if (!check) {
				tempArray = stackCorrupt(this.root, this.leavesNo);
			}
		} catch (Exception e) {

		}

		return tempArray;
	}

	public ArrayList<Stack<String>> stackCorrupt(Node node, List<Integer> leavesNo) {

		ArrayList<Stack<String>> tempStack = new ArrayList<Stack<String>>();
		if (node == null) {

			return null;
		}
		for (int i = 0; i < this.leavesNo.size(); i++) {

			Stack<String> stackCo = new Stack<String>();

			int height = this.listOfLists.size();

			Node newNode = node;

			stackCo.add(newNode.getData());

			while (height > 1) {

				Node tempNode = newNode;

				if ((this.leavesNo.get(i) / (int) Math.pow(2, height - 2)) % 2 == 0) {

					newNode = tempNode.getLeft();
					stackCo.add(newNode.getData());

				} else if ((this.leavesNo.get(i) / (int) Math.pow(2, height - 2)) % 2 == 1) {

					newNode = tempNode.getRight();
					stackCo.add(newNode.getData());

				}

				height--;

			}

			tempStack.add(stackCo);

		}

		return tempStack;
	}

	public String getPath() {
		return path;
	}

	public void setPath(String path) {
		this.path = path;
	}

	public Node getRoot() {
		return root;
	}

	public void setRoot(Node root) {
		this.root = root;
	}

	public List<List<Node>> getListOfLists() {
		return listOfLists;
	}

	public void setListOfLists(List<List<Node>> listOfLists) {
		this.listOfLists = listOfLists;
	}

	public List<Integer> getLeavesNo() {
		return leavesNo;
	}

	public void setLeavesNo(List<Integer> leavesNo) {
		this.leavesNo = leavesNo;
	}

}