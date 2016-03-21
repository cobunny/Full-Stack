from flask import Flask, render_template, request, redirect, url_forfrom sqlalchemy import create_engine, asc, descfrom sqlalchemy.orm import sessionmakerfrom database_setup import Category, CategoryItem, Baseimport random, stringapp = Flask(__name__, static_url_path='/static')# Connect to Database and create database sessionengine = create_engine('sqlite:///catalog.db')Base.metadata.bind = engineDBSession = sessionmaker(bind=engine)session = DBSession()# Show all categories@app.route('/')@app.route('/category/')def showCategories():    categories = session.query(Category).order_by(asc(Category.name))    items = session.query(CategoryItem).order_by(desc(CategoryItem.lastTime)).limit(10)    return render_template('categories.html', categories=categories, items=items)# Show a category item@app.route('/category/<int:category_id>/')@app.route('/category/<int:category_id>/categoryItem/')def showItems(category_id):    category = session.query(Category).filter_by(id=category_id).one()    items = session.query(CategoryItem).filter_by(        category_id=category_id).all()    return render_template('categoryitem.html', items=items, category=category)# Create a new category@app.route('/category/new/', methods=['GET', 'POST'])def newCategory():    if request.method == 'POST':        newCategory = Category(name=request.form['name'])        session.add(newCategory)        session.commit()        return redirect(url_for('showCategories'))    else:        return render_template('newcategory.html')# Delete a new category@app.route('/category/<int:category_id>/delete/', methods=['GET', 'POST'])def deleteCategory(category_id):    categoryToDelete = session.query(        Category).filter_by(id=category_id).one()    if request.method == 'POST':        session.delete(categoryToDelete)        session.commit()        return redirect(url_for('showCategories'))    else:        return render_template('deletecategory.html', category=categoryToDelete)# Edit a restaurant@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])def editCategory(category_id):    editedCategory= session.query(        Category).filter_by(id=category_id).one()    if request.method == 'POST':        if request.form['name']:            editedCategory.name = request.form['name']            return redirect(url_for('showCategories'))    else:        return render_template('editcategory.html', category=editedCategory)# Create a new category item@app.route('/category/<int:category_id>/categoryItem/new/', methods=['GET', 'POST'])def newCategoryItem(category_id):    category = session.query(Category).filter_by(id=category_id).one()    if request.method == 'POST':        newCategoryItem = CategoryItem(name=request.form['item-name'], description=request.form[            'item-description'], category_id=category_id)        session.add(newCategoryItem)        session.commit()        return redirect(url_for('showItems', category_id=category_id))    else:        return render_template('newcategoryitem.html', category_id=category_id, category=category)if __name__ == '__main__':    app.secret_key = 'super_secret_key'    app.debug = True    app.run(host='0.0.0.0', port=5000)