import sqlite3
# import pygame

database = "tinat_planner.db"
commands = {
    "Query Lines in a Network": "SELECT Line.Name, Line.Gauge, Line.Electrified FROM Line WHERE Line.NetworkID = <NetworkID>;",
    "Query Models produced by a Manufacturer": "SELECT Model.Name FROM Model WHERE Model.ManufacturerID = "
                                               "<ManufacturerID>;",
    "Query Train ages": "SELECT Train.TrainID, Train.Built FROM Train WHERE Train.Built < <Cutoff Date>;",
    "Query Accessible Stations on a Line (multi-table)": "SELECT Station.Name, Station.Accessible, Station.Staffed "
                                                         "FROM Station JOIN StationAllocation ON Station.StationID = "
                                                         "StationAllocation.StationID WHERE StationAllocation.LineID "
                                                         "= <LineID>;",
    "Query Lines and Train types through a Station (multi-table)": "SELECT DISTINCT Line.LineID, Model.ModelName FROM "
                                                                   "Line JOIN StationAllocation ON Line.LineID = "
                                                                   "StationAllocation.LineID JOIN TrainAllocation ON "
                                                                   "Line.LineID = TrainAllocation.LineID JOIN Train "
                                                                   "ON TrainAllocation.TrainID = Train.TrainID JOIN "
                                                                   "Model ON Train.ModelID = Model.ModelID WHERE "
                                                                   "StationAllocation.StationID = <StationID>;",
}


def query(command):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    cursor.execute(command)
    outline = cursor.fetchall()
    connection.close()
    return outline


print("Commands:")
for i, entry in enumerate(commands.keys()):
    print(f'{i + 1} : {entry}')

while True:
    try:
        selection = int(input("Command ID: "))
        print(query(commands[selection + 1]))
    except ValueError:
        print("Value must be an integer")
