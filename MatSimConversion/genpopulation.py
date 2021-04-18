#!/usr/bin/env python3
import time

"""
Population class that contains persons defined by the Person class
"""
class Population:
    def __init__(self, person):
        self.people = []
        if isinstance(person, list):
            for i in person:
                self.add(i)
        else:
            self.add(person)
    def add(self, person):
        self.people.append(person)
    def mergePopulation(self, population):
        for i in population.people:
            self.add(i)
    def printXML(self):
        populationString = "<population>\n"
        for i in self.people:
            person = i.printXML().split("\n")
            for j in person:
                if j:
                    populationString += "\t"
                    populationString += j
                    populationString += "\n"
        populationString += "</population>\n"
        return populationString
"""
Person class that contains info about its plans
"""
class Person:
    maxId = 1;
    def __init__(self, plan):
        self.id = Person.maxId
        self.plan = []
        if isinstance(plan, list):
            for i in plan:
                self.add(i)
        else:
            self.add(plan)
        Person.maxId += 1
    def add(self, plan):
        self.plan.append(plan)
    def printXML(self):
        personString = ""
        for p in self.plan:
            personString += f"<person id=\"{self.id}\">\n"
            plan = p.printXML().split("\n")
            for i in plan:
                if i:
                    personString += "\t"
                    personString += i
                    personString += "\n"
            personString += "</person>\n"
        return personString
"""
Plan class that follows MatSim conventions
    Contains a list of activity objects
    Score can be an empty string if no score wants to be provided
    Selected should normally be yes unless multiple plans for each person want to be made
"""
class Plan:
    def __init__(self, score, selected, activity):
        self.listofactivities = []
        self.score = score
        self.selected = selected
        if isinstance(activity, list):
            for i in activity:
                self.add(i)
        else:
            self.add(activity)

    def add(self, activity):
        self.listofactivities.append(activity)
    def printXML(self):
        planString = f"<plan "
        planString += f"selected=\"{self.selected}\""
        if self.score:
            planString += f" score=\"{self.score}\""
        planString += ">\n"
        for i in self.listofactivities:
            activity = i.printXML().split("\n")
            for j in activity:
                if j:
                    planString += "\t"
                    planString += j
                    planString += "\n"
        planString += "</plan>\n"
        return planString
"""
Activity class that follows MatSim conventions for an activity in a Plan
    Contains information about the activity name, starting coordinates, endtime, and mode of transportation
"""
class Activity:
    usedNames = []
    def __init__(self, name, startx, starty, endtime, mode):
        self.name = name
        self.startx = startx
        self.starty = starty
        self.endtime = endtime
        self.mode = mode
        if name not in Activity.usedNames:
            Activity.usedNames.append(name)
    def printXML(self):
        activityString = f"<activity "
        activityString += f"type=\"{self.name}\" "
        activityString += f"x=\"{self.startx}\" "
        activityString += f"y=\"{self.starty}\" "
        if self.endtime:
            activityString += f"end_time=\"{self.endtime}\" "

        activityString += f"/>\n"
        activityString += f"<leg "
        activityString += f"mode=\"{self.mode}\""
        activityString += f"/>\n"
        return activityString
"""
Prints a header for an xml file
"""
def print_header(file):
    file.write(r"""<?xml version="1.0" encoding="UTF-8"?>""")
    file.write("\n")

"""
Prints a population object to a file in xml format
"""
def print_population(file, population):
    try:
        file.write(population.printXML())
    except Exception:
        file.write("<population>\n</population>\n")
        print("Invalid Population")
    finally:
        print("Population file created")

"""
This function generates a generic population that goes to Point A, then Point B. Every person in this population
has the same activity with an interval between when they start the action of going to Point A.
For example, person i where i is from 0 - 10 go to point A starting at a specified time + i*interval
This function is used to a generate a generic population file for a simple highway model where there is one
2-directional highway.

potentialStart is a list of 2-element tuples containing floats that is the starting location of each activity.

initialTime is the starting time of each activity corresponding to the location specified by potentialStart.
The last activity can have an initial starting time of "" (empty string)

interval is the interval between each person leaving the same potential start location from the starting time
    For example, a potential start location at (0,5) with a starting time of 8:00:00 with an interval of 20 means
    the next person would leave the location at (0,5) with a starting time of 8:00:20
    Interval should be an integer and is in seconds
"""
def generate_generic_population(number, potentialStart, initialTime, interval):
    """
    potentialStart and initialTime must be of the same size!
    final initial time may be an empty string
    """
    if len(potentialStart) != len(initialTime):
        print("Incorrect arguments to generate_generic_population")
        return None
    names = ["Home", "Work"]
    if len(potentialStart) > 2:
        for i,d in enumerate(potentialStart):
            if i >= 2:
                names.append("Add" + f"{i}")

    mode = "car"
    score = ""
    selected = "yes"
    people = []
    for num in range(0, number):
        activities = []
        for i, coord in enumerate(potentialStart):
            activities.append(Activity(names[i], coord[0], coord[1], initialTime[i], mode))
            if initialTime[i]:
                initialTime[i] = time.strftime('%H:%M:%S', time.gmtime(get_sec(initialTime[i]) + interval))
        plan = Plan(score, selected, activities)
        people.append(Person(plan))
    return Population(people)
"""
# https://stackoverflow.com/questions/6402812/how-to-convert-an-hmmss-time-string-to-seconds-in-python/6402934
Returns the number of seconds past 00:00:00 from a string of the format HH:MM:SS
"""
def get_sec(time_str):
    """Get Seconds from time."""
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

"""
This function is used to generate a generic population specifically for the US 52 highway model.
Modify the potentialStart, initialTime, and interval as necessary if you want to generate a generic population.
Please remember the generic population is for a simply highway model.
"""
def main():
    print("Generating Population File")
    file = open("population.xml", "w")
    print_header(file)
    #Population 1
    interval = 20
    number = 50
    potentialStart = [(-9656623.440958649,4909284.069400239), (-9650226.27717708, 4901384.945767977)]
    initialTime = ["08:00:00", ""]
    population = generate_generic_population(number, potentialStart, initialTime, interval)
    #Population 2
    interval = 20
    number = 50
    potentialStart = [(-9650194.751497287,4901381.503978073), (-9656607.678118752,4909298.022744203)]
    initialTime = ["08:00:00", ""]
    population.mergePopulation(generate_generic_population(number, potentialStart, initialTime, interval))
    #Write Populations to file
    print_population(file, population)

    file.close()

if __name__ == '__main__':
    print("Going to generate a generic population based on preset defaults")
    main()
