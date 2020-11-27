package com;

import java.util.*;
import java.text.DecimalFormat;

/**
 * @author Bekir Yıldırım
 */
public class BonusRunningAverage {
    private Double currentAverage = 0.0;
    private Integer populationSize = 0;
    private List<Double> population = new ArrayList<>();
    DecimalFormat newFormat = new DecimalFormat("#.###");

    /**
     * Default Constructor.
     */
    public BonusRunningAverage() {
        this.CalculateAverageSize();
    }

    /**
     * Explicit Value Constructor.
     */
    public BonusRunningAverage(List<Double> population) {
        this.population = population;
        this.CalculateAverageSize();
    }

    public void CalculateAverageSize(){
        this.populationSize = this.population.size();
        this.currentAverage = 0.0;
        if(this.populationSize == 0){}
        else {
            for(double e : this.population) this.currentAverage+=e;
            this.currentAverage/=this.populationSize;
            this.currentAverage = Double.valueOf(newFormat.format(this.currentAverage));
        }
    }

    /**
    * Copy Constructor.
    */
    public BonusRunningAverage(BonusRunningAverage lastAverage)
    {
        this.currentAverage = lastAverage.currentAverage;
        this.populationSize = lastAverage.populationSize;
        this.population = lastAverage.population;
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
    * Getter for list population
    */
    public List<Double> getPopulation() {
        return population;
    }

    /**
    * Adds elements to the population and returns the new average.
    */
    public Double addElements(List<Double> addedPopulation)
    {
        List<Double> newPopulation = new ArrayList<>();
        newPopulation.addAll(this.population);
        newPopulation.addAll(addedPopulation);
        this.population = newPopulation;
        this.CalculateAverageSize();
        return this.currentAverage;
    }

    /**
    * Removes elements to the population and returns the new average.
    */
    public Double removeElements(List<Double> removedPopulation)
    {
        List<Double> newPopulation = new ArrayList<>();
        newPopulation.addAll(this.population);
        for(double e : removedPopulation) newPopulation.remove(e);
        this.population = newPopulation;
        this.CalculateAverageSize();
        return this.currentAverage;
    }

    /**
     * Combines two running averages and returns a new running average
     */
    static public BonusRunningAverage combine(final BonusRunningAverage avg1, final BonusRunningAverage avg2)
    {
        List<Double> newPopulation = new ArrayList<>();
        newPopulation.addAll(avg1.getPopulation());
        newPopulation.addAll(avg2.getPopulation());
        return new BonusRunningAverage(newPopulation);
    }
}
