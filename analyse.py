import json
import csv  

class Animal:
    locationX = None
    locationY = None 
    temperature = None
    oxygen = None
    heart_rate = None
    distance = None
    def __init__(self, deviceId, timestamp):
        self.deviceId = deviceId
        self.timestamp = timestamp
    def __str__(self): 
        attrs = vars(self)
        print(', '.join("%s: %s" % item for item in attrs.items()))

def Ultrasonic(reading):
    return reading['distance']

# def AirQuality(reading):
#     print "n is a perfect square\n"

def Temperature(reading):
    return reading['temperature']

# def Humidity(reading):
#     print "n is a prime number\n"

def GPS(reading):
    return reading['location'][0],reading['location'][1]

def Vitals(reading):
    return reading['pulseOxygen'][0],reading['pulseOxygen'][1]

# map the inputs to the function blocks
options = {3 : Ultrasonic,
        #    9 : AirQuality,
           24 : Temperature,
        #    25 : Humidity,
           27 : GPS,
           31 : Vitals
} 
def main():
    infile = r"./log_220503_195914.txt"

    animalReadings = []
    print("Started Reading JSON file which contains multiple JSON document")
    with open(infile) as f:
        for jsonObj in f:        
            try:
                animalDict = json.loads(jsonObj)
                animalReadings.append(animalDict)
            except ValueError as err:
                continue            

    animal_dict = {}
    for reading in animalReadings:

        if isinstance(reading, list):

            for animal in reading:
                id = animal['deviceId'].split("_")[1]
                timestamp = animal['timestamp']
                key = str(id) + '_'+str(timestamp)

                zebra = None
                if key in animal_dict:
                    zebra = animal_dict[key]
                else:
                    zebra = Animal(id,timestamp)
                    animal_dict[key] = zebra
                sensors = animal['sensors']
                for sensor in sensors:
                    senreading = options[sensor['type']](sensor['input'])
                    # print(senreading)
                    type =sensor['type']
                    if type == 3:
                        zebra.distance =senreading
                    elif type == 27:      
                        zebra.locationX = senreading[0]                      
                        zebra.locationY = senreading[1]                      
                    elif type == 31:      
                        zebra.oxygen = senreading[0]                      
                        zebra.heart_rate = senreading[1]                      
                    elif type == 24:      
                        zebra.temperature = senreading      
    with open('animalSensorReadings.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        header = ['animal', 'timestamp', 'locationX', 'locationY','distance', 'oxygen','heartrate', 'temperature']
        writer.writerow(header)
        for key, value in animal_dict.items():
            # print(key)
            attrs = vars(value)
            # print(', '.join("%s: %s" % item for item in attrs.items()))
            row = []
            row.append(value.deviceId)
            row.append(value.timestamp)
            row.append(value.locationX)
            row.append(value.locationY)
            row.append(value.distance)
            row.append(value.oxygen)
            row.append(value.heart_rate)
            row.append(value.temperature)
            # print(row)
            writer.writerow(row)

if __name__ == "__main__":
    try: 
        main()
    finally: 
        print("Completed reading")


              

