from __future__ import print_function
from csv import reader
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark.sql.functions import *

import sys

MUNI = 10
TYPE = 2
ORIGIN = 5
DEST = 6
IDENT = 1 #ident
CITY_INDEX = 0

sc = SparkContext()
spark = SparkSession.builder.getOrCreate()
sqlContext = SQLContext(spark)

def processString(input_string):
	if input_string == None:
		return input_string
	return input_string.lstrip().rstrip().upper()

def getSqlList(lst):
	return "(\""+'\",\"'.join(lst)+"\")"

def getAirportTypeListFor(temp_list):
	return [processString(x) for x in temp_list]

def getCityMapper(filename):
	city_map = {}
	mapper_rdd = sc.textFile(filename)
	mapper_list = mapper_rdd \
					.map(lambda line: (processString(line.split(',')[0]),processString(line.split(',')[1]))) \
					.collect()
	for key, val in mapper_list:
		city_map[key] = val
	return city_map

def findMapping(city_string):
	city_string = processString(city_string)
	if city_string in city_mapper:
		return city_mapper[city_string]
	return city_string

def getCityList(filename):
	city_rdd = sc.textFile(filename)
	city_list = city_rdd\
		.map(lambda line: (findMapping(processString(line.split(',')[0])), 1)) \
		.reduceByKey(lambda x,y: x + y) \
		.map(lambda x: x[0]) \
		.collect()
	return city_list

def getAirportDataDFrame(filename):
	airport = sc.textFile(filename)
	schema = ['ident','type','municipality']
	valid_data = airport \
		.mapPartitions(lambda line: reader(line)) \
		.map(lambda arr: [processString(x) if i != MUNI else findMapping(processString(x)) for i,x in enumerate(arr)]) \
		.filter(lambda arr: arr[TYPE] in airport_type_list and arr[IDENT] != '' and arr[MUNI] != '' ) \
		.map(lambda arr: [arr[IDENT], arr[TYPE], arr[MUNI]]) \
		.collect()
	return spark.createDataFrame(valid_data, schema)

def getAllAirportCodes():
	airport_dataframe.registerTempTable('airport_df')
	df1 = sqlContext.sql ( 
			"""
				SELECT DISTINCT ident
				FROM airport_df
			"""
	)
	res = df1.collect()
	return [x['ident'] for x in res]

def getOnlyCityListAirportCodes():
	airport_dataframe.registerTempTable('airport_df')
	df1 = sqlContext.sql ("""
		SELECT DISTINCT ident 
		FROM airport_df 
		WHERE municipality in """ + getSqlList(city_list))
	res = df1.collect()
	return [x['ident'] for x in res]

def getCovidDataFrame(filename):
	covid = sc.textFile(filename)
	valid_data = covid \
		.mapPartitions(lambda line: reader(line)) \
		.map(lambda arr: [processString(x) if i != CITY_INDEX else findMapping(processString(x)) for i,x in enumerate(arr)]) \
		.filter(lambda arr: arr[CITY_INDEX] in city_list) \
		.collect()
	schema = ['city', 'date', 'cases', 'deaths']
	return spark.createDataFrame(valid_data, schema)

def getFlightDataFrame(filename):
	df1 = spark.read.csv(filename, header='true')
	df1.registerTempTable('df1')
	df1 = sqlContext.sql(
			"""
			SELECT * 
			FROM
			(
				SELECT 
				UPPER(TRIM(origin)) as origin,
				UPPER(TRIM(destination)) as destination,
				UPPER(TRIM(SUBSTRING(day,1,10))) as day
				FROM df1
			) as res
			WHERE 
			(
				res.origin != '' and 
				res.destination != '' and
				res.origin != res.destination and
				(res.origin in {only_selectected_city_air_codes:} 
					or res.destination in {only_selectected_city_air_codes:}) and
				res.origin in {all_city_air_codes:} and
				res.destination in {all_city_air_codes:}
			)
			""".format(
				only_selectected_city_air_codes = getSqlList(only_city_list_airport_codes),
				all_city_air_codes = getSqlList(all_airport_codes)
				)
		)
	return df1

