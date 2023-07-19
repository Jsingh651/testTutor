from flask import Flask, render_template, request, jsonify, session, redirect
import stripe
from flask_app.models.users import User
from flask_app import app

stripe.api_key = 'sk_test_51NDup2FabksylCi8SFvbhtLIVxxBS1gZ3MUvH1lq9sKc8tjJgllKghz1gPVsm6rybRXsQ3kVdoIssPDdaDFii2AK00NH08t73i'


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    user_id = request.json['userId']
    user = User.get_one({'id': user_id})
    if user:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    # Replace with your Stripe Price ID for the monthly subscription
                    'price': 'price_1NEP8ZFabksylCi8e5lcSdZj',
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url='http://127.0.0.1:4242/success34iubbuyhgugiuBIBv2?' + \
            user_id,  # Pass user ID as a query parameter
            cancel_url='http://127.0.0.1:4242/',
            customer=user.stripe_customer_id,
            metadata = {
                        'selected_product': 'premium38'
                    }
        )

        return jsonify({'sessionId': session.id})
    else:
        return jsonify({'error': 'User not found'})


@app.route('/success34iubbuyhgugiuBIBv2', methods=['GET'])
def succcesss():
    return redirect('/')


@app.route('/create-checkout-session/premium', methods=['POST'])
def create_checkout_sessionadvanced():
    user_id = request.json['userId']
    user = User.get_one({'id': user_id})
    if user:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': 'price_1NEP9zFabksylCi8BHQMlGme',
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url='http://127.0.0.1:4242/success34iubbuyhgugiuBIBv2?' +
            user_id,
            cancel_url='http://127.0.0.1:4242/',
            customer=user.stripe_customer_id,
            metadata = {
                        'selected_product': 'premium70'
                    }
        )

        return jsonify({'sessionId': session.id})
    else:
        return jsonify({'error': 'User not found'})


