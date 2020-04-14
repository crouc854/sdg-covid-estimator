def estimator(data):
  output = {}
  output['data'] = data
  output['impact'] = calculateImpact(data)
  output['severeImpact'] = calculateImpact(data, "severe")

  return output

def calculateImpact(data, condition="normal"):

  if condition == "severe":
    currentlyInfected = data['reportedCases']*50
  else:
    currentlyInfected = data['reportedCases']*10

  days = convertToDays(data['periodType'], data['timeToElapse'])
  durationFactor = 2**(days//3)
  infectionsByRequestedTime = currentlyInfected*durationFactor
  severeCasesByRequestedTime = 0.15*infectionsByRequestedTime
  availableHospitalBeds = 0.35* data['totalHospitalBeds']
  hospitalBedsByRequestedTime = availableHospitalBeds-severeCasesByRequestedTime
  casesForICUByRequestedTime = 0.05*infectionsByRequestedTime
  casesForVentilatorsByRequestedTime = 0.02*infectionsByRequestedTime
  dollarsInFlight = (infectionsByRequestedTime * data['region']['avgDailyIncomePopulation'] * data['region']['avgDailyIncomeInUSD']) // days

  output = {
    'currentlyInfected':int(currentlyInfected),
    'infectionsByRequestedTime':int(infectionsByRequestedTime),
    'severeCasesByRequestedTime':int(severeCasesByRequestedTime),
    'hospitalBedsByRequestedTime':int(hospitalBedsByRequestedTime),
    'casesForICUByRequestedTime':int(casesForICUByRequestedTime),
    'casesForVentilatorsByRequestedTime':int(casesForVentilatorsByRequestedTime),
    'dollarsInFlight':int(dollarsInFlight)
  }
  return output

def convertToDays(periodType, timeToElapse):
  if periodType == "weeks":
    return timeToElapse*7
  if periodType == "months":
    return timeToElapse*30
  return timeToElapse