from flask import Flask, render_template, request, redirect, url_for, abort, session
import json

app = Flask(__name__)

def createFood():
    food = []
    food.append( 'Veggies' )
    food.append( 'Breads')
    food.append( 'Desserts' )
    food.append( 'Chinese' )
    food.append( 'Beverages' )
    #return json.dumps(food)
    return food

categories = createFood()
Veggies = [ 'ShahiPaneer', 'Mushroom', 'DalMakhani', 'PaneerPyaza' ]
Breads = [ 'Naan', 'Kulcha', 'Roti', 'Phulka', 'Paratha' ]
Desserts = [ 'GulabJamun', 'Rasgulla', 'IceCream' ]
Chinese = [ 'Noodles', 'Choupsey', 'Momos', 'Haka-Noodles' ]
Beverages = [ 'Coke', 'LimeWater', 'FruitPunch', 'LichiJuice' ]

def check_categ( cat ):
    if cat == 'Veggies':
        return Veggies
    elif cat == 'Breads':
        return Breads
    elif cat == 'Desserts':
        return Desserts
    elif cat == 'Chinese':
        return Chinese
    elif cat == 'Beverages':
        return Beverages

finalOrder = []
def finalOrder( obj ):
    order =  obj.split(',')
    cat = "";
    print order
    if order[0] == '':
        return
    elif order[0] in Veggies:
        cat = "Veggies"
    elif order[0] in Chinese:
        cat = "Chinese"
    elif order[0] in Beverages:
        cat = "Beverages"
    elif order[0] in Breads:
        cat = "Breads"
    elif order[0] in Desserts:
        cat = "Desserts"
    print cat

@app.route('/order', methods=['GET', 'POST'])
def order_placed():
    finalOrder( str( request.form["order"] ) )
    return "Yes"

@app.route( '/', methods=['GET','POST'] )
def menu_page():
    if request.method == 'GET':
        return render_template('menu.html', categ=categories )
    elif request.method == 'POST':
        items = check_categ( str( request.form["category"] ) )
        print items
        print str( request.form["category"] )
        global USERID
        print USERID
        return render_template( 'temp.html', categName = str( request.form["category"] ), items=items, userid=USERID )
if __name__ == '__main__':
    app.run(debug=True)
