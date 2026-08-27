# Table of Contents
1. [Project Background](#project-background)
    * [Insights, Reccomendations and focus areas](#insights-reccomendations-and-focus-areas)
2. [Data Structure](#data-structure)
3. [Executive Summary](#executive-summary)
    * [Overview of Discoveries](#overview-of-discoveries)
    * [Discovery Trends](#discovery-trends)
4. [Insights Details](#insight-details)
    * [Concentration: 56.4% of International Visitors](#concentration-564-of-international-visitors)
    * [Immigration Control Among the Top 3 Countries](#immigration-control-among-the-top-3-countries)
    * [The Months with 21.75% of Annual Tourists](#the-months-with-2175-of-annual-tourists)
5. [Models, Predictions, and their Impacts](#models-predictions-and-their-impacts)
    * [Predicting Expected Number of Tourist Visitors](#predicting-expected-number-of-tourist-visitors)
    * [The 6 Types of International Visitors](#the-6-types-of-international-visitors)
6. [Recommendations](#recommendations)
    * [Targeted Marketing Based on Country and Point of Entry](#targeted-marketing-based-on-country-and-point-of-entry)
    * [Managing a Budget That Fluctuates Month to Month](#managing-a-budget-that-fluctuates-month-to-month)
    * [Including Free-Admission Sites in Promotional Packages for Machu Picchu](#including-free-admission-sites-in-promotional-packages-for-machu-picchu)
7. [KPIs](#kpis)
    * [Percent Change of Clients](#1-percent-change-of-clients)
    * [Dynamic Budget](#2-dynamic-budget)
    * [Site Ratios](#3-site-ratios)
8. [Assumptions](#assumptions)

## Project Background
PeruTur is a small company that provides tourism services to international visitors entering Peru. It currently operates in the city of Lima and wants to expand throughout the country, but it is unsure of the best strategy to promote its services nationwide. This project uses Peruvian public data containing information on country-wide tourist sites and international tourists from **2019–2025**.

The analysis and models show that tourists can be grouped based on the **Immigration Control Office (OCM)** through which they entered the country, which can be used to generate targeted marketing to optimize advertisement efforts. Additionally, the analysis reveals that tourist visits follow a monthly trend throughout the year, with the number of tourists peaking in July and August and reaching a low in February. Finally, there are a variety of tourist sites with no admission fee, creating an opportunity to minimize the costs of tourist trips.

The recommendations on targeted marketing, dynamic budgeting, and free sites is highlighted when creating a strategy to help PeruTur expand nationwide.

<br><br>

### Insights, Reccomendations and focus areas
**Visitor Distribution and Countries of Origin**: 95% of international visitors come from **25 countries**, with the top 6 countries accounting for 70.6%. Additionally, 5 of these 6 countries are in South America. This creates an opportunity to narrow down the focus to specific countries and conduct targeted marketing toward each of them.


**Immigration Control Offices (OCMs) and Neighboring Countries**: 4 of the 81 national OCMs account for **94.67%** of all international arrivals in Peru. Furthermore, the majority of arrivals at each of these 4 OCMs come from the nearest neighboring country (with the exception of Lima International Airport). When developing advertisements located on these OCMs, it is recommended to focus on attracting tourists from the closest neighboring countries.


**Availability of Free Tourist Sites**: Machu Picchu, one of the seven wonders of the world, is the most popular tourist site in Peru, meaning that most of PeruTur’s customers will want to travel there. The analysis showed that there are 16 **free-entry** tourist sites within a 25-kilometer radius of Machu Picchu. This presents an opportunity to create advertisements that include these sites without incurring additional costs (other than gasoline).

<br><br>
The web scraping process can be found [HERE](scraper.py)

The data insight development can be found [HERE](./insights.ipynb)

The models' creation and evaluation can be found [HERE](./Models/)

<br><br>

## Data Structure
Three different datasets were used to conduct the necessary analyses, and their components are as follows:
1. International visitors: year, month, country, continent, OCM, and number of visitors
2. Visitors to tourist sites: year, month, department, tourist site, and number of visitors
3. Inventory of tourist resources: region, category, URL, latitude, and longitude

Before beginning the analysis, the integrity and structure of the datasets were verified through organization and cleaning.



<br><br>

## Executive Summary
### Overview of Discoveries
Most international visitors to Peru come from just 25 countries, with Chile, the U.S., and Ecuador accounting for **56.4% of annual visitors**. This presents an opportunity for PeruTur to focus on a small number of countries and develop targeted marketing strategies. Additionally, the entry points for these visitors are split between Lima Airport (55.76%) and Santa Rosa Airport (28.41%). This suggests that marketing efforts should focus on the areas surrounding these entry points, in order to reach the majority of potential customers. Furthermore, **July and August account for 21.75% of annual visitors** and are the months when PeruTur can invest more to meet the demand for tourism services. Finally, Machu Picchu is the most popular tourist site and is surrounded by other sites with free admission. PeruTur can take advantage of this financial opportunity to expand its promotional packages without incurring additional expenses. 


### Discovery Trends

**South America and Peru's Neighbors**: Five of the top six countries in terms of international visitors are Peru's neighbors, and all South American countries are among the top 25 countries by contribution.

**Tourism Seasons**: Every year, July and August see the highest number of international visitors, while **February has the lowest**, accounting for only 4.84* of all annual visitors.

**Free Sites Around Machu Picchu**: Within a 25-kilometer radius of Machu Picchu, there are 16 sites with free admission, most of which are located to the north.


<br><br>
## Insight Details
### Concentration: 56.4% of International Visitors
Given that Peru has an abundance of historical and cultural sites, including one of the seven wonders of the world, it was expected that there would be a balanced percentage of visitors from all countries. The analysis revealed other findings.


* **Chile**: accounts for 32.9% of **all** international visitors
* **Top 3 Countries**: account for 56.4% of international visitors
* **Top 6 Countries**: account for 70.6% of international visitors

Notable Patterns:
* **Monthly Consistency**
    - Within each month, the top 3 countries are generally Chile, the U.S., and Ecuador. This consistency will help enable targeted marketing efforts throughout the year.
* **Border Policy Impacts Number of International Visitors**
    - Five of the top six countries are **direct neighbors** of Peru. A large majority of international visitors are affected by policies at Peru’s borders.
* **High Concentration in 25 of 198 Countries**
    - 95% of all international visitors come from the top 25 out of 198 countries. That is, 177 countries do not contribute significantly to visitor numbers, and there is no need to focus heavily on them.

![Visitors Per Month](./Images/VisitorsPerMonth.png)

<br><br>

### Immigration Control Among the Top 3 Countries
Given that Chile, the U.S., and Ecuador account for more than half of all visitors, it is important to consider the Immigration Control Office (OCM) they use to enter Peru.

* 79.47% of Chileans enter through the **Santa Rosa** OCM in Tacna, southern Peru
* 96.19% of Americans use **Jorge Chávez International Airport**.
* 67.54% of Ecuadorians enter through the **Cebaf-Tumbes** OCM in Tumbes, northern Peru

Notable Patterns:
* 81 OCMs account for only 4.36% of international visitors.
    - There are 86 OCMs in Peru, with 81 of them grouped under the same variable ‘OTRAS_OCM’. Only 4.36% of international visitors enter through these other OCMs, implying that they do not have a significant impact.
    <h4 id="ocm"></h4>
* Border Crossing Points (OCMs) and their **closest** neighboring country
    - Every OCM, except Lima Airport, has the majority of its visitors coming from the closest neighboring country.
* Santa Rosa and Chileans
    - Although **28.41%** of all international visitors enter through the Santa Rosa OCM, most of those visitors come from Chile. This is evident from the fact that one-third of all international visitors are Chilean, and 79.47% of them enter through Santa Rosa.

![OCM by Country](./Images/OCMByCountry.png)

### The Months with 21.75% of Annual Tourists
There are various factors that affect the number of tourists in a given month, such as the weather, historical events, political changes, etc. Some of these factors follow an annual cycle, signaling that the number of tourists also follows annual trends.

* The months of **July and August** account for 21.75% of annual tourists.
* February has the **lowest** number of tourists.
* **Machu Picchu**, including the town, is the most visited site every month.

Notable Patterns:
* Seasonal trends at all tourist sites
    - There is a seasonal trend at all tourist sites. July and August receive the highest number of tourists, while February has the lowest number.
* Prominence of Machu Picchu
    - The top 5 sites are all related to Machu Picchu in some way. Some are services related to Machu Picchu, and others are sites in the surrounding area.

![Monthly Tourists](./Images/MonthlyTourists.png)

<br><br>

### 16 Free Sites Within 25 km of Machu Picchu
As one of the seven wonders of the world, Machu Picchu was expected to be the most popular tourist destination. There are also a variety of nearby tourist sites with no admission fee, providing an opportunity for travel agencies to maximize their profits.

* There are 16 sites with **free admission** within 25 kilometers of Machu Picchu.
* Most of these sites are located to the **north** and are along major routes.

![Map](./Images/MP.png)

<br><br>

## Models, Predictions, and Their Impacts
### Predicting Expected Number of Tourist Visitors
Predicting the number of visitors expected in a given month would help a business optimize its resources. Given the month, department, and name of the tourist site, the regression model predicts the number of visitors expected at that site.

Three candidate models were tested on this data: linear regression, lasso regression, and random forest. When an appropriate metric was applied to all candidates, the random forest model yielded the best results.

When applying the model to the available data, it is estimated that there is a small average difference of 4,915 tourists between the prediction and the actual value. The results demonstrate that the model can be used with confidence to predict the number of tourists within a given month.

![Pred Vs Actual](./Images/PredVSActual.png)

<br><br>

### The 6 Types of International Visitors
K-Means is an algorithm that groups data points into clusters based on their proximity to one another. This process revealed the following clusters:

* Cluster 1: Entrants via the Santa Rosa Border Crossing Point
* Cluster 2: Chilean and U.S. visitors
* Cluster 3: Entrants via the Lima International Airport and Cebaf-Tumbres border crossing points
* Cluster 4: Entrants via other border crossing points not considered
* Cluster 5: Entrants via the Desaguadero border crossing point
* Cluster 6: Arrivals via the Kasani border crossing point

K-Means primarily grouped international visitors by their point of entry. Given that the majority of visitors at a border crossing point are citizens of the <a href="#ocm">nearest country</a>, this grouping is consistent with the data.

The second cluster focuses entirely on the visitors’ country of origin, particularly Chile and the U.S. Given that these two countries account for [48.5% of all international visitors](#concentration-564-of-international-visitors), this cluster is consistent with the data.

In practice, targeted marketing campaigns can be developed for each cluster. When a new visitor arrives, they can be assigned to a cluster based on which OCM they entered from. Once assigned to a cluster, they can be shown the same marketing campaigns as others in that group.

<br><br>

## Recommendations
Based on the findings, insights, and model results, the following recommendations are made to PeruTur’s **Marketing Team**:

### Targeted Marketing Based on Country and Point of Entry
The top 10 countries of origin for international visitors account for 82.5% of **all** international visitors, with Chile accounting for nearly one-third of that total, and 6 of those 10 countries are in South America. Additionally, it was found that the majority of visitors entering through each port of entry come from the **nearest neighboring country**, creating a link between the port of entry and the country of origin. This finding was reinforced by the clusters created by the K-Means algorithm, which grouped all visitors by their entry OCM.

Therefore, it is recommended that the marketing team focus on the following targeted marketing strategies:
* Lima Airport OCM: Focus on an international audience, without placing too much emphasis on South American countries.
* Santa Rosa OCM: Focus on Chile.
* Cebaf-Tumbes OCM: Focus on Ecuador.
* Desaguadero OCM: Focus on Bolivia.
* All other OCMs: minimal and general investment.

<br>

### Managing a Budget That Fluctuates Month to Month
Tourist destinations have peak seasons in July and August, and off-peak seasons in February. To optimize the use of an annual budget, it’s recommended to create a **dynamic budget** that allocates a high budget to July and August, while assigning a low budget to February.

This dynamic would also affect the campaigns being run, but trends from countries of origin remain consistent across all months. Given that the majority of international visitors come from Chile every month, it would be best to focus marketing efforts on Chileans during the off-season. Conversely, during the peak season — when the budget is larger — campaigns can be expanded to target Americans, Ecuadorians, and others, depending on the available budget.

<br>

### Including Free-Admission Sites in Promotional Packages for Machu Picchu
Machu Picchu is the most popular tourist destination in Peru. It has also been discovered that there are a variety of other sites in the surrounding area with no admission fee. Within 25 kilometers of Machu Picchu, there are 16 of these **free-entry** sites. Taking into consideration the cost of gas to transport tourists within a 25-kilometer radius, these sites can be incorporated into promotional packages to attract more visitors.

<br><br>

## KPIs

### 1. Percent Change of Clients
((New Clients - Old Clients)/Old Clients) * 100

Focus: To measure the targeted marketing campaign effectiveness, this metric will be measured in each OCM that gets selected for the marketing campaign. 

### 2. Dynamic Budget
Annual Budget * (Monthly Tourists / Annual Tourists)

Objetive: Assign a budget proportional to the percent of tourists during a given month.

### 3. Site Ratios
Free-entry sites : paid-entry sites

Focus: This ratio will demonstrate the effect of integrating free-entry sites into advertisements, with the objective being to increase the value of this ratio. 

<br><br>

## Assumptions
This analysis made the following assumptions in order to overcome multiple challenges:
* Tourists vs. Day Trippers: Given the limited data, no distinction was made between tourists and day trippers in this analysis. Similarly, it is possible for a day tripper to visit a tourist site or for a tourist not to visit any sites at all. Both categories were grouped under “international visitors.”
* Weather: Although weather is an important factor in tourist movement, this data was omitted due to the significant differences between Peru’s coast, highlands, and jungle regions. This point was communicated to the company, and they decided to begin recording weather conditions at all tourist sites. In a future project, this information could be integrated to improve the regression model’s predictions.