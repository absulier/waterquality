#Problem:
-Water quality is a huge factor in public health, but unfortunately not
consistently clean everywhere in the US.

-Identify if particular groups are most at risk for certain contaminations or
violations in their drinking water.

-Try to predict where future drinking water violations will occur

##NOTE:
Full data set is too large to push to github.
To compile full data set:

1) In "EPA" directory, run 'vio_cat.py' to get 'violations.py'  
2) In "census" directory, run 'census_cleaner.py' to get 'census.csv'  
3) In main directory, run 'data_compile.py' to get 'vio_full.csv'  
4) In main directory run 'vio_organizer.py' to get 'vio_org.csv'  
5) In main directory, run 'compile_for_test.py' to get 'fulltest_w_census'

These steps will print 5 CSV files to the local directory housing the git
repository of this project.
