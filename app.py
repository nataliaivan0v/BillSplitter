from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Store the menu data globally to pass it to the next page
menu_items = []
names = []
tax = 0
tip = 0
dish_assignments = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dishes', methods=['POST'])
def dishes():
    # Get the menu items, names, and other inputs from the form
    global menu_items, names
    menu_items = list(zip(request.form.getlist('dish_name[]'), request.form.getlist('dish_price[]')))
    names = request.form.getlist('names[]')
    
    # Store tax and tip as well
    global tax, tip
    tax = float(request.form['tax'])
    tip = float(request.form['tip'])
    
    return render_template('dishes.html', names=names, menu_items=menu_items)

@app.route('/submit_assignments', methods=['POST'])
def submit_assignments():
    # Collect the dish selections for each person
    global dish_assignments
    for name in names:
        selected_dishes = request.form.getlist(name)
        dish_assignments[name] = selected_dishes
    
    # Process calculations (similar to the previous logic)
    results = calculate_totals()
    
    return render_template('results.html', results=results)

def calculate_totals():
    # Calculate the total bill
    meal_total = sum(float(price) for name, price in menu_items if name.strip() and price)
    total_with_tax_tip = meal_total + tax + tip
    results = []
    results.append(f"The grand total of the bill is ${total_with_tax_tip:.2f}")

    # Count how many people selected each dish
    dish_counts = {i: 0 for i in range(len(menu_items))}

    for name in dish_assignments:
        for dish in dish_assignments[name]:
            dish_counts[int(dish)] += 1

    # Calculate total amount for each person
    for name in dish_assignments:
        if name.strip():
            personal_total = 0
            for dish in dish_assignments[name]:
                personal_total += float(menu_items[int(dish)][1]) / dish_counts[int(dish)]
        
            percent_of_bill = personal_total / meal_total
            personal_total += round(percent_of_bill * tip, 2)
            personal_total += round(percent_of_bill * tax, 2)
            results.append(f"{name} owes ${personal_total:.2f}")
    
    return results

if __name__ == '__main__':
    app.run(debug=True)
