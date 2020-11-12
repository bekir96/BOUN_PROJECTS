public class TestAndSet {
    int myValue = -1; // lock
   // atomic function below
    public synchronized int testAndSet(int newValue) {
        int oldValue = myValue;
        myValue = newValue;
        return oldValue;
    }
}