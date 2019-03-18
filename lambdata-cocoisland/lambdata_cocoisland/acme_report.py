import random
from acme import Product

ADJECTIVES=['Awesome', 'Shiny', 'Impressive', 'Portable', 'Improved']
NOUNS=['Anvil', 'Catapult', 'Disguise', 'Mousetrap', '???']

def generate_products():
   products=[]
   total_prod = random.randint(30,100)
   for _ in range(total_prod):
      new_name = random.choice(ADJECTIVES) + ' ' + random.choice(NOUNS)
      new_prod = Product(new_name)
      new_prod.price = random.randint(5,100)
      new_prod.weight = random.randint(5,100)
      new_prod.flammability = random.uniform(0.0, 2.5)
      products.append(new_prod)
   return products

def inventory_report(products):
   names = set() #ensure unique product
   tot_price=0
   tot_weight=0
   tot_flammability=0.0

   for product in products:
      names.add(product.name)
      tot_price += product.price
      tot_weight += product.weight
      tot_flammability += product.flammability

   print('ACME CORPORATION OFFICIAL INVENTORY REPORT')
   print('Unique product names: {}'.format(len(names)))
   print('Average price: {}'.format(tot_price/len(names)))
   print('Average weight: {}'.format(tot_weight/len(names)))
   print('Average flammability: {}'.format(tot_flammability/len(names)))


if __name__ == '__main__':
   p=generate_products()
   inventory_report(p)


