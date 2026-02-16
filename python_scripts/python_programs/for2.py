weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
            'Saturday', 'Sunday']
attending_days = ['Monday', 'Wednesday', 'Friday']
# TODO: The loop should skip these days instead of stopping
for day in weekdays:
    if day not in attending_days:
        continue
    print(f"Attending {day}")