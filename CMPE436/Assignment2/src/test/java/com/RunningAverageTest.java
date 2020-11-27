package com;

import junitparams.JUnitParamsRunner;
import junitparams.Parameters;
import java.util.*;
import org.junit.*;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.junit.rules.ErrorCollector;	
// import org.junit.runners.Parameterized.Parameters;

import static org.junit.Assert.*;

@RunWith(JUnitParamsRunner.class)
public class RunningAverageTest 
{
    @Rule		
    public ErrorCollector collector = new ErrorCollector();

    private static final Object[] getEmptyClass(){
        return new Object[] {
            new RunningAverage()
        };
    }

    @Test
    @Parameters(method = "getEmptyClass")
    public void testConstructor(RunningAverage empty)
    {
        try{
            assertEquals("Population is not 0", (Object)0, empty.getPopulationSize());
        } catch (Throwable t) {					
            collector.addError(t);					
        }
        
        try{
            assertEquals("Average is not 0", (Object)0.0, empty.getCurrentAverage());
        } catch (Throwable t) {					
            collector.addError(t);					
        }
        
    }

    private static final Object[] getAddList() {
        return new Object[][] {
                new Object[][] {{4.0, 5.0}, {24.0/7}, {7}},
                new Object[][] {{4.0, 5.0 , 6.0}, {30.0/8}, {8}},
                new Object[][] {{2.0, 3.0, 5.0, 4.0, 11.0},{40.0/10},{10}}
        };
    }

    @Test
    @Parameters(method = "getAddList")
    public void testAdd(Object[] mNumber, Object[] mExpectedAverage, Object[] mExpectedPopulation){
        RunningAverage add = new RunningAverage(3.0, 5);
        List<Object> addedPopulation = Arrays.asList(mNumber);
        List<Object> cloned_addedPopulation = new ArrayList<Object>(addedPopulation);
        double newAverage;

        try{
            newAverage = add.addElements((List<Double>)(Object) addedPopulation);
            assertEquals("Return newAverage is not true", newAverage, (Object)add.getCurrentAverage());
        } catch (Throwable t) {					
            collector.addError(t);					
        }

        try{
            assertEquals("Average is not true", mExpectedAverage[0], (Object)add.getCurrentAverage());
        } catch (Throwable t) {					
            collector.addError(t);					
        }

        try{
            assertEquals("Population is not true", mExpectedPopulation[0], (Object)add.getPopulationSize());
        } catch (Throwable t) {					
            collector.addError(t);					
        }

        try{
            assertEquals("Contents of List is changed", cloned_addedPopulation, addedPopulation);
        } catch (Throwable t) {					
            collector.addError(t);					
        }

        List<Double> emptyPopulation = new ArrayList<>();
        try{
            double currentAverage = add.addElements(emptyPopulation);
            assertEquals("EMPTY: Average is not true", (Object) add.getCurrentAverage(), (Object) currentAverage);
        } catch (Throwable t) {					
            collector.addError(t);					
        }
    }

    private static final Object[] getRemoveList() {
        return new Object[][] {
                new Object[][] {{2.0, 1.0}, {4.0}, {3}},
                new Object[][] {{2.0, 1.0 , 4.0}, {4.0}, {2}},
                new Object[][] {{1.0, 5.0, 2.0, 3.0, 1.0},{0.0},{0}}
        };
    }

    @Test
    @Parameters(method = "getRemoveList")
    public void testRemove(Object[] mNumber, Object[] mExpectedAverage, Object[] mExpectedPopulation){
        RunningAverage remove = new RunningAverage(3.0, 5);
        List<Object> removedPopulation = Arrays.asList(mNumber);
        List<Object> cloned_removedPopulation = new ArrayList<Object>(removedPopulation);
        double newAverage;

        try{
            newAverage = remove.removeElements((List<Double>)(Object) removedPopulation);
            assertEquals("Return newAverage is not true", newAverage, (Object)remove.getCurrentAverage());
        } catch (Throwable t) {					
            collector.addError(t);					
        }

        try{
            assertEquals("Average is not true", mExpectedAverage[0], (Object)remove.getCurrentAverage());
        } catch (Throwable t) {					
            collector.addError(t);					
        }

        try{
            assertEquals("Population is not true", mExpectedPopulation[0], (Object)remove.getPopulationSize());
        } catch (Throwable t) {					
            collector.addError(t);					
        }

        try{
            assertEquals("Contents of List is changed", cloned_removedPopulation, removedPopulation);
        } catch (Throwable t) {					
            collector.addError(t);					
        }

        List<Double> emptyPopulation = new ArrayList<>();
        try{
            double currentAverage = remove.removeElements(emptyPopulation);
            assertEquals("EMPTY: Average is not true", (Object) remove.getCurrentAverage(), (Object) currentAverage);
        } catch (Throwable t) {					
            collector.addError(t);					
        }
    }

    private static final Object[] getInitialPopulationNegativeClass(){
        return new Object[] {
            new RunningAverage(1.0, -4),
            new RunningAverage(2.0, -5),
            new RunningAverage(4.0, -4)
        };
    }

    @Test
    @Parameters(method = "getInitialPopulationNegativeClass")
    public void testInitialPopulationNegativeConstructor(RunningAverage negative)
    {
        try{
            assertFalse("Initial population size can be negative", negative.getPopulationSize() < 0);
        } catch (Throwable t) {					
            collector.addError(t);					
        }
    }

    private static final Object[] getPopulationNegativeList() {
        return new Object[] {
                new Object[] {2.0, 1.0},
                new Object[] {2.0, 1.0 , 4.0},
                new Object[] {2.0, 4.0, 5.0, 3.0, 2.0}
        };
    }

    @Test
    @Parameters(method = "getPopulationNegativeList")
    public void testPopulationNegative(Object[] mNumber){
        RunningAverage remove = new RunningAverage();
        List<Object> removedPopulation = Arrays.asList(mNumber);
        double newAverage;
        try{
            newAverage = remove.removeElements((List<Double>)(Object) removedPopulation);
            assertFalse("Population size can be negative", remove.getPopulationSize() < 0);
        } catch (Throwable t) {					
            collector.addError(t);					
        }

    }

    private static final Object[] getCombineClass(){
        return new Object[] {
            new Object[][] {{new RunningAverage(2.0, 4), new RunningAverage(3.0, 5)}, {23.0/9, 9}},
            new Object[][] {{new RunningAverage(3.0, 2), new RunningAverage(2.0, 4)}, {14.0/6, 6}},
            new Object[][] {{new RunningAverage(4.0, 6), new RunningAverage(3.0, 5)}, {39.0/11, 11}}
        };
    }

    @Test
    @Parameters(method = "getCombineClass")
    public void testCombine(Object[] mNumber, Object[] mExpectedAverage){
        Object returnObject = new Object();
        try{
            returnObject = RunningAverage.combine((RunningAverage)mNumber[0], (RunningAverage)mNumber[1]);
            assertFalse("RunningAverage object is not created", !(returnObject instanceof RunningAverage));
        } catch (Throwable t) {					
            collector.addError(t);					
        }

        RunningAverage temp = (RunningAverage) returnObject;
        
        try{
            assertEquals("Average is not true", mExpectedAverage[0], temp.getCurrentAverage());
        } catch (Throwable t) {					
            collector.addError(t);					
        }

        try{
            assertEquals("Population is not true", mExpectedAverage[1], temp.getPopulationSize());
        } catch (Throwable t) {					
            collector.addError(t);					
        }
    }
}