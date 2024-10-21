from pulp import LpProblem, LpMinimize, LpVariable, PULP_CBC_CMD, LpStatus

tasks = {
    'A': 4.5, 
    'B': 18.5, 
    'C': 12, 
    'D1': 7.5, 
    'D2': 36, 
    'D3': 36, 
    'D4': 108,
    'D5': 18, 
    'D6': 36, 
    'D7': 36, 
    'D8': 36, 
    'E': 36, 
    'F': 18, 
    'G': 18, 
    'H': 18
}

# 25% increase in time for worst case
# 25% decrease in time for best case

worst_case_tasks = {k: v * 1.25 for k, v in tasks.items()}
best_case_tasks = {k: v * .75 for k, v in tasks.items()}


roles = ['Project Manager', 'Frontend Dev', 'Backend Dev', 'Data Scientist', 'Data Engineer']
roles_tasks = {
    'A': {'Project Manager': 4, 'Data Scientist': 1.5},
    'B': {'Project Manager': 18, 'Data Scientist': 6},
    'C': {'Frontend Dev': 12},
    'D1': {'Project Manager': 3, 'Frontend Dev': 7.5, 'Backend Dev': 7.5, 'Data Scientist': 3},
    'D2': {'Frontend Dev': 20, 'Backend Dev': 20},
    'D3': {'Backend Dev': 36},
    'D4': {'Frontend Dev': 90, 'Backend Dev': 108, 'Data Scientist': 70, 'Data Engineer': 85},
    'D5': {'Frontend Dev': 10, 'Backend Dev': 10, 'Data Scientist': 10, 'Data Engineer': 10},
    'D6': {'Frontend Dev': 15, 'Backend Dev': 15, 'Data Scientist': 15, 'Data Engineer': 15},
    'D7': {'Frontend Dev': 15, 'Backend Dev': 15, 'Data Scientist': 15, 'Data Engineer': 15},
    'D8': {'Backend Dev': 12, 'Frontend Dev': 10},
    'E': {'Project Manager': 30, 'Data Scientist': 6},
    'F': {'Project Manager': 15, 'Data Scientist': 5},
    'G': {'Project Manager': 15, 'Frontend Dev': 6, 'Backend Dev': 6},
    'H': {'Project Manager': 18}
}

worst_case_roles_tasks = {
    task: {role: hours * 1.25 for role, hours in roles.items()}
    for task, roles in roles_tasks.items()
}

best_case_roles_tasks = {
    task: {role: hours * .75 for role, hours in roles.items()}
    for task, roles in roles_tasks.items()
}


max_hours = int(sum(tasks.values()))

def solver(scenario, tasks, roles_tasks):
    model = LpProblem("Software_Plan", LpMinimize)

    start_times = {}
    for task in tasks:
        start_times[task] = LpVariable(f"Start_{task}", lowBound=0, cat='Integer')

    completion_time = LpVariable("Completion_Time", lowBound=0, cat='Continuous')

    model += completion_time
    # Define dependencies in the project plan
    model += start_times['C'] >= start_times['A'] + tasks['A']
    model += start_times['D1'] >= start_times['A'] + tasks['A']
    model += start_times['E'] >= start_times['B'] + tasks['B']
    model += start_times['E'] >= start_times['C'] + tasks['C']
    model += start_times['D2'] >= start_times['D1'] + tasks['D1']
    model += start_times['D3'] >= start_times['D1'] + tasks['D1']
    model += start_times['D4'] >= start_times['D2'] + tasks['D2']
    model += start_times['D4'] >= start_times['D3'] + tasks['D3']
    model += start_times['D5'] >= start_times['D4'] + tasks['D4']
    model += start_times['D6'] >= start_times['D4'] + tasks['D4']
    model += start_times['D7'] >= start_times['D6'] + tasks['D6']
    model += start_times['D8'] >= start_times['D5'] + tasks['D5']
    model += start_times['D8'] >= start_times['D7'] + tasks['D7']
    model += start_times['F'] >= start_times['E'] + tasks['E']
    model += start_times['F'] >= start_times['D8'] + tasks['D8']
    model += start_times['G'] >= start_times['A'] + tasks['A']
    model += start_times['H'] >= start_times['F'] + tasks['F']
    model += start_times['H'] >= start_times['G'] + tasks['G']

    for task in tasks:
        model += completion_time >= start_times[task] + tasks[task]
    solver = PULP_CBC_CMD(msg=False)
    status = model.solve(solver)
    LpStatus[status]

    hours_per_day = 8 
    print(f"\n{scenario} Scenario:")
    print(f"Project completion time: {completion_time.varValue / hours_per_day} days")
    print("\nTask start times (in days):")
    for task in tasks:
        start_day = start_times[task].varValue / hours_per_day
        end_day = (start_times[task].varValue + tasks[task]) / hours_per_day
        print(f"{task}: Start: {start_day}, End: {end_day}, Duration: {tasks[task] / hours_per_day}")

    total_hours = sum(sum(hours for hours in task_roles.values()) for task_roles in roles_tasks.values())
    
    # Assume each position = $50 / hour
    total_cost = total_hours * 50
    print(f"\nTotal project cost: ${total_cost}")
    print(f"Total project hours: {total_hours}")


def main():
    solver("Expected", tasks, roles_tasks)
    print('\n')
    solver("Best case", best_case_tasks, best_case_roles_tasks)
    print('\n')
    solver("Worst case", worst_case_tasks, worst_case_roles_tasks)

if __name__ == '__main__':
    main()
