# CmpE 436 ASSIGNMENT 2

## UNIT TESTING AT RunnningAverage

### Usage

`$ java -jar normal-test.jar`
`$ java -jar true-test.jar`
`$ java -jar bonus-test.jar`

### Unit Test

- I used `Junit4.12` while creating the tests and I used ErrorCollector to collect all the asserts. In Junit4, I put the `JUnitParams` library in `pom.xml` to be able to parameterize test functions. Thus, I was able to give multiple objects that I created statically as parameters to functions.

- I wrote one test function for each specification:

1. testConstructor
2. testAdd
3. testRemove
4. testInitialPopulationNegativeConstructor
5. testPopulationNegative
6. testCombine

#### testConstructor 

- I checks that `Unless explicitly stated otherwise, a new RunningAverage must start with a population size of zero (0) and thereby the current average must also be zero.`

#### testAdd 

- I checks that `addElements(List<Double>) functions satisfy all requirements.`

#### testRemove 

- I checks that `removeElements(List<Double>) functions satisfy all requirements.`

#### testInitialPopulationNegativeConstructor 

- I checks that `Initial population size is NOT negative.`

#### testPopulationNegative 

- I checks that `The population size can never be negative.`

#### testCombine 

- I checks that `The combine(final RunningAverage, final RunningAverage) function satisfy all requirements.`

### Corrections

- Since I got an error from the `testConstructor` function, I set `populationSize = 0` in the RunningAverage empty constructor.

- Since I got an error from the `testRemove` function, I returned the current `currentAverage` when the length of the removedPopulation list or itself is a null object in the `removeElements` function.

- Since I got an error from the `testInitialPopulationNegativeConstructor` function, I returned an `IllegalArgumentException ()` error in the RunningAverage constructor if the `populationSize` given as a parameter is negative.

- Since I get an error from the `testPopulationNegative` function, if the `populationSize` takes 0 in the `removeElements` function, I break the function and thus the populationSize does not get a value less than 0.

- Since I got an error from the `testCombine` function, I corrected the parentheses error I noticed while creating the RunningAverage object in the `combine` function.






