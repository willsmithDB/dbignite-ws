# Databricks notebook source
pip install git+https://github.com/databricks-industry-solutions/dbignite.git@feature-FHIR-schema-dbignite-HLSSA-289


# COMMAND ----------

from dbignite.fhir_mapping_model import *

# COMMAND ----------

fhir_resource_map = fhirSchemaModel()

# COMMAND ----------

fhir_resource_map.resource("Account")

# COMMAND ----------

fhir_resource_map.debug_print_keys()

# COMMAND ----------

import json 

with open("../sampledata/Abe_Bernhard_4a0bf980-a2c9-36d6-da55-14d7aa5a85d9.json") as patient_file:
  patient_data = json.load(patient_file)

patient_data["entry"][0]["resource"]

# COMMAND ----------

## Researching Issue with reading in patient info
data = json.load(open("../sampledata/Abe_Huels_cec871b4-8fe4-03d1-4318-b51bc279f004.json", "r"))
abe = data['entry'][0]['resource']

print(abe)


# COMMAND ----------

#The inferred schema
infer = spark.createDataFrame([abe])

# COMMAND ----------

#The explicit schema
schema =  fhir_resource_map.resource("Patient")
explicit = spark.createDataFrame([abe], schema)

display(explicit)

# COMMAND ----------


#birth dates match
explicit.select("birthdate").show(truncate=False)

#names all match
explicit.select("name").show(truncate=False)

# COMMAND ----------


