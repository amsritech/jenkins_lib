# Planning a cultural tour with events for each destination.
destination_events = {
    "France": ["Cannes Film Festival", "Bastille Day Fireworks"],
    "Italy": ["Venice Carnival", "Florence Wine Festival"],
    "Spain": ["La Tomatina", "Running of the Bulls"],
    "Japan": ["Sapporo Snow Festival", "Cherry Blossom Viewing"]
}

for destination, events in destination_events.items():
    print(f"Events to attend in {destination}:")
    for event in events:
        print(f"- {event}")