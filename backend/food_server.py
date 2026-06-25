from flask import Flask, render_template,redirect,request, jsonify
from backend.food_list import add_food_item, view_food_items, update_items, delete_item


app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../asset"
)

def food_a(app):
    
  
    @app.route('/view_items')
    def view_items():
        return render_template("dashbord_business.html") ###

   
    @app.route('/api/listings')
    def api_listings():
        business_id = 1
        items = view_food_items(business_id)
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

        business_id = 1
        if request.method== 'POST':
            food_name = request.form.get("food_name") 
            price = request.form.get("price") 
            quantity = request.form.get("quantity") 
            description = request.form.get("description") 
            pickup_address = request.form.get("pickup_address")

            add_food_item( 
                business_id, 
                food_name,
                price, 
                quantity, 
                description, 
                pickup_address )
            
        return redirect ("/view_items")
    
    @app.route ("/delete-items/<int:listing_id>")
    def delete_items_list(listing_id):
        business_id = 1
        
        delete_item(
            listing_id,
            business_id
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
            
            update_items(
                listing_id,
                business_id,
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