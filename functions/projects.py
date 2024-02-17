import database


def add_project(name, description, start_date, end_date, client_id, budget, status):
    # Get a reference to the 'projects' branch in the Firebase Realtime Database
    ref = database.get_ref('projects')

    if ref is not None:
        # Generate a new unique key for the project
        new_project_ref = ref.push()

        # Set the project data under the new key
        new_project_ref.set({
            'name': name,
            'description': description,
            'start_date': start_date,
            'end_date': end_date,
            'client_id': client_id,
            'budget': budget,
            'status': status
        })

        print("Project added successfully.")
    else:
        print("Failed to add project: 'projects' reference not found.")


# Test adding a new project record
if __name__ == "__main__":
    add_project(
        name="New Project",
        description="This is a new project",
        start_date="2024-01-01",
        end_date="2024-12-31",
        client_id="client1",
        budget=1000000,
        status="in progress"
    )
