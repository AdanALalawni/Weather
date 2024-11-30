# Weather_ETL
This ETL used to read weather information (city_name, temperature, humidity, weather_condition, and timestamp) each hour from the Openweather API and load it to a CSV file in local storage.
![Alt](https://github.com/AdanALalawni/Weather/blob/main/W-ETL.png)

### Run Airflow on Docker container using `docker-compose.yaml` file 
 and use this command to compose it up:
 
      docker compose -f "docker-compose.yaml" up -d --build 
Go to airflow login using:

       http://localhost:8080

![Alt](https://github.com/AdanALalawni/Weather/blob/main/ETL.png)
This ETL will read weather data for London city(you can chamge city to your city) from openweather and save it in CSV format in local storage.
## Note:
change api_key in`config.json`to your key to use this ETL.

