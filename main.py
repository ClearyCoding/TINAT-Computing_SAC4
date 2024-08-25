import sqlite3
database = "tinat_planner.db"

# Format [Query Name, Query (without variables to be added by the user), Variable, Result Headings]
commands = [
    ["Query Lines in a Network", "SELECT Line.Name, Line.Gauge, Line.Electrified FROM Line WHERE Line.NetworkID = ",
     "Network", ["Line Name", "Gauge", "Electrified"]],
    ["Query Models produced by a Manufacturer", "SELECT Model.Name FROM Model WHERE Model.ManufacturerID = ",
     "Manufacturer", ["Model Name"]],
    ["Query Train built before a date", "SELECT Train.CarriageID, Train.Built FROM Train WHERE Train.Built < ",
                                        "Cut-Off", ["Carriage ID", "Date Built"]],
    ["Query Accessible Stations on a Line (multi-table)", "SELECT Station.Name, Station.Staffed "
                                                          "FROM Station JOIN StationAllocation ON Station.StationID = "
                                                          "StationAllocation.StationID WHERE Station.accessible = 1 "
                                                          "AND StationAllocation.LineID = ", "Line",
                                                          ["Station Name", "Staffed"]],
    #["Query Lines and Train types through a Station (multi-table)", "SELECT Line.LineID, Model.Name FROM "
    #                                                                "Line JOIN StationAllocation ON Line.LineID = "
    #                                                                "StationAllocation.LineID JOIN TrainAllocation ON "
    #                                                                "Line.LineID = TrainAllocation.LineID JOIN Train "
    #                                                                "ON TrainAllocation.TrainID = Train.TrainID JOIN "
    #                                                                "Model ON Train.ModelID = Model.ModelID WHERE "
    #                                                                "StationAllocation.StationID = ", "Station"],
]


# Sends Query to SQLite
def query(command):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    cursor.execute(command)
    outline = cursor.fetchall()
    connection.close()
    return outline


# Adds user input to queries before export
def configure_query(query_id):
    table = commands[query_id][2]
    amend = ""

    # Date selection
    if table == "Cut-Off":
        while True:
            try:
                year = int(input("Enter Cut-Off Date (YYYY): "))
            except ValueError:
                print("Value must be an integer")
            else:
                break
        amend = year

    # Selection from another table
    else:
        table_options = (query("SELECT Name FROM " + table))
        for i, entry in enumerate(table_options):
            print(f'{i} : {entry[0]}')
        while True:
            try:
                option = int(input(f"Enter {table} Option: "))
            except ValueError:
                print("Value must be an integer")
            else:
                if 0 <= option < len(table_options):
                    break
                else:
                    print("Value is out of range")
        amend = option + 1

    # Returns the full query with the variable amended to the end
    return commands[query_id][1] + str(amend) + ";"


# Query Selection Interface
print("Commands:")
for i, entry in enumerate(commands):
    print(f'{i} : {entry[0]}')
while True:
    selection = 0
    try:
        selection = int(input("Command ID: "))
    except ValueError:
        print("Value must be an integer")
    else:
        if 0 <= selection < len(commands):
            break
        else:
            print("Value is out of range")

# Allows the user to select options for their command
query_filled = configure_query(selection)

# Fetches the results
results = query(query_filled)

# Displays the results
print("\nResults:")
header_bar = "("
for header in commands[selection][3]:
    header_bar += f"{header},    "
header_bar = header_bar[:-5] + ")"
print(header_bar)
if results:
    for i, result in enumerate(results):
        for column in result:
            print(f"{column}    ", end="")
        print("")
else:
    print("No Results Found")
