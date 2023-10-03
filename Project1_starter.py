def merge_intervals(intervals):
    if not intervals:
        return []

    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for i in range(1, len(intervals)):
        current_start, current_end = intervals[i]
        last_end = merged[-1][1]

        if current_start <= last_end:
            merged[-1][1] = max(last_end, current_end)
        else:
            merged.append(intervals[i])

    return merged

def get_available_slots(busy_schedule, working_hours, duration):
    available_slots = []
    for i in range(len(busy_schedule) - 1):
        end_current, start_next = busy_schedule[i][1], busy_schedule[i + 1][0]
        if int(start_next.split(':')[0])*60 + int(start_next.split(':')[1]) - (int(end_current.split(':')[0])*60 + int(end_current.split(':')[1])) >= duration:
            available_slots.append([end_current, start_next])

    if int(working_hours[1].split(':')[0])*60 + int(working_hours[1].split(':')[1]) - (int(busy_schedule[-1][1].split(':')[0])*60 + int(busy_schedule[-1][1].split(':')[1])) >= duration:
        available_slots.append([busy_schedule[-1][1], working_hours[1]])

    return available_slots

def group_schedule_matching(person1_busy, person1_work, person2_busy, person2_work, duration):
    merged_busy = merge_intervals(person1_busy + person2_busy)
    person1_available = get_available_slots(merged_busy, person1_work, duration)
    person2_available = get_available_slots(merged_busy, person2_work, duration)

    common_slots = []
    for slot1 in person1_available:
        for slot2 in person2_available:
            start = max(slot1[0], slot2[0])
            end = min(slot1[1], slot2[1])
            if int(end.split(':')[0])*60 + int(end.split(':')[1]) - (int(start.split(':')[0])*60 + int(start.split(':')[1])) >= duration:
                common_slots.append([start, end])

    return common_slots

def read_input_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    test_cases = []
    data = {}
    key = None
    for line in lines:
        line = line.strip()
        if line.endswith("_Schedule") or line.endswith("_work_hours") or line == "duration_of_meeting":
            key = line
            data[key] = []
        elif line == "END":
            if key == "duration_of_meeting":
                data[key] = int(data[key][0])
            test_cases.append(data)
            data = {}
            key = None
        else:
            if key:  # Ensure key is not None before appending
                data[key].append(line.split())

    return test_cases

def write_output_file(filename, results):
    with open(filename, 'w') as file:
        for result in results:
            for slot in result:
                file.write(f"{slot[0]} {slot[1]}\n")
            file.write("END\n")

test_cases = read_input_file("input.txt")
results = []

for test_case in test_cases:
    result = group_schedule_matching(test_case["person1_busy_Schedule"], test_case["person1_work_hours"], test_case["person2_busy_Schedule"], test_case["person2_work_hours"], test_case["duration_of_meeting"])
    results.append(result)

write_output_file("output.txt", results)