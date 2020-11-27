package com;

import junitparams.JUnitParamsRunner;
import junitparams.Parameters;
import java.util.*;
import org.junit.*;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.junit.rules.ErrorCollector;	
import java.text.DecimalFormat;
// import org.junit.runners.Parameterized.Parameters;

import static org.junit.Assert.*;

@RunWith(JUnitParamsRunner.class)
public class BonusRunningAverageTest 
{
    @Rule		
    public ErrorCollector collector = new ErrorCollector();
    DecimalFormat newFormat = new DecimalFormat("#.###");

    private static final Object[] getEmptyClass(){
        return new Object[] {
            new BonusRunningAverage()
        };
    }

    @Test
    @Parameters(method = "getEmptyClass")
    public void testConstructor(BonusRunningAverage empty)
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
                new Object[][] {{2.0, 6.0, 4.0, 1.0, 2.0}, {4.0, 5.0}, {24.0/7}, {7}},
                new Object[][] {{4.0, 3.0, 8.0}, {4.0, 5.0 , 6.0}, {30.0/6}, {6}},
                new Object[][] {{15.0}, {2.0, 3.0, 5.0, 4.0, 11.0},{40.0/6},{6}}
        };
    }

    @Test
    @Parameters(method = "getAddList")
    public void testAdd(Object[] mAdded, Object[] mNumber, Object[] mExpectedAverage, Object[] mExpectedPopulation) throws Exception {
        List<Object> population = Arrays.asList(mAdded);
        BonusRunningAverage add = new BonusRunningAverage((List<Double>)(Object) population);
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
            assertEquals("Average is not true", Double.valueOf(newFormat.format(mExpectedAverage[0])), (Object)add.getCurrentAverage());
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
                new Object[][] {{2.0, 6.0, 4.0, 1.0, 2.0}, {2.0, 1.0}, {4.0}, {3}},
                new Object[][] {{4.0, 3.0, 8.0}, {2.0, 1.0 , 4.0}, {5.5}, {2}},
                new Object[][] {{15.0}, {1.0, 5.0, 2.0, 3.0, 1.0}, {15.0}, {1}},
                new Object[][] {{1.0, 5.0, 2.0, 3.0, 1.0}, {1.0, 5.0, 2.0, 3.0, 1.0}, {0.0}, {0}}
        };
    }

    @Test
    @Parameters(method = "getRemoveList")
    public void testRemove(Object[] mRemoved, Object[] mNumber, Object[] mExpectedAverage, Object[] mExpectedPopulation) throws Exception {
        List<Object> population = Arrays.asList(mRemoved);
        BonusRunningAverage remove = new BonusRunningAverage((List<Double>)(Object) population);
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
            assertEquals("Average is not true", Double.valueOf(newFormat.format(mExpectedAverage[0])), (Object)remove.getCurrentAverage());
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
        return new Object[][] {
            new Object[][] {{2.0, 6.0, 4.0, 1.0, 2.0}},
            new Object[][] {{4.0, 3.0, 8.0}},
            new Object[][] {{15.0}},
            new Object[][] {{1.0, 5.0, 2.0, 3.0, 1.0}}
        };
    }

    @Test()
    @Parameters(method = "getInitialPopulationNegativeClass")
    public void testInitialPopulationNegativeConstructor(Object[] constructor)
    {
        List<Object> population = Arrays.asList(constructor);
        BonusRunningAverage negative = new BonusRunningAverage((List<Double>)(Object) population);
        try{
            assertFalse("Initial population size can be negative", negative.getPopulationSize() < 0);
        } catch (Throwable t) {					
            collector.addError(t);					
        }
    }

    private static final Object[] getPopulationNegativeList() {
        return new Object[][] {
            new Object[][] {{2.0, 6.0, 4.0, 1.0, 2.0}, {2.0, 1.0}},
            new Object[][] {{4.0, 3.0, 8.0}, {2.0, 1.0 , 4.0}},
            new Object[][] {{15.0}, {1.0, 5.0, 2.0, 3.0, 1.0}},
            new Object[][] {{1.0, 5.0, 2.0, 3.0, 1.0}, {1.0, 5.0, 2.0, 3.0, 1.0, 4.0}}
        };
    }

    @Test
    @Parameters(method = "getPopulationNegativeList")
    public void testPopulationNegative(Object[] mAdded, Object[] mRemoved){
        List<Object> population = Arrays.asList(mAdded);
        BonusRunningAverage remove = new BonusRunningAverage((List<Double>)(Object) population);
        List<Object> removedPopulation = Arrays.asList(mRemoved);
        double newAverage;

        try{
            newAverage = remove.removeElements((List<Double>)(Object) removedPopulation);
            assertFalse("Population size can be negative", remove.getPopulationSize() < 0);
        } catch (Throwable t) {					
            collector.addError(t);					
        }

    }

    private static final Object[] getCombineClass() throws Exception {
        return new Object[][] {
            new Object[][] {{2.0, 6.0, 4.0, 1.0, 2.0}, {2.0, 1.0}, {18.0/7}, {7}},
            new Object[][] {{4.0, 3.0, 8.0}, {2.0, 1.0 , 4.0}, {22.0/6}, {6}},
            new Object[][] {{15.0}, {1.0, 5.0, 2.0, 3.0, 1.0}, {27.0/6}, {6}},
            new Object[][] {{1.0, 5.0, 2.0, 3.0, 1.0}, {1.0, 5.0, 2.0, 3.0, 1.0, 4.0}, {28.0/11}, {11}}
        };
    }

    @Test
    @Parameters(method = "getCombineClass")
    public void testCombine(Object[] combin1, Object[] combin2, Object[] mExpectedAverage, Object[] mNumber){
        List<Object> population1 = Arrays.asList(combin1);
        List<Object> population2 = Arrays.asList(combin2);
        BonusRunningAverage rn1 = new BonusRunningAverage((List<Double>)(Object) population1);
        BonusRunningAverage rn2 = new BonusRunningAverage((List<Double>)(Object) population2);
        Object returnObject = new Object();
        try{
            returnObject = BonusRunningAverage.combine(rn1, rn2);
            assertFalse("BonusRunningAverage object is not created", !(returnObject instanceof BonusRunningAverage));
        } catch (Throwable t) {					
            collector.addError(t);					
        }

        BonusRunningAverage temp = (BonusRunningAverage) returnObject;
        
        try{
            assertEquals("Average is not true", Double.valueOf(newFormat.format(mExpectedAverage[0])), temp.getCurrentAverage());
        } catch (Throwable t) {					
            collector.addError(t);					
        }

        try{
            assertEquals("Population is not true", mNumber[0], temp.getPopulationSize());
        } catch (Throwable t) {					
            collector.addError(t);					
        }
    }
}