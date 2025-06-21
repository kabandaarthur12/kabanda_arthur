class Shop:
    def __init__(self, name):
        self.name = name
        self.products = {
            "apple": 1.0,
            "banana": 0.5,
            "orange": 0.75
        }
    
    def calculate_price(self, product, quantity):
        """Calculate regular price"""
        if product not in self.products:
            return "Product not found"
        price = self.products[product] * quantity
        return f"Total price: ${price}"

class DiscountShop(Shop):
    def calculate_price(self, product, quantity):
        """Override calculate_price to add 10% discount"""
        if product not in self.products:
            return "Product not found"
        original_price = self.products[product] * quantity
        discount_price = original_price * 0.9  # 10% discount
        return f"Original price: ${original_price}\nAfter 10% discount: ${discount_price}"


if __name__ == "__main__":
    
    print("\n=== Method Overriding Example ===")
    regular_shop = Shop("Regular Store")
    discount_shop = DiscountShop("Discount Store")
    
    # Same method, different behavior
    print("\nBuying 5 apples from regular shop:")
    print(regular_shop.calculate_price("apple", 5))
    
    print("\nBuying 5 apples from discount shop:")
    print(discount_shop.calculate_price("apple", 5))