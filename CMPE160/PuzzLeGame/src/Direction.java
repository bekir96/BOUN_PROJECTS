package puzzleGame;


public enum Direction {

    UP(0, -1), DOWN(0, 1), LEFT(-1, 0), RIGHT(1, 0);

    private Direction(float x, float y) {
        this.x = x;
        this.y = y;
    }

    private float x;
    private float y;

    public float getX() {
        return x;
    }
    public float getY() {
        return y;
    }

}

	