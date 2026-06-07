"""Progress tracking mixin."""

import json
from datetime import datetime


class ProgressMixin:
    """Mixin for PandasPractice."""

    def load_progress(self):
        """Load user progress from file."""
        if self.progress_file.exists():
            with open(self.progress_file, 'r') as f:
                data = json.load(f)
                # Migrate old format to new format
                if "exercises_completed" in data and "exercise_stats" not in data:
                    data["exercise_stats"] = {}
                    for ex in data.get("exercises_completed", []):
                        data["exercise_stats"][ex] = {"count": 1, "total_grade": 100.0, "grades": [100.0]}
                    if "exercises_completed" in data:
                        del data["exercises_completed"]
                return data
        return {
            "exercise_stats": {},
            "last_session": None
        }
    def save_progress(self):
        """Save user progress to file."""
        self.progress["last_session"] = datetime.now().isoformat()
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress, f, indent=2)
    def record_exercise_completion(self, exercise_name, tasks_completed, total_tasks):
        """Record exercise completion with grade."""
        if exercise_name not in self.progress["exercise_stats"]:
            self.progress["exercise_stats"][exercise_name] = {
                "count": 0,
                "total_grade": 0.0,
                "grades": []
            }
        
        grade = (tasks_completed / total_tasks) * 100.0
        self.progress["exercise_stats"][exercise_name]["count"] += 1
        self.progress["exercise_stats"][exercise_name]["total_grade"] += grade
        self.progress["exercise_stats"][exercise_name]["grades"].append(grade)
        self.save_progress()
    def reset_statistics(self):
        """Reset all learning statistics. Returns True if reset, False if cancelled."""
        while True:
            confirm = input("\n⚠️  Are you sure you want to reset all statistics? (yes/no): ").strip().lower()
            if confirm in ['yes', 'y']:
                self.progress["exercise_stats"] = {}
                self.progress["last_session"] = None
                self.save_progress()
                print("\n✅ Statistics reset successfully!")
                return True
            elif confirm in ['no', 'n']:
                print("\n❌ Reset cancelled.")
                return False
            else:
                print("❌ Invalid choice. Please enter 'yes', 'no', 'y', or 'n'.")
