class HWMutex implements Lock {
    TestAndSet lockFlag = new TestAndSet();
    volatile int lock = 0;

    @Override
    public void requestCS(int i) {
        while(true){
            while(lock == 1-i);
            if(lockFlag.testAndSet(1) != 1){
                break;
            }
        }
    }

    @Override
    public void releaseCS(int i) {
        lock = 1-i;
        lockFlag.testAndSet(0);
    }
} 