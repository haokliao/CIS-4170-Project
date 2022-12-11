import pandas as pd

def clean(csv):
  housing_violations = pd.read_csv(csv)
  # Dataset has a couple approved/inspection dates that are incorrectly formatted. 
  violation_errors = housing_violations[housing_violations.ViolationID.isin([11936862,13410649,7107587,3984316])].index
  housing_violations.drop(violation_errors,inplace=True)
  # We drop those, and a couple columns (BBL,BIN) we don't need
  housing_violations = housing_violations.drop(columns=['BBL','BIN'])
  #Transform Zipcode to correct data type

  #We need to remove all trailing zeroes first
  housing_violations['Postcode'] = housing_violations['Postcode'].astype(str).str.rstrip("0")
  housing_violations['Postcode'] = housing_violations['Postcode'].astype(str).str.rstrip(".")

  #We create the dataframe, **closed_violations** to represent all the past violations that have been closed/fixed
  closed_violations = housing_violations[housing_violations['ViolationStatus']=='Close']
  # We want to drop any violations that were dismissed, as they will muddle our data (0 days) to fix violations
  closed_violations = closed_violations[closed_violations['CurrentStatus'] != 'VIOLATION DISMISSED']
  #converting these columns to datetime columns
  closed_violations['InspectionDate']= pd.to_datetime(closed_violations['InspectionDate'])
  closed_violations['OriginalCorrectByDate']= pd.to_datetime(closed_violations['OriginalCorrectByDate'])

  #creating ViolationLength, ViolationYear, filtering for violations past the year 2000.
  closed_violations['ViolationLength'] = (closed_violations['OriginalCorrectByDate'] - closed_violations['InspectionDate']).dt.days
  closed_violations['ViolationYear'] = closed_violations['InspectionDate'].dt.year
  closed_violations = closed_violations[closed_violations['ViolationYear']>= 2000]
  closed_violations = closed_violations[closed_violations['Class'] != 'I']

  return closed_violations