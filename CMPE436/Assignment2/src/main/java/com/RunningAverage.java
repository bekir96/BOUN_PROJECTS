package com;
import java.util.*;

/**
* @author Yavuz Koroglu
*/
public class RunningAverage
{
    private Double currentAverage = 0.0;
    private Integer populationSize = 0;
    /**
    * Default Constructor.
    */
    public RunningAverage()
    {
        this.currentAverage = 0.0;
        this.populationSize = 1;
    }

    /**
    * Explicit Value Constructor.
    */
    public RunningAverage(double lastAverage, int lastPopulationSize)
    {
        this.currentAverage = lastAverage;
        this.populationSize = lastPopulationSize;
    }

    /**
    * Copy Constructor.
    */
    public RunningAverage(RunningAverage lastAverage)
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
            return 0.0;
        }
        double sum = this.currentAverage * this.populationSize;
        for (double element : removedPopulation) {
            sum -= element;
            this.populationSize--;
        }

        this.currentAverage = sum / this.populationSize;

        return this.currentAverage;
    }

    /**
    * Combines two running averages and returns a new running average
    */
    static public RunningAverage combine(final RunningAverage avg1, final RunningAverage avg2)
    {
        return new RunningAverage
        (
            avg1.getCurrentAverage() * avg1.getPopulationSize() + avg2.getCurrentAverage() * avg2.getPopulationSize()
            / (avg1.getPopulationSize() + avg2.getPopulationSize()),
            avg1.getPopulationSize() + avg2.getPopulationSize()
        );
    }
}