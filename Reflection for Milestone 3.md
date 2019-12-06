## Reflections for Milestone 3

#### Summary of feedback received

The users were able to navigate around the tabs and majorly understood how the app functioned. Specifically for Tab 1, they were able to explore various socio-economic factors on the x-axis through the dropdown and were also able to interpret similar conclusions as done by our team. For Tab 2, as we had suspected, users were not clearly able to understand the interactivity component of clicking on the bar(s) in the heatmap to explore where the state lied in the subsequent bar plots. But upon pointing them to note written at the bottom of the page, they were able to interact with the plots. We have now addressed this issue by explicitly stating how the interactivity component works at the top of the plots on the page. 

Another common point of feedback that all members of the group received was that users found it difficult to comprehend what “low and high baseline” meant. We have also tried to address this by adding an explanation on top of the graphs. There were certain points discussed as part of the feedback process (for example, giving the drop down on Tab 1 at top of the graph or making the chloropleth map smaller than the scatterplot) which the team decided would not impact the overall app functionality much and did not implement in the updated app.
Also, another point discussed in the feedback were adding p-values with the regression line in the scatter plot, which we would implement in the R version of the app, as it is harder to do with Python.

The feedback received has made the app easier to navigate and has made the graphs more understandable for the user.


#### Summary of changes made in the app

Based on the feedback received, we have made the following changes in the latest deployed version of the app:
- Included an explanation as part of description of the app and corrected grammatical errors. 
- Included a description of what low and high baseline states meant before the graphs on Tab 2, rather than as part of a note at the bottom of the page. We have also included the formula for `rate of change of crime rate` to clearly explain what it means.
- Sorted the bar plots on Tab 2 in ascending order of rate of change of hate crime values.
- Changed the y-axis title for the heatmap from `Share of Trump voters` to `People who voted for Trump (%)`.
- Changed the text on top of the dropdown for Tab 1.

#### Prospects for Future Improvement
- In the second tab of the dashboard, we have compared rate of change in hate crimes based on low and high baseline with bar graphs. Box-plots with jitter points would have been a better choice to answer the corresponding research question. But it was difficult to create such a visualization in an appropriate manner for our dataset with altair, even with catplot( ). We will incorporate this change with the app’s version on R. (Screen shots of plots in R include this graph with boxplot and jitter points)
- In the first tab, we can add statistics for p-value and R for the best fit line which would give us more information about the relation between hate crime rate and the socio-economic factors. We will include this with R’s version of the app as well.
