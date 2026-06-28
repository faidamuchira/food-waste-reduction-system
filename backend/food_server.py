from flask import Flask, render_template,redirect,request, jsonify
from food_list import FoodItems

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../asset"
)

business_db = FoodItems(business_id=1)


def food_a(app):
    
  
    @app.route('/view_items')
    def view_items():
        return render_template("dashbord_business.html") ###

   
    @app.route('/api/listings')
    def api_listings():
        items = business_db.view_food_items()
        return jsonify(items)
    
    # def view_items():
    #     business_id = 1
    #     items = view_food_items(business_id)
        
        
    #     return render_template(
    #         "dashbord_business.html",
    #         items=items
    #     )


    @app.route('/add_items', methods= ['GET' , 'POST'])
    def add_items():

        if request.method== 'POST':
            food_name = request.form.get("food_name") 
            price = request.form.get("price") 
            quantity = request.form.get("quantity") 
            description = request.form.get("description") 
            pickup_address = request.form.get("pickup_address")

            business_db.add_food_item( 
                food_name,
                price, 
                quantity, 
                description, 
                pickup_address )
            
        return redirect ("/view_items")
    
    @app.route ("/delete-items/<int:listing_id>")
    def delete_items_list(listing_id):
        
        
        business_db.delete_item(
            listing_id,
        )

        return redirect ("/view_items")
    
    @app.route ("/update-items/<int:listing_id>", methods=["GET", "POST"])
    def update_items_list(listing_id):
        print("UPDATE CLICKED")
        business_id = 1
        if request.method =="POST":
            print("POST RECEIVED")
            food_name = request.form.get("food_name") 
            price = request.form.get("price") 
            quantity = request.form.get("quantity") 
            description = request.form.get("description") 
            pickup_address = request.form.get("pickup_address")
            
            business_db.update_items(
                listing_id,            
                food_name,
                description,
                price,
                quantity,
                pickup_address
            )

        return redirect ("/view_items")


food_a(app)
if __name__ == "__main__":
    app.run(debug=True)