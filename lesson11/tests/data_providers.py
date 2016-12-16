from model.product import Product


valid_products = [[],  # No elements
                  [Product('popular', 'Blue Duck', 1)],  # single product
                  [Product('popular', 'Blue Duck', 2),  # multiple products
                   Product('popular', 'Red Duck', 3),
                   Product('campaigns', 'Yellow Duck', 1, 'Small')]]
