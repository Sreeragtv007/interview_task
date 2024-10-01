import json
from datetime import datetime


class Task:
    def __init__(self, task_id, title, description, due_date, status="Pending"):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.status = status

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date.isoformat(),
            "status": self.status
        }

    @staticmethod
    def from_dict(data):
        return Task(
            task_id=data["task_id"],
            title=data["title"],
            description=data["description"],
            due_date=datetime.fromisoformat(data["due_date"]),
            status=data["status"]
        )


class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def add_task(self, title, description, due_date, status="Pending"):
        task_id = len(self.tasks) + 1
        new_task = Task(task_id, title, description, due_date, status)
        self.tasks.append(new_task)

    def list_tasks(self, status=None):
        for task in self.tasks:
            if status is None or task.status == status:
                print(
                    f"{task.task_id}: {task.title} - {task.description} (Due: {task.due_date.date()}, Status: {task.status})")

    def update_task(self, task_id, title=None, description=None, due_date=None, status=None):
        for task in self.tasks:
            if task.task_id == task_id:
                if title is not None:
                    task.title = title
                if description is not None:
                    task.description = description
                if due_date is not None:
                    task.due_date = due_date
                if status is not None:
                    task.status = status
                break

    def delete_task(self, task_id):
        self.tasks = [task for task in self.tasks if task.task_id != task_id]

    def save_tasks(self):
        with open("tasks.json", "w") as file:
            json.dump([task.to_dict() for task in self.tasks], file)

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as file:
                task_data = json.load(file)
                self.tasks = [Task.from_dict(data) for data in task_data]
        except FileNotFoundError:
            self.tasks = []


def main():
    obj = TaskManager()

    while True:
        print("\nTask Management System")

        print("1. Add Task")
        print("2. List Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            due_date = input("Enter due date (YYYY-MM-DD): ")
           
            
            due_date = datetime.fromisoformat(due_date)

            obj.add_task(title, description, due_date)
            obj.save_tasks()
            print("Tasks saved. Exiting.")
           
        elif choice == "2":
            status_filter = input(
                "Enter status to filter (or leave blank for all): ")
            if status_filter.strip() == "":
                obj.list_tasks()
            else:
                obj.list_tasks(status_filter)
        elif choice == "3":
            task_id = int(input("Enter task ID to update: "))
            title = input("Enter new title (or leave blank to keep current): ")
            description = input(
                "Enter new description (or leave blank to keep current): ")
            due_date_str = input(
                "Enter new due date (YYYY-MM-DD, or leave blank to keep current): ")
            due_date = datetime.fromisoformat(
                due_date_str) if due_date_str else None
            status = input(
                "Enter new status (or leave blank to keep current): ")
            obj.update_task(task_id, title or None,
                            description or None, due_date, status or None)
            obj.save_tasks()
            print("Task updated. Exiting.")
        elif choice == "4":
            task_id = int(input("Enter task ID to delete: "))
            obj.delete_task(task_id)
        elif choice == "5":
            obj.save_tasks()
            print("Tasks saved. Exiting.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
