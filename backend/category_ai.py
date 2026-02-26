def categorize_transaction(merchant_name: str):

    merchant = merchant_name.lower()

    category_map = {
        "Food": [
            "swiggy",
            "zomato",
            "starbucks",
            "dominos",
            "pizza",
            "restaurant",
            "cafe"
        ],
        "Transport": [
            "uber",
            "ola",
            "rapido",
            "metro",
            "irctc"
        ],
        "Shopping": [
            "amazon",
            "flipkart",
            "myntra",
            "meesho"
        ],
        "Entertainment": [
            "netflix",
            "spotify",
            "bookmyshow"
        ],
        "Bills": [
            "electricity",
            "bescom",
            "water",
            "internet",
            "jio",
            "airtel"
        ]
    }

    for category, keywords in category_map.items():
        for word in keywords:
            if word in merchant:
                return category

    return "Others"