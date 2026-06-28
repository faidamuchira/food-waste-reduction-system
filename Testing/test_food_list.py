import unittest
from backend.food_list import FoodItems

class TestFoodItems(unittest.TestCase):

    def setUp(self):
        self.food_items = FoodItems(business_id=1)

    def test_add_food_item(self):
        result,output = self.food_items.add_food_item(
            food_name= "food_1_test",
            price = 10,
            quantity = 5,
            description ="Testing food items",
            pickup_address ="London"
        )
        
        self.assertEqual(output, "Food item has been added successfully.")
        self.assertTrue(result)
        
    def test_view_food_items(self): 
        result = self.food_items.view_food_items()
        self.assertIsNotNone(result)

    def test_delete_item(self):

        item_db = self.food_items.view_food_items()
        found_item = None
        for item in item_db:
            if item['food_name'] ==  "food_1_test":
                found_item = item ['listing_id']
                break
        
        if found_item is not None:
            result, output = self.food_items.delete_item(found_item)
            self.assertTrue(result)
        else:
            self.fail("could not find the item to delete")
    
    def test_update_item(self):
        result,output = self.food_items.add_food_item(
            food_name= "Updating_item_test",
            price = 10,
            quantity = 5,
            description ="update food items",
            pickup_address ="London"
        )

        self.assertTrue(result)
        

        item_db = self.food_items.view_food_items()
        found_item = None

        for item in item_db:
            if item ["food_name"] == "Updating_item_test":
                found_item = item ["listing_id"]
                break
        
        if found_item is not None:
            result, output = self.food_items.update_items(
                listing_id= found_item,
                food_name="updated_item_sucess",
                description ="Testing Updated food items",
                pickup_address ="London",
                price=10,
                quantity=10

            )

            self.assertTrue(result)
        
        else:
            self.fail("unable to update")
    
    #def test_update_item(self):
    #result, output = self.food_tems.delete_item(1)
    #self.assertTrue(result)
if __name__ == "__main__":
    unittest.main()