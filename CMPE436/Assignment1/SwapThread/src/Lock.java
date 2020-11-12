public interface Lock {
    public void requestCS(int pid); //may block // entry
    public void releaseCS(int pid); // exit
}