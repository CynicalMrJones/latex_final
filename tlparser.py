

import sys

totalCount = 0
currentLine = ""

if len(sys.argv) < 2:
    print("Usage: parse input_file")
    exit()
try:
    file = open(sys.argv[1], 'r')
except FileNotFoundError:
    print('Could not open file')


def main():
    global totalCount
    global file
    global currentLine

    getLine(file)
    # Find time log
    while currentLine.lower() != 'time log:\n':
        getLine(file)
    # Now we are after time log
    while currentLine != "":
        getLine(file)
        value = GetTimePeriod()
        truevalue = float(value)
        truevalue = truncate(truevalue)
        totalCount += truevalue
        hours = int(totalCount)
        minutes = int((totalCount - hours) * 60)
    print(f'{hours} hours and {minutes} minutes')


def getLine(file):
    global currentLine
    currentLine = ""
    currentLine = file.readline()


def truncate(value):
    value = int(value * 10**2) / 10**2
    return value


def GetTimeValue(time):
    # parse a value like 9:30pm
    if time[-2:] in ("am", "pm"):
        ap = time[-2:]
        time_part = time[:-2]
    else:
        ap = time[-1] + 'm'
        time_part = time[:-1]
    hours, mins = time_part.split(':')

    hours = float(hours)
    mins = float(mins)

    if ap == 'pm':
        if hours == 12:
            return truncate(hours), truncate(mins)
        hours = float(hours)
        mins = float(mins)
        hours += 12.00
        return truncate(hours), truncate(mins)
    if ap == 'am':
        if hours == 12:
            hours = hours - 12.00
            return truncate(hours), truncate(mins)
        return truncate(hours), truncate(mins)


def GetTimePeriod():
    # to parse 9:30pm - 11:45pm
    # it will call GetTimeValue() in order to
    # return 9:30pm and 11:30pm seperatly
    global currentLine
    preprocess = ''
    part1 = ''
    part2 = ''
    for c in currentLine:
        if c != ' ':
            preprocess += c
        else:
            break
    if preprocess == "":
        currentLine = currentLine.strip(' ')
    else:
        currentLine = currentLine.replace(preprocess + ' ', "")
        currentLine = currentLine.strip()
    for c in currentLine:
        if c == '-':
            part1 = '0'
            part2 = '0'
            break
        if c != ' ':
            part1 += c
        else:
            break
    if currentLine == '' or not currentLine[0].isdigit():
        return 0
    currentLine = currentLine.replace(part1 + ' ', "")
    for c in currentLine:
        if c != 'm':
            part2 += c
        else:
            break
    part2 = part2.replace("- ", "")
    if not part1[0].isdigit():
        return 0
    valuea, valueb = GetTimeValue(part1)
    valuec, valued = GetTimeValue(part2)
    start = (float(valuea) * 60) + float(valueb)
    end = (float(valuec) * 60) + float(valued)
    if end < start:
        end = end + (24 * 60)
    return (truncate(end) - truncate(start)) / 60


if __name__ == '__main__':
    main()
