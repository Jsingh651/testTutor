
function redirectToLanding() {
    window.location.href = "/";
}

document.getElementById('checkout-button').addEventListener('click', function () {
    fetch('/create-checkout-session', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ userId: "{{ user.id }}" }) // Pass the user ID in the request body
    })
        .then(function (response) {
            return response.json();
        })
        .then(function (session) {
            var stripe = Stripe('pk_test_51NDup2FabksylCi830zi3NH1XSTPzSgwNmldMSOZ77XMVUWQeHwvlgP4AVxz7QpbDhwyVs1S4tb52q4lOHUj2F5x00RBGQuLCP');
            stripe.redirectToCheckout({ sessionId: session.sessionId });
        })
        .catch(function (error) {
            console.error('Error:', error);
        });
});

