from flask import Flask, render_template, request, jsonify
from railway import BASE_PRICE, calculate_ticket_price, validate_inputs

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    data = request.get_json(silent=True) or {}
    gender = data.get('gender')
    age = data.get('age')

    is_valid, parsed_gender, parsed_age, error_msg = validate_inputs(gender, age)

    if not is_valid:
        return jsonify({
            'success': False,
            'error': error_msg
        }), 400

    category, discount, final_price = calculate_ticket_price(parsed_gender, parsed_age)
    discount_amount = BASE_PRICE * (discount / 100)

    return jsonify({
        'success': True,
        'gender': parsed_gender,
        'age': parsed_age,
        'category': category,
        'base_price': BASE_PRICE,
        'discount_percent': discount,
        'discount_amount': discount_amount,
        'final_price': final_price
    })

if __name__ == '__main__':
    print("Starting Railway Ticket Booking Web Server at http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