def getInterCityFlightDataFrame():
	flight_dataframe.registerTempTable('flight_df')
	airport_dataframe.registerTempTable('airport_df')
	return sqlContext.sql(
	"""
		SELECT a1.municipality as from_city,
		d.from_airport as from_airport,
		d.to_city as to_city,
		d.to_airport as to_airport,
		d.day as day
		FROM airport_df as a1
		INNER JOIN (
			SELECT 
				f.origin as from_airport,
				a2.municipality as to_city,
				f.destination as to_airport,
				f.day as day
			FROM airport_df as a2
			INNER JOIN flight_df as f
			ON a2.ident = f.destination
		) as d
		ON a1.ident = d.from_airport
	"""
	)

def getCityFromAndToFlightCountsDataFrame():
	inter_city_flight_dataframe.registerTempTable('inter_city_flight_df')
	df1 = sqlContext.sql(
			"""
			SELECT 
				from_city as city,
				day as day,
				COUNT(*) as outgoing_flight_count
			FROM inter_city_flight_df
			GROUP BY from_city, day
			"""
		)
	df2 = sqlContext.sql(
			"""
			SELECT 
				to_city as city,
				day as day,
				COUNT(*) as incoming_flight_count
			FROM inter_city_flight_df
			GROUP BY to_city, day
			"""
		)
	df1.registerTempTable('df1')
	df2.registerTempTable('df2')
	df3 = sqlContext.sql(
		"""
		SELECT 
			df1.city as city,
			df1.day as day,
			df2.incoming_flight_count as incoming_flight_count,
			df1.outgoing_flight_count as outgoing_flight_count
		FROM df1
		INNER JOIN df2
		ON df1.city = df2.city and df1.day = df2.day
		WHERE df1.city IN """ +getSqlList(city_list) + """ ORDER BY df1.day"""
	)
	return df3

def getCovidFlightCountDataFrame():
	covid_dataframe.registerTempTable('covid_count_df')
	city_from_and_to_flight_counts_dataframe.registerTempTable('flight_count_df')
	df1 = sqlContext.sql(
		"""
		SELECT 
			cc.city as city,
			cc.date as day,
			cc.cases as cases,
			cc.deaths as deaths,
			fc.incoming_flight_count as incoming_flight_count,
			fc.outgoing_flight_count as outgoing_flight_count
		FROM covid_count_df as cc
		INNER JOIN flight_count_df as fc
		ON cc.city = fc.city and cc.date = fc.day
		ORDER BY cc.city, cc.date
		"""
		)
	return df1

def saveData(df, filename):
	df.write.option("header","true").csv(filename)


if __name__ == "__main__":

	if len(sys.argv) != 6:
		print("Wrong usage, all arguments not provided.")
		exit(-1)

	map_list_path = sys.argv[1]
	city_list_path = sys.argv[2]
	airport_dataset_path = sys.argv[3]
	merged_flight_dataset_path = sys.argv[4]
	covid_disease_dataset_path = sys.argv[5]

	print('map_list_path: ' + map_list_path)
	print('city_list_path: ' + city_list_path)
	print('airport_dataset_path: ' + airport_dataset_path)
	print('merged_flight_dataset_path: ' + merged_flight_dataset_path)
	print('covid_disease_dataset_path: ' + covid_disease_dataset_path)

	print('Processing has started. It will take 5 to 10 minutes from the start time ......')
	city_mapper = getCityMapper(map_list_path)
	city_list = getCityList(city_list_path)
	airport_type_list = getAirportTypeListFor(['medium_airport','large_airport'])
	airport_dataframe = getAirportDataDFrame(airport_dataset_path)
	all_airport_codes = getAllAirportCodes() ##Uses airport_dataframe
	only_city_list_airport_codes = getOnlyCityListAirportCodes() ##Uses airport_dataframe
	flight_dataframe = getFlightDataFrame(merged_flight_dataset_path)
	covid_dataframe = getCovidDataFrame(covid_disease_dataset_path)
	inter_city_flight_dataframe = getInterCityFlightDataFrame() ##Uses flight_dataframe and airport_dataframe
	city_from_and_to_flight_counts_dataframe = getCityFromAndToFlightCountsDataFrame()  ##Uses inter_city_flight_dataframe
	covid_flight_count_dataframe = getCovidFlightCountDataFrame() ##Uses inter_city_flight_dataframe and covid_dataframe

	saveData(inter_city_flight_dataframe, 'inter_city_flight_data.out')
	saveData(covid_flight_count_dataframe, 'covid_flight_count_data.out')
	
