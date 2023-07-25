
__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"


# from models import
from models import Product, Transaction, User, Tag


def search(term):
    term = term.lower()
    query = Product.select().where(
        (Product.name.contains(term)) | (Product.description.contains(term))
    )
    product_names = [product.name for product in query]

    return product_names
    # return list(query)


def list_user_products(user_id):
    try:
        user_id = int(user_id)
    except ValueError:
        print("Invalid user_id. Please provide a valid integer user_id.")
        return []

    user_products = Product.select().join(Transaction).join(User).where(User.id == user_id)
    products = []
    for a in user_products:
        products.append(a)
        for a in products:
            return a.name


def list_products_per_tag(tag_id):
    try:
        tag_id = int(tag_id)
    except ValueError:
        print("Invalid tag_id. Please provide a valid integer tag_id.")
        return ''

    tag_products = Product.select().join(Tag).where(Tag.id == tag_id)

    product_names = [product.name for product in tag_products]

    return product_names

# example product
new_product_details = {
        'name': 'Piano',
        'description': 'Honky-tonk',
        'price_per_unit': 222.00,
        'quantity_in_stock': 1,
        'tags': 'Music',
        'owner': 2   
    }


def add_product_to_catalog(user_id, product):
    try:
        user_id = int(user_id)
    except ValueError:
        print("Invalid user_id. Please provide a valid integer user_id.")
        return ''

    try:
        User.get(User.id == user_id)
    except User.DoesNotExist:
        print(f"User with ID {user_id} does not exist.")
        return ''

    try:
        Product.create(
            name=product['name'],
            description=product['description'],
            price_per_unit=product['price_per_unit'],
            quantity_in_stock=product['quantity_in_stock'],
            tags=product.get('tags'),
            owner=user_id
        )
        print("Product added to the catalog successfully.")
        return ''
    except Exception as e:
        print(f"Error adding product to the catalog: {e}")
        return ''


def update_stock(product_id, new_quantity):
    try:
        product_id = int(product_id)
    except ValueError:
        print("Invalid product_id. Please provide a valid integer product_id.")
        return ''

    try:
        product = Product.get(Product.id == product_id)
    except Product.DoesNotExist:
        print(f"Product with ID {product_id} does not exist.")
        return ''

    try:
        # Update the quantity in stock for the product
        product.quantity_in_stock = new_quantity
        product.save()
        print("Stock quantity updated successfully.")
    except Exception as e:
        print(f"Error updating stock quantity: {e}")


def purchase_product(product_id, buyer_id, quantity):
    try:
        product_id = int(product_id)
        buyer_id = int(buyer_id)
        quantity = int(quantity)
    except ValueError:
        print("Invalid input. Please provide valid integer values for product_id, buyer_id, and quantity.")
        return ''

    try:
        # Check if the product with the given product_id exists in the database
        product = Product.get(Product.id == product_id)

        # Check if the buyer with the given buyer_id exists in the database
        buyer = User.get(User.id == buyer_id)

        # Check if the requested quantity is available in stock
        if product.quantity_in_stock < quantity:
            print(f"Insufficient quantity in stock. Available: {product.quantity_in_stock}, Requested: {quantity}")
            return ''

        # Create a new transaction for the purchase
        transaction = Transaction.create(buyer=buyer, product=product, quantity_purchased=quantity)

        # Update the quantity in stock for the product after the purchase
        product.quantity_in_stock -= quantity
        product.save()

        print("Purchase successful. Transaction ID:", transaction.id)
        return ''
    except Product.DoesNotExist:
        print(f"Product with ID {product_id} does not exist.")
        return ''
    except User.DoesNotExist:
        print(f"Buyer with ID {buyer_id} does not exist.")
    except Exception as e:
        print(f"Error during the purchase: {e}")


def remove_product(product_id) -> None:
    try:
        product_id = int(product_id)
    except ValueError:
        print("Invalid product_id. Please provide a valid integer product_id.")
        return ''

    try:
        # Check if the product with the given product_id exists in the database
        product = Product.get(Product.id == product_id)

        # Remove the product from the catalog
        product.delete_instance()
        print("Product removed from the catalog successfully.")
        return ''
    except Product.DoesNotExist:
        print(f"Product with ID {product_id} does not exist.")
        return ''
    except Exception as e:
        print(f"Error while removing product: {e}")
        return ''


if __name__ == "__main__":

    # # Example search
    print(search("Star Wars"))
 
    print(list_user_products(2))

    print(list_products_per_tag(3))

    print(add_product_to_catalog(2, new_product_details))

    print(update_stock(1, 5))

    print(purchase_product(2, 1, 1))

    print(remove_product(1))
