public class Synch implements Lock{
    boolean wantCS[] = {false, false, true}; // Last element is lock.

    // swap two memory locations in one atomic step
    public static synchronized void swap(boolean[] array, int i){
        boolean temp = array[i];
        array[i] = array[array.length-1];
        array[array.length-1] = temp;
    }

    @Override
    public void requestCS(int i) {
        while(true){
            Synch.swap(wantCS, i);
            if(wantCS[i]) break;
        }
    }

    @Override
    public void releaseCS(int i) {
        Synch.swap(wantCS, i);
    }
} 