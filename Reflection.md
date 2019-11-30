Our dashboard is based on average annual hate crime data from 2010-2016 across all US states. 
So with limited data of 50 rows, we created 4 research questions and made plots accordingly. We have tried to make the 
dashboard easy to navigate by adding description for each tab and appropriate headings for all plots which make them 
self-explanatory.

#### Prospects for future improvement

- In the second tab of the dashboard, we have compared rate of change in hate crimes based on low and high baseline with 
bar graphs. Box-plots with jitter points would have been a better choice to answer the corresponding research question. 
But it was difficult to create such a visualization in an appropriate manner for our dataset with altair, even with catplot( ). 
- In the first tab, we can add statistics for p-value and R for the best fit line which would give us more information about 
the relation between hate crime rate and the socio-economic factors. 
- In tab 2, we could add mean or median lines in the lower and higher baseline plots for pre and post election hate crime rates.

#### Limitation of the app

The dashboard only compares hate crime rates before and after 2016 elections and hints that this change may be attributed to 
the voting trend for Donald Trump. In case we had access to hate crime data of previous elections, we would have been able to 
particularly differentiate the significance of 2016 election (with Trump in the running). 

#### Incorporating feedback

- To address the issues raised in Github, we did more conversions using github issues and made sure everyone got chances 
to make pull requests frequently. 
- We included all the variables in the data that are mentioned in our proposal. For those variables with less meaningful names, 
we define them with better meaningful names in the plot in our dashboard. 
- Also we re-worded the research question language and README.md to make it more comprehendable. We have tried to make the 
interpretation of the last research question easy and simplified it by grouping the data into states with low or high 
baseline hate crimes to explore the effect of baseline hate crime rates on the changes of the hate crime rates. 
Further, we have also added a footnote in our app to explain the meaning of "baseline crime rates". 
- To avoid grammatical errors, we tried to re-check the texts written by each group member by others. 
- We have also made the text large enough for axes and legends in our dashboard.
