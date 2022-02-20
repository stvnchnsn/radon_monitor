See Project Overview.ipynb for full overview of project.

Abstract:
A machine learning model is developed to read a radon monitor display.  This data is combined with environmental data to determine the extent of correlation with environmental variables.  It is determined that the correlation coefficents for temperature and pressure are 0.202 and 0.262 respectfully.  This information and data will be used to determine the effectivness of potential mitigation efforts.

Background:
[Radon](https://www.cdc.gov/nceh/features/protect-home-radon/index.html) is a radioactive gas that forms naturally when uranium, thorium, or radium, which are radioactive metals break down in rocks, soil and groundwater.  It is the second leading cause of lung cancer.  The CDC recommends mitigation if radon levels exceed 4 picocuries per liter (pCi/L).  

Personal Motivation:
My basement was professionally tested in the winter of 2016 and was measured at around 3.5 pCi/L.  At the time we considered this acceptable because the basement would mainly be used for storage.  However, during the initial months of the pandemic and the normalization of work from home I started to spend more time in the basement working as it was the quietest place in the house.  This lead me to purchase an [AirThings](https://www.amazon.com/Corentium-Detector-Airthings-223-Lightweight/dp/B00H2VOSP8/ref=asc_df_B00H2VOSP8/?tag=hyprod-20&linkCode=df0&hvadid=312148082093&hvpos=&hvnetw=g&hvrand=3126199023951679431&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9021463&hvtargid=pla-568997698229&psc=1) radon detector.  After installing the detector it became apparent from ancedotal observations over several months that the levels could vary wildly. This observation motivated more research and after reading about potential correlation between weather conditions and radon level fluctuations as well as the varying levels a radon mitigation I decided to build a system to track radon measurements over time to compare the radon measurements to weather conditions so that the effectiveness of any radon mitigation efforts could be evaluated accuratly. 

