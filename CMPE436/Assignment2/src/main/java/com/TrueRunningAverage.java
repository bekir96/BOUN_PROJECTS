package com;
import java.util.*;

/**
* @author Bekir Yıldırım
*/
public class TrueRunningAverage
{
    private Double currentAverage;
    private Integer populationSize;
    /**
    * Default Constructor.
    */
    public TrueRunningAverage()
    {
        this.currentAverage = 0.0;
        this.populationSize = 0;
    }

    /**
     * Explicit Value Constructor.
     */
    public TrueRunningAverage(double lastAverage, int lastPopulationSize)
    {
        this.currentAverage = lastAverage;
        this.populationSize = lastPopulationSize;
        if(lastPopulationSize < 0){
            throw new IllegalArgumentException();
        }
    }

    /**
    * Copy Constructor.
    */
    public TrueRunningAverage(TrueRunningAverage lastAverage)
    {
        this.currentAverage = lastAverage.currentAverage;
        this.populationSize = lastAverage.populationSize;
    }

    /**
    * Getter for currentAverage
    */
    public Double getCurrentAverage()
    {
        return currentAverage;
    }

    /**
    * Getter for populationSize
    */
    public Integer getPopulationSize()
    {
        return populationSize;
    }

    /**
    * Adds elements to the population and returns the new average.
    */
    public Double addElements(List<Double> addedPopulation)
    {
        if (addedPopulation.size() == 0 || addedPopulation == null) {
            return this.currentAverage;
        }

        double sum = this.currentAverage * this.populationSize;
        for (double element : addedPopulation) {
            sum += element;
            this.populationSize++;
        }

        this.currentAverage = sum / this.populationSize;

        return this.currentAverage;
    }

    /**
    * Removes elements to the population and returns the new average.
    */
    public Double removeElements(List<Double> removedPopulation)
    {
        if (removedPopulation.size() == 0 || removedPopulation == null) {
            return this.currentAverage;
        }
        double sum = this.currentAverage * this.populationSize;
        boolean control = true;
        for (double element : removedPopulation) {
            if(this.populationSize == 0){
                control = false;
                break;
            }
            sum -= element;
            this.populationSize--;
        }
        if(this.populationSize == 0){
            control = false;
        }

        if(control){
            this.currentAverage = sum / this.populationSize;
        } else {
            this.currentAverage = 0.0;
        }
        return this.currentAverage;
    }

    /**
     * Combines two running averages and returns a new running average
     */
    static public TrueRunningAverage combine(final TrueRunningAverage avg1, final TrueRunningAverage avg2)
    {
        return new TrueRunningAverage
        (
            (avg1.getCurrentAverage() * avg1.getPopulationSize() + avg2.getCurrentAverage() * avg2.getPopulationSize())
            / (avg1.getPopulationSize() + avg2.getPopulationSize()),
            avg1.getPopulationSize() + avg2.getPopulationSize()
        );
    }
}
