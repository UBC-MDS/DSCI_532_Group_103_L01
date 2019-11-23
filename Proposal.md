## MOTIVATION AND PURPOSE

[Hate crimes](https://en.wikipedia.org/wiki/Hate_crime) in the US has been the talking point in media lately. In a country like the United States with large numbers of immigrant population, this is a major concern for the authorities. We have analysed past hate crime data and tried to delve deeper into the causes of these crimes. Our dashboard app tries to find out the relation between demographics data of income, unemployment, education, etc. with hate crime records. 

Firstly, we tried to identify the distribution of hate crimes across US states and various factors which might affect the crime rate. Secondly, our app will also show the differences caused by the US general elections of 2016 
across the hate crime rates.


## DESCRIPTION OF THE DATA

The dataset we are visualizing has details for 50 states and the District of Columbia (which houses the capital city) of United States of America related to hate crime rates pre and post the 2016 election and factors that may influence these rates across the states. Each state has 11 associated variables that may be used to explore the variables that may have an impact on hate crimes across the states. The column `avg_hatecrimes_per_100k_fbi` describes the average annual hate crimes per 100,000 population from 2010-2015 as collected by FBI and the column `hate_crimes_per_100k_splc` has the hate crimes per 100,000 population for 10 days after the 2016 presidential election which has been collected by the Southern Poverty Law Center. We will explore the spread of average hate crime incidences across the states .Further, in order to explore which factors may contribute to hate crime rates, we will analyze available data on socioeconomic factors for each state which includes the following:

*	`gini_index` - a measure for income disparity, for the year 2015
*	`share_unemployed_seasonal` - seasonally adjusted unemployed population, September 2016
*	`share_white_poverty` for the year 2015
*	`share_non_citizen` - share of citizens for the year 2015
*	`share_population_in_metro_areas` for the year 2015

To help understand the trend of hate crime rates post election and explore any possible relations of this trend with the voting pattern, the column `share_voters_voted_trump`, which details the share of 2016 U.S. voters who voted for Donald Trump, would be used for analysis. Apart from these variables, information for `median_household_income` (2016) and `share_population_with_high_school_degree` (2009) are also available for the states.


## RESEARCH QUESTIONS AND USAGE SCENARIOS

The research questions we wish to explore from the U.S. hate crime dataset are:

1. What is the trend of hate crime rates across the states of U.S.?
2. What are the factors that may influence the rate of hate crimes across the country?
3. Did change in hate crime rates post 2016 presidential elections depend on the proportion of Trump voters in a state?
4. Was the change in hate crime rate post 2016 election higher or lower for states across lower and higher pre-election hate crime rates?

Anyone intersted in exploring the spread of hate crime across the United States, specifically for the purpose of security of citizens and visitors of the nation, or authorities from the law may make use of the dataset to understand potential factors that may influence rate of hate crime across the nation. The user can see the states with hate crime rates on both the, higher and lower end and compare the rate of hate crime in these states by hovering over the states to see more details about the count of these incidents. Moreover, in order to understand which factors may influence the hate crime rates across states, the user can select the factor of interest from a drop down menu and understand if there is a linear relationship with the rate of hate crimes. For instance, upon selecting income disparity, one may notice that it has a positively linear relation with hate crime rates and can also hover over the scatterpoints for more information about the state and variable values.

Users interested in exploring the change of hate crime rates and its plausible relation with the voting pattern of the state can explore this through a heat map on the dashboard, detailing the share of voter supporting one candidate and the extent of change in hate crime rate 10 days after election from the average rate. The user may be able to explore a comparison of a state’s hate crime rate before and after the election to understand if there has been any significant change in this rate on the basis of whether the state had a low or high rate prior to the election. For instance, this may help give insight into whether states that already had a high pre-election rate of hate crime were the ones that did not see much increase in this rate post the elections, which may indicate that voting share may not be a very strong influencing factor on the change in hate crime rate.
