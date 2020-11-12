/* 
    REFERENCES: https://www.tutorialspoint.com/java/java_multithreading.htm
*/

class RunnableDemo implements Runnable {
    private Thread      _t;
    private String      _threadName;
    private HWMutex     _mutex;
    private int         _pid;
    
    RunnableDemo( String name, HWMutex hw, int threadId) {
        this._threadName = name;
        this._mutex = hw;
        this._pid = threadId;
        System.out.println("Creating " +  this._threadName );
    }
    
    public void run() {
        System.out.println("Running " +  this._threadName );
        for(int i = 0; i < 200; i++) {
            this._mutex.requestCS(this._pid);
            System.out.println("Thread: " + this._threadName + ", " + i);
            this._mutex.releaseCS(this._pid);
        }
                
        System.out.println("Thread " +  this._threadName + " exiting.");
    }
    
    public void start () {
        System.out.println("Starting " +  this._threadName );
        if (this._t == null) {
            this._t = new Thread (this, this._threadName);
            this._t.start ();
        }
    }
 }

class Main{
    public static void main(String[] args) {
        HWMutex mutex = new HWMutex();
        RunnableDemo R1 = new RunnableDemo( "Thread-1", mutex, 0);
        R1.start();
      
        RunnableDemo R2 = new RunnableDemo( "Thread-2", mutex, 1);
        R2.start();
    }
}