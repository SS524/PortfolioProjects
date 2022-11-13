select * from CovidDeaths order by 3,4 
select * from CovidVaccinations order by 3,4


--Looking at total cases vs total deaths
Select location,date,total_cases,total_deaths,(total_deaths/total_cases)*100 as DeathPercentage from CovidDeaths
where location like '%India%' order by 1,2

--Looking at total cases vs population
--Shows what percentage of population got covid
Select location,date,population,total_cases,(total_cases/population)*100 as PercentageOfPopulationInfected from CovidDeaths order by 1,2


--Looking at countries with highest infection rate compared to population
Select location,population,MAX(total_cases) as TotalInfectionCount,MAX((total_cases/population)*100) as PercentageOfPopulationInfected
from CovidDeaths where continent is not null group by location,population order by PercentageOfPopulationInfected desc

--Showing total death count by country
Select location,MAX(cast(total_deaths as int)) as TotalDeathCount
from CovidDeaths where continent is not null group by location order by TotalDeathCount desc

--Let's break down by continent as per highest death count
Select continent,MAX(cast(total_deaths as int)) as TotalDeathCount
from CovidDeaths where continent is not null 
group by continent order by TotalDeathCount desc

--Global numbers per day
Select date, SUM(new_cases) as TotalCases,SUM(cast(new_deaths as int)) as TotalDeaths,
SUM(cast(new_deaths as int))/SUM(new_cases)*100 as DeathPercentage
from CovidDeaths where continent is not null 
group by date
order by 1,2

--Overall Global numbers
Select SUM(new_cases) as TotalCases,SUM(cast(new_deaths as int)) as TotalDeaths,
SUM(cast(new_deaths as int))/SUM(new_cases)*100 as DeathPercentage
from CovidDeaths where continent is not null 

--Looking at total population vs Vaccinations
Select dea.continent,dea.location,dea.date,dea.population,vac.new_vaccinations, 
SUM(Cast(vac.new_vaccinations as bigint)) OVER(Partition by dea.location order by dea.date) as RollingPeopleVaccinated
from CovidDeaths dea INNER JOIN
CovidVaccinations vac on dea.location=vac.location and
dea.date=vac.date where dea.continent is not null
order by 2,3

--Use CTE
WITH PopVsVac(Continent,Location,Date,Population,New_Vaccinations,RollingPeopleVaccinated)
as
(
Select dea.continent,dea.location,dea.date,dea.population,vac.new_vaccinations, 
SUM(Cast(vac.new_vaccinations as bigint)) OVER(Partition by dea.location order by dea.date) as RollingPeopleVaccinated
from CovidDeaths dea INNER JOIN
CovidVaccinations vac on dea.location=vac.location and
dea.date=vac.date where dea.continent is not null

)
Select *,(RollingPeopleVaccinated/Population)*100 from PopVsVac order by 2,3


--Temp Table
Drop table if exists #PercentPopulationVaccinated
Create table #PercentPopulationVaccinated
(
Continent nvarchar(255),
Location nvarchar(255),
Date datetime,
Population numeric,
New_Vaccinations numeric,
RollingPeopleVaccinated numeric
)
Insert Into #PercentPopulationVaccinated
Select dea.continent,dea.location,dea.date,dea.population,vac.new_vaccinations, 
SUM(Cast(vac.new_vaccinations as bigint)) OVER(Partition by dea.location order by dea.date) as RollingPeopleVaccinated
from CovidDeaths dea INNER JOIN
CovidVaccinations vac on dea.location=vac.location and
dea.date=vac.date where dea.continent is not null

Select *,(RollingPeopleVaccinated/Population)*100 from #PercentPopulationVaccinated order by 2,3

--Create View to store data for later visualization
Create View PercentPopulationVaccinated as
Select dea.continent,dea.location,dea.date,dea.population,vac.new_vaccinations, 
SUM(Cast(vac.new_vaccinations as bigint)) OVER(Partition by dea.location order by dea.date) as RollingPeopleVaccinated
from CovidDeaths dea INNER JOIN
CovidVaccinations vac on dea.location=vac.location and
dea.date=vac.date where dea.continent is not null

Select *,(RollingPeopleVaccinated/Population)*100 from PercentPopulationVaccinated order by 2,3


--Let's create visualization for Power BI
--View 1
Create view GlobalReportView1 as
Select SUM(new_cases) as TotalCases,SUM(cast(new_deaths as int)) as TotalDeaths,
SUM(cast(new_deaths as int))/SUM(new_cases)*100 as DeathPercentage
from CovidDeaths where continent is not null 

select * from GlobalReportView1
--View2
Create view ContinetDeathCountView2 as
Select location, SUM(cast(new_deaths as int)) as TotalDeathCount
From CovidDeaths
Where continent is null 
and location not in ('World', 'European Union', 'International','High income','Upper middle income','Lower middle income','Low income')
Group by location

Select * from ContinetDeathCountView2

--View 3
Create view InfectionCountView3 as 
Select location,population,MAX(total_cases) as TotalInfectionCount,MAX((total_cases/population)*100) as PercentageOfPopulationInfected
from CovidDeaths where continent is not null 
group by location,population 

Select * from InfectionCountView3 where location='jersey'

--View 4
Create View InfectionCountPerDayView4 as
Select location,population,date,MAX(total_cases) as TotalInfectionCount,MAX((total_cases/population)*100) as PercentageOfPopulationInfected
from CovidDeaths where continent is not null 
group by location,population,date 

Select * from InfectionCountPerDayView4










