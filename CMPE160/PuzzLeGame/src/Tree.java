package puzzleGame;

import java.util.ArrayList;
import java.util.HashMap;

public class Tree<T> {

  private T head;
  
  private ArrayList<Tree<T>> leafs = new ArrayList<Tree<T>>();

  private Tree<T> parent = null;

  private HashMap<T, Tree<T>> locate = new HashMap<T, Tree<T>>();

  public Tree(T head) {
    this.head = head;
    locate.put(head, this);
  }
 
  public void addLeaf(T root, T leaf) {
    if (locate.containsKey(root)) {
      locate.get(root).addLeaf(leaf);
    } else {
      addLeaf(root).addLeaf(leaf);
    }
  }

  public Tree<T> addLeaf(T leaf) {
    Tree<T> t = new Tree<T>(leaf);
    leafs.add(t);
    t.parent = this;
    t.locate = this.locate;
    locate.put(leaf, t);
    return t;
  }

  public Tree<T> setAsParent(T parentRoot) {
    Tree<T> t = new Tree<T>(parentRoot);
    t.leafs.add(this);
    this.parent = t;
    t.locate = this.locate;
    t.locate.put(head, this);
    t.locate.put(parentRoot, t);
    return t;
  }

  public T getHead() {
    return head;
  }

  public Tree<T> getTree(T element) {
    return locate.get(element);
  }

  public Tree<T> getParent() {
    return parent;
  }
}