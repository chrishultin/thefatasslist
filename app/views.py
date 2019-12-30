from flask import render_template, flash, redirect
from app import app
from pymongo import MongoClient
from .forms import UpdateRestaurant
import os

mongoIP = os.environ['MONGO_PORT_27017_TCP_ADDR']
mongoPort = os.environ['MONGO_PORT_27017_TCP_PORT']


mongoServer = MongoClient('mongodb://{}:{}'.format(mongoIP, mongoPort))
mongoDB = mongoServer.fatasslist
restaurants = mongoDB.restaurants


@app.route('/')
@app.route('/index')
def index():
    locationsArray = list(restaurants.distinct('location'))
    restaurantsArray = list(restaurants.find({"$or":[ {"closed":{"$exists": False}}, {"closed":{"$eq": True}}]}) )
    return render_template('mainlist.html',
                           locations=locationsArray,
                           restaurants=restaurantsArray)

@app.route('/honorable')
def honorable():
    locationsArray = list(restaurants.distinct('location'))
    restaurantsArray = list(restaurants.find({ 'honorablemention': True }))
    #restaurantsArray = list(restaurants.find())
    return render_template('mainlist.html',
                           locations=locationsArray,
                           restaurants=restaurantsArray)

@app.route('/champions')
def champions():
    locationsArray = list(restaurants.distinct('location'))
    restaurantsArray = list(restaurants.find({ 'halloffame': True }))
    #restaurantsArray = list(restaurants.find())
    return render_template('mainlist.html',
                           locations=locationsArray,
                           restaurants=restaurantsArray)

@app.route('/closed')
def closed():
    locationsArray = list(restaurants.distinct('location'))
    restaurantsArray = list(restaurants.find({ 'closed': True }))
    #restaurantsArray = list(restaurants.find())
    return render_template('mainlist.html',
                           locations=locationsArray,
                           restaurants=restaurantsArray)

@app.route('/admin')
def admin():
    restaurantsArray = list(restaurants.find())
    return render_template('admin.html',
                           restaurants=restaurantsArray)

@app.route('/admin/<string:name>', methods=['GET','POST'])
def restaurant_page(name="None"):
    restaurant = restaurants.find_one({ "name" : name })
    restaurantsArray = list(restaurants.find())
    form = UpdateRestaurant()
    if form.validate_on_submit():
        if form.deleteField.data:
            print 'Deleting Restaurant'
            result = restaurants.delete_one({
                'name': form.orig_name.data
            })
        elif form.orig_name.data == 'None':
            print 'Adding New Restaurant'
            result = restaurants.insert_one({
                        'name': form.rest_name.data,
                        'category': form.categories.data.replace('\r','').split('\n'),
                        'price': float(form.price.data),
                        'ambiance': float(form.ambiance.data),
                        'food': float(form.food.data),
                        'tried': form.consumed.data.replace('\r','').split('\n'),
                        'commentary': form.commentary.data,
                        'vegan-gluten': form.vegangluten.data,
                        'honorablemention': form.honorablemention.data,
                        'halloffame': form.champion.data,
                        'location': form.location.data,
                        'closed': bool(form.closed.data)
            })
        else:
            print 'Updating Restaurant'
            result = restaurants.update_one(
                { "name": form.orig_name.data },
                {
                    '$set' : {
                        'name': form.rest_name.data,
                        'category': form.categories.data.replace('\r','').split('\n'),
                        'price': float(form.price.data),
                        'ambiance': float(form.ambiance.data),
                        'food': float(form.food.data),
                        'tried': form.consumed.data.replace('\r','').split('\n'),
                        'commentary': form.commentary.data,
                        'vegan-gluten': form.vegangluten.data,
                        'honorablemention': form.honorablemention.data,
                        'halloffame': form.champion.data,
                        'location': form.location.data,
                        'closed': bool(form.closed.data)
                    }
                })
        return redirect('/admin')
    if name == 'None':
        restaurant = {'name': 'New Restaurant'}
        form.orig_name.data = 'None'
        form.rest_name.data = ''
        form.categories.data = ''
        form.price.data = 0
        form.ambiance.data = 0
        form.food.data = 0
        form.consumed.data = ''
        form.commentary.data = ''
        form.vegangluten.data = False
        form.honorablemention.data = False
        form.champion.data = False
        form.location.data = 'Denver, CO'
        form.closed.data = False
    else:
        form.orig_name.data = restaurant['name']
        form.rest_name.data = restaurant['name']
        form.categories.data = "\n".join(restaurant['category'])
        form.price.data = restaurant['price']
        form.ambiance.data = restaurant['ambiance']
        form.food.data = restaurant['food']
        form.consumed.data = "\n".join(restaurant['tried'])
        form.commentary.data = restaurant['commentary']
        form.vegangluten.data = restaurant['vegan-gluten']
        form.honorablemention.data = restaurant['honorablemention']
        form.champion.data = restaurant['halloffame']
        form.location.data = restaurant['location']
        form.closed.data = restaurant['closed']
    #categoriesString =
    return render_template('modify_restaurant.html',
                           restaurant=restaurant,
                           restaurants=restaurantsArray,
                           form=form)
