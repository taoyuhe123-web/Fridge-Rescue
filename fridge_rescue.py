"""
Fridge Rescue: Student Food Waste Helper
COMP9001 Python Project Challenge

How to run:
    python fridge_rescue.py

This program uses only Python built-in libraries.
It saves data into 'fridge_rescue_data.json' in the same folder.
"""

import json
import os
from datetime import datetime

DATA_FILE = "fridge_rescue_data.json"

# A small recipe database. You can add more recipes if you want.
RECIPES = [
    {
        "name": "Emergency Fried Rice",
        "ingredients": ["rice", "egg", "vegetables"],
        "time": 12,
        "steps": [
            "Heat a pan with a little oil.",
            "Add egg and vegetables, then add rice.",
            "Stir fry everything together and season to taste."
        ]
    },
    {
        "name": "Quick Omelette",
        "ingredients": ["egg", "tomato", "cheese"],
        "time": 10,
        "steps": [
            "Beat the eggs in a bowl.",
            "Add chopped tomato and cheese.",
            "Cook slowly in a pan until the egg is set."
        ]
    },
    {
        "name": "Student Noodle Bowl",
        "ingredients": ["noodles", "egg", "vegetables"],
        "time": 8,
        "steps": [
            "Boil noodles until soft.",
            "Add vegetables and egg.",
            "Mix with your favourite sauce."
        ]
    },
    {
        "name": "Healthy Tuna Rice Bowl",
        "ingredients": ["rice", "tuna", "cucumber"],
        "time": 7,
        "steps": [
            "Put cooked rice in a bowl.",
            "Add tuna and sliced cucumber.",
            "Mix with mayonnaise or soy sauce."
        ]
    },
    {
        "name": "Tomato Pasta Rescue",
        "ingredients": ["pasta", "tomato", "cheese"],
        "time": 15,
        "steps": [
            "Boil pasta until ready.",
            "Cook tomato in a pan to make a simple sauce.",
            "Add pasta and cheese, then mix well."
        ]
    },
    {
        "name": "Breakfast Yogurt Cup",
        "ingredients": ["yogurt", "banana", "cereal"],
        "time": 3,
        "steps": [
            "Put yogurt into a cup.",
            "Add sliced banana.",
            "Top with cereal for crunch."
        ]
    }
]


def normalise(text):
    """Make user input easier to compare."""
    return text.strip().lower()


def ask_int(prompt, minimum=0, maximum=365):
    """Keep asking until the user enters a valid integer."""
    while True:
        value = input(prompt).strip()
        try:
            number = int(value)
            if minimum <= number <= maximum:
                return number
            print(f"Please enter a number from {minimum} to {maximum}.")
        except ValueError:
            print("Please enter a whole number, for example 3 or 10.")


class FridgeRescue:
    """Main application class for storing food and making suggestions."""

    def __init__(self):
        self.items = []
        self.load_data()

    def load_data(self):
        """Load saved fridge data. If no file exists, use demo items."""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as file:
                    self.items = json.load(file)
            except (json.JSONDecodeError, OSError):
                print("Saved data could not be loaded, so demo data is used.")
                self.items = self.demo_items()
        else:
            self.items = self.demo_items()

    def save_data(self):
        """Save all food items to a JSON file."""
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(self.items, file, indent=4)

    def demo_items(self):
        """Demo food items so the tutor can run the program immediately."""
        return [
            {"name": "egg", "quantity": "6", "category": "protein", "days_left": 5},
            {"name": "tomato", "quantity": "2", "category": "vegetable", "days_left": 1},
            {"name": "rice", "quantity": "1 box", "category": "carb", "days_left": 30},
            {"name": "cheese", "quantity": "half pack", "category": "dairy", "days_left": 3},
            {"name": "noodles", "quantity": "2 packs", "category": "carb", "days_left": 60}
        ]

    def add_item(self):
        print("\nAdd a food item")
        name = normalise(input("Food name: "))
        if name == "":
            print("Food name cannot be empty.")
            return
        quantity = input("Quantity, for example '2', '1 pack', or 'half bottle': ").strip()
        if quantity == "":
            quantity = "1"
        category = normalise(input("Category, for example fruit/protein/carb/dairy: "))
        if category == "":
            category = "other"
        days_left = ask_int("How many days before it expires? ", 0, 365)

        new_item = {
            "name": name,
            "quantity": quantity,
            "category": category,
            "days_left": days_left
        }
        self.items.append(new_item)
        self.save_data()
        print(f"Added {name}. Your fridge list has been saved.")

    def view_items(self):
        print("\nYour fridge items, sorted by expiry date")
        print("-" * 66)
        if len(self.items) == 0:
            print("Your fridge is empty. Add some food first.")
            return

        sorted_items = sorted(self.items, key=lambda item: item["days_left"])
        print(f"{'No.':<5}{'Food':<18}{'Quantity':<14}{'Category':<14}{'Days left'}")
        print("-" * 66)
        for index, item in enumerate(sorted_items, start=1):
            print(f"{index:<5}{item['name']:<18}{item['quantity']:<14}{item['category']:<14}{item['days_left']}")
        print("-" * 66)

    def remove_item(self):
        if len(self.items) == 0:
            print("Your fridge is empty.")
            return

        self.view_items()
        sorted_items = sorted(self.items, key=lambda item: item["days_left"])
        choice = ask_int("Enter the number of the item you want to remove: ", 1, len(sorted_items))
        item_to_remove = sorted_items[choice - 1]
        self.items.remove(item_to_remove)
        self.save_data()
        print(f"Removed {item_to_remove['name']} from your fridge list.")

    def check_expiry_risk(self):
        print("\nExpiry risk check")
        print("-" * 50)
        if len(self.items) == 0:
            print("No food to check yet.")
            return

        urgent = []
        soon = []
        safe = []

        for item in self.items:
            if item["days_left"] <= 1:
                urgent.append(item)
            elif item["days_left"] <= 3:
                soon.append(item)
            else:
                safe.append(item)

        print(f"Urgent, use today or tomorrow: {len(urgent)} item(s)")
        for item in sorted(urgent, key=lambda x: x["days_left"]):
            print(f"  - {item['name']} ({item['days_left']} day left)")

        print(f"\nUse soon: {len(soon)} item(s)")
        for item in sorted(soon, key=lambda x: x["days_left"]):
            print(f"  - {item['name']} ({item['days_left']} days left)")

        print(f"\nSafe for now: {len(safe)} item(s)")
        print("-" * 50)

    def find_item(self, ingredient):
        """Find whether an ingredient exists in the fridge list."""
        ingredient = normalise(ingredient)
        for item in self.items:
            item_name = normalise(item["name"])
            if ingredient in item_name or item_name in ingredient:
                return item
        return None

    def recipe_score(self, recipe):
        """
        Create a rescue score for a recipe.
        The score rewards recipes that use many existing items and urgent items.
        """
        required = recipe["ingredients"]
        matched = []
        missing = []
        urgent_used = []
        urgency_bonus = 0

        for ingredient in required:
            item = self.find_item(ingredient)
            if item is None:
                missing.append(ingredient)
            else:
                matched.append(ingredient)
                if item["days_left"] <= 1:
                    urgency_bonus += 15
                    urgent_used.append(f"{item['name']} ({item['days_left']} day left)")
                elif item["days_left"] <= 3:
                    urgency_bonus += 8
                    urgent_used.append(f"{item['name']} ({item['days_left']} days left)")

        match_score = (len(matched) / len(required)) * 70
        rescue_score = int(min(100, match_score + urgency_bonus))

        return {
            "recipe": recipe,
            "score": rescue_score,
            "matched": matched,
            "missing": missing,
            "urgent_used": urgent_used
        }

    def suggest_meals(self):
        print("\nMeal rescue suggestions")
        print("-" * 60)
        if len(self.items) == 0:
            print("Your fridge is empty. Add food items first.")
            return []

        results = []
        for recipe in RECIPES:
            results.append(self.recipe_score(recipe))

        results.sort(key=lambda result: result["score"], reverse=True)

        for index, result in enumerate(results[:5], start=1):
            recipe = result["recipe"]
            missing_text = ", ".join(result["missing"]) if result["missing"] else "nothing"
            matched_text = ", ".join(result["matched"]) if result["matched"] else "nothing"
            print(f"{index}. {recipe['name']}  | Rescue score: {result['score']}/100")
            print(f"   Time needed: about {recipe['time']} minutes")
            print(f"   You already have: {matched_text}")
            print(f"   Missing: {missing_text}")
            if result["urgent_used"]:
                print("   Good choice because it uses: " + ", ".join(result["urgent_used"]))
            print()
        return results

    def show_recipe_steps(self):
        results = self.suggest_meals()
        if not results:
            return

        choice = ask_int("Choose a recipe number to see cooking steps: ", 1, min(5, len(results)))
        selected = results[choice - 1]
        recipe = selected["recipe"]

        print(f"\nHow to make {recipe['name']}")
        print("-" * 50)
        for number, step in enumerate(recipe["steps"], start=1):
            print(f"{number}. {step}")
        if selected["missing"]:
            print("\nShopping list: " + ", ".join(selected["missing"]))
        else:
            print("\nShopping list: You have everything needed.")

    def daily_rescue_plan(self):
        print("\nToday's mini rescue plan")
        print("-" * 50)
        if len(self.items) == 0:
            print("No food found. Add items first.")
            return

        most_urgent = sorted(self.items, key=lambda item: item["days_left"])[0]
        best_recipe = sorted([self.recipe_score(recipe) for recipe in RECIPES],
                             key=lambda result: result["score"], reverse=True)[0]

        print("1. Check first:")
        print(f"   Your most urgent item is {most_urgent['name']} ({most_urgent['days_left']} day(s) left).")
        print("2. Recommended meal:")
        print(f"   {best_recipe['recipe']['name']} with a rescue score of {best_recipe['score']}/100.")
        if best_recipe["missing"]:
            print("3. Buy only these missing items:")
            print("   " + ", ".join(best_recipe["missing"]))
        else:
            print("3. No shopping needed for this meal.")
        print("4. Student tip:")
        print("   Cook the urgent item first to save money and reduce food waste.")

    def show_summary(self):
        print("\nProject summary")
        print("-" * 60)
        print("Fridge Rescue helps students decide what to cook before food expires.")
        print("It stores fridge items, checks expiry risk, suggests meals, and creates a small shopping list.")
        print("Advanced Python concepts used: classes, functions, lists/dictionaries, JSON file handling, sorting, input validation.")
        print("Data file:", os.path.abspath(DATA_FILE))
        print("Current time:", datetime.now().strftime("%Y-%m-%d %H:%M"))


def print_menu():
    print("\n" + "=" * 60)
    print("FRIDGE RESCUE - Student Food Waste Helper")
    print("=" * 60)
    print("1. View my fridge")
    print("2. Add a food item")
    print("3. Remove a food item")
    print("4. Check expiry risk")
    print("5. Suggest meals")
    print("6. Show cooking steps and shopping list")
    print("7. Create today's mini rescue plan")
    print("8. Show project summary")
    print("9. Save and exit")


def main():
    app = FridgeRescue()
    print("Welcome to Fridge Rescue!")
    print("This program helps students reduce food waste and decide what to cook.")

    while True:
        print_menu()
        choice = ask_int("Choose an option from 1 to 9: ", 1, 9)

        if choice == 1:
            app.view_items()
        elif choice == 2:
            app.add_item()
        elif choice == 3:
            app.remove_item()
        elif choice == 4:
            app.check_expiry_risk()
        elif choice == 5:
            app.suggest_meals()
        elif choice == 6:
            app.show_recipe_steps()
        elif choice == 7:
            app.daily_rescue_plan()
        elif choice == 8:
            app.show_summary()
        elif choice == 9:
            app.save_data()
            print("Your data has been saved. Goodbye!")
            break


if __name__ == "__main__":
    main()
