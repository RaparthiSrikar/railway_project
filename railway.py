"""
Railway Ticket Booking Application
-----------------------------------
Base ticket price : Rs. 1000

Pricing rules:
  Male,   age >= 60  -> Senior Citizen -> 30% discount -> Rs. 700
  Male,   age <  60  -> Normal Citizen -> 0%  discount -> Rs. 1000
  Female, age >= 60  -> Senior Citizen -> 50% discount -> Rs. 500
  Female, age <  60  -> Normal Citizen -> 30% discount -> Rs. 700

Age validation:
  Age must be between 0 and 200 (inclusive).
  Negative age or age above 200 -> "Please enter the valid age"
"""

BASE_PRICE = 1000


def get_valid_gender():
    """Keep asking until the user enters a valid gender."""
    while True:
        gender = input("Enter your gender (M/F): ").strip().lower()
        if gender in ("m", "male"):
            return "male"
        elif gender in ("f", "female"):
            return "female"
        else:
            print("Please enter a valid gender (M/F)")


def get_valid_age():
    """Keep asking until the user enters a valid age (0-200)."""
    while True:
        age_input = input("Enter your age: ").strip()
        try:
            age = int(age_input)
        except ValueError:
            print("Please enter the valid age")
            continue

        if age < 0 or age > 200:
            print("Please enter the valid age")
            continue

        return age


def validate_inputs(gender, age):
    """Validate gender and age. Returns (is_valid, parsed_gender, parsed_age, error_message)."""
    if gender is None or str(gender).strip().lower() not in ("m", "male", "f", "female"):
        return False, None, None, "Please enter a valid gender (M/F)"
    
    clean_gender = "male" if str(gender).strip().lower() in ("m", "male") else "female"

    try:
        age_int = int(age)
    except (ValueError, TypeError):
        return False, None, None, "Please enter the valid age"

    if age_int < 0 or age_int > 200:
        return False, None, None, "Please enter the valid age"

    return True, clean_gender, age_int, None


def calculate_ticket_price(gender, age):
    """Return (category, discount_percent, final_price) based on rules above."""
    if gender == "male":
        if age >= 60:
            category = "Senior Citizen"
            discount = 30
        else:
            category = "Normal Citizen"
            discount = 0
    else:  # female
        if age >= 60:
            category = "Senior Citizen"
            discount = 50
        else:
            category = "Normal Citizen"
            discount = 30

    final_price = BASE_PRICE - (BASE_PRICE * discount / 100)
    return category, discount, final_price


def main():
    print("===== Railway Ticket Booking =====")
    gender = get_valid_gender()
    age = get_valid_age()

    category, discount, final_price = calculate_ticket_price(gender, age)

    print("\n----- Ticket Details -----")
    print(f"Gender      : {gender.capitalize()}")
    print(f"Age         : {age}")
    print(f"Category    : {category}")
    print(f"Base Price  : Rs. {BASE_PRICE}")
    print(f"Discount    : {discount}%")
    print(f"Final Price : Rs. {final_price:.0f}")


if __name__ == "__main__":
    main()