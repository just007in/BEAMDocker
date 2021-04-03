#!/usr/bin/env python3
import time

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

class Person:
    maxId = 1;
    def __init__(self, plan):
        self.id = Person.maxId
        self.plan = plan
        Person.maxId += 1
    def printXML(self):
        personString = f"<person id=\"{self.id}\">\n"
        plan = self.plan.printXML().split("\n")
        for i in plan:
            if i:
                personString += "\t"
                personString += i
                personString += "\n"
        personString += "</person>\n"
        return personString

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

def print_header(file):
    file.write(r"""<?xml version="1.0" encoding="UTF-8"?>""")
    file.write("\n")

def print_population(file, population):
    try:
        file.write(population.printXML())
    except Exception:
        file.write("<population>\n</population>\n")
        print("Invalid Population")
    finally:
        print("Population file created")

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

#https://stackoverflow.com/questions/6402812/how-to-convert-an-hmmss-time-string-to-seconds-in-python/6402934
def get_sec(time_str):
    """Get Seconds from time."""
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

def main():
    print("Generating Population File")
    file = open("population.xml", "w")
    print_header(file)
    #Population 1
    interval = 20
    number = 50
    potentialStart = [(30,60), (80, 1200)]
    initialTime = ["08:00:00", ""]
    population = generate_generic_population(number, potentialStart, initialTime, interval)
    #Population 2
    interval = 20
    number = 50
    potentialStart = [(40,80), (50, 240)]
    initialTime = ["08:00:00", ""]
    population.mergePopulation(generate_generic_population(number, potentialStart, initialTime, interval))
    #Write Populations to file
    print_population(file, population)

    file.close()

if __name__ == '__main__':
    print("Going to generate a generic population based on preset defaults")
    main()
