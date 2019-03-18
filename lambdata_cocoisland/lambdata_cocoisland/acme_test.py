#!/usr/bin/env python

import unittest
from acme import Product,BoxingGlove
from acme_report import generate_products, ADJECTIVES, NOUNS

class AcmeProductTests(unittest.TestCase):
   '''Making sure Acme products are the tops!'''

   def test_default_product_price(self):
      prod=Product('Test Product')
      self.assertEqual(prod.price, 10)

   def test_default_product_weight(self):
      prod=Product('Test 2 product')
      self.assertEqual(prod.weight, 20)

   def test_default_boxingGlove(self):
      glove=BoxingGlove('Test Punch')
      self.assertEqual(glove.weight, 10) 
      self.assertEqual(glove.stealability(), 'Very stealable!')
      self.assertEqual(glove.explode(), "...it's a glove.")

   def test_stealable_and_explode(self):
      bomb = Product('Explosive')
      bomb.price=200
      bomb.weight=30
      bomb.flammability=2.5
      self.assertEqual(bomb.stealability(), 'Very stealable!')
      self.assertEqual(bomb.explode(), '...BABOOM!!')

class AcmeReportTests(unittest.TestCase):
   #def test_default_num_products(self):
   #   self.assertEqual(len(generate_products()), 30)

   def test_legal_names(self):
      for product in generate_products():
         adjective, noun = product.name.split()
         self.assertIn(adjective, ADJECTIVES)
         self.assertIn(noun, NOUNS)


if __name__ == '__main__':
   unittest.main()
