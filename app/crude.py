from app import db
from app import models


def add_query_to_database(username, email, query, discount):
    user = models.User.query.filter_by(email=email).first()

    if not user:
        # Create a new user if the email doesn't exist
        user = models.User(name=username, email=email)
        db.session.add(user)
        db.session.commit()

    new_query = models.Query(user=user, query_title=query, discount=discount)
    db.session.add(new_query)
    db.session.commit()


def add_product_history_data(product_id, product_name, current_price, query_obj):
    product = models.Product.query.filter_by(id=product_id).first()
    if not product:
        # Create a new product if it doesn't exist
        product = models.Product(id=product_id, name=product_name, price=current_price)
        db.session.add(product)
        db.session.commit()
        return

    # Add product data to the history table
    history_entry = models.History(product=product, price=current_price)
    db.session.add(history_entry)
    db.session.commit()
    discount = query_obj.discount  # Вопрос что это???
    initial_price = product.price

    if current_price < initial_price - (initial_price * (discount / 100)):
        # Record a notification if the current price is lower than the discounted initial price
        notification = models.Notification(
            product=product,
            query=query_obj,
            previous_price=initial_price,
            current_price=current_price
        )
        db.session.add(notification)
        db.session.commit()
        return True
    return
