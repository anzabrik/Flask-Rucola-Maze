# Rucola Maze: a Flask App That Keeps Track of Restaurant Inventory and Purchases

## Video Demo

[Video Demo](https://youtu.be/FuucjgUQ8Vg)

## Built With

Flask (with Blueprints and Jinja), Python, SQLite, WTForms, and BootStrap.

## Summary

The app is intended for the staff of a restaurant. It keeps track of the restaurant inventory and purchases. - shows which menu items are available
- registers purchases
- updates the amount of each ingredient
- checks out whether each menu item is available
- automatically calculates revenue and profit
The manipulations are available to registered users only.

## Structure

The app can be broken down into two sub-apps, each taking form of a separate blueprint:

- 'inventory', which performs all the operations with ingredients, menu items, and purchases. URLs have no prefix as this sub-app is more important.
- 'auth', which is responsible for user authorization and authentication. URLs for this blueprint start with 'auth'.
Each sub-app has a separate views file ('inventory.py' and 'auth.py') and a separate template folder. The sub-apps are brought together via the '\_\_init\_\_.py' file, which contains an app factory function.

## Models

There are four models in addition to the User model: Ingredient, MenuItem, RecipeRequirement, and Purchase.
Ingredient and MenuItem are connected via RecipeRequirement in the following way: a single RecipeRequirement shows how much of a single Ingredient is needed for a certain MenuItem.

So, a MenuItem has many RecipeRequirements and an Ingredient is part of many RecipeRequirements, but a single RecipeRequirement only has one Ingredient and one MenuItem.

## Using the app: the Inventory part

### Ingredients

The 'Ingredients' page lists all ingredients in alphabetical order, including their names, amount in stock and price per unit.
You can manipulate ingredients:

- add ingredients using the respective button at the top the 'Ingredients' page
- edit or delete ingredients using the buttons next to the name

The data from the user is collected via WTForms. Flask's 'flash' function is used to show a message for the user at the top of the page that confirms the user's last action. 

Сonfirmation messages like "You've added the ingredient 'egg', $0,20 per item." seem useful because, as the tables becomes longer, it might be time-consuming to scroll the page down and look for the ingredient you've added to check out whether the action was successful. The messages also  give the user a chance to immediately catch typos. If the user by mistake tries to add an ingredient with the same name, the app refuses to do so and prints out an error message.

### Menu Items

The 'Menu Items' page lists all menu items:
- name (in alphabetical order)
- price
- all recipe requirements (which ingredient and in which quantity is necessary to cook the menu item)
- whether the menu item is available (all ingredienta are in stock)

In the 'Availability' column the staff immediately sees what they can offer the client without the need to visit any additional pages. We will describe the mechanism behind this feature later, in the 'How do we check whether a menu item is available?' section.

You can add, edit or delete Menu Items, with error or confirmation messages, in the same way as ingredients.

### Recipe Requirements

Each menu item has one or more recipe requirement. Each recipe requirement contains the name of the menu item, a single ingredient, and the amount that is needed for this specific menu item.

The 'Add' and 'Edit' pages for Recipe Requirements have a dynamic Select field offering a choice of the existing menu items and ingredients.

#### How do we check whether a menu item is available?

The 'in_stock()' method, which is part of the RecipeRequirement model, takes a single recipe requirement and checks whether the quantity of a certain ingredient that is required in this recipe requirement ('RecipeRequirement.quantity_required') is not more than the quantity of this ingredient that is actually available. In other words, the method does two things:

1. Gets the following two values:

- MenuItem.RecipeRequirement -> RecipeRequirement.Ingredient -> Ingredient.quantity_available
- MenuItem.RecipeRequirement.quantity_required

2. Checks whether the first value isn't less than the second one.

Then, the method returns a Boolean that answers the question: 'Do we have enough of a certain ingredient to cook a certain menu item?'

But, as a single menu item typically contains several ingredients, we'll have to check out each one. This is what the 'is_available()' method does, which is part of the MenuItem model. This method creates a list of all RecipeRequirements for a given MenuItem ('rr_availability_list'). Then, it checks whether they are in stock using the python's 'all()' method and returns a Boolean.

### Purchases

The 'Purchases' page lists all the purchases that have been already made: the name of the menu item and the time. You can add new purchases or delete some of the existing ones.

The 'Add purchase' page shows only the menu items that are currently available. This approach helps to eliminate situation when a customer decides to order something and then finds out that the item is unavailable.

#### What happens when a purchase is added?

As soon as a purchase is added, the required quantity of every ingredient needed for the menu item is subtracted from the available amount of ingredients. The result is reflected in the column 'Quantity available' of the 'Ingredients' page. If as a result of this, a menu item becomes unavailable, this is reflected on the page 'Menu Items'.

In this app, when you add a purchase, it means that the menu item was cooked (the ingredients are subtracted permanently). So, you cannot edit a purchase. You can only completely delete a purchase so it will be ignored in revenue/profit calculations. This means that although the menu item was cooked, the restaurant didn't receive the money for it (e.g. the client found some problems with the dish and refused to pay).

### Profit & Revenue calculations

The app's homepage displays three values:

- total revenue (sum of all recorded purchases)
- total cost of purchases (sum of cost of all ingredients used)
- profit (revenue - cost).