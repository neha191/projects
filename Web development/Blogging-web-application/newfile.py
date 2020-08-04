from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author=db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Blog %r>' % self.id

@app.route('/home')
def home_page():
	return render_template('homepage.html')

@app.route('/add-blog', methods=['POST','GET'])
def add_blog():
    if request.method == 'POST':
        blog_author=request.form['author']
        blog_content = request.form['content']
        new_blog = Blog(content=blog_content, author=blog_author )

        try:
            db.session.add(new_blog)
            db.session.commit()
            return redirect('/add-blog')
        except:
            return 'There was an issue adding your task'

    else:
        blogs = Blog.query.order_by(Blog.date_created).all()
        return render_template('add_blog.html', blogs=blogs)

@app.route('/delete/<int:id>')
def delete(id):
	post=Blog.query.get_or_404(id)
	db.session.delete(post)
	db.session.commit()
	return redirect('/add-blog')

@app.route('/update/<int:id>', methods=['POST','GET'])
def update(id):
	blog=Blog.query.get_or_404(id)
	if request.method=='POST':
		blog.author=request.form['author']
		blog.content=request.form['content']
		#db.session.commit() without try 
		#return redirect('/add-blog')
	#else:
		#return render_template('edit.html', blog=blog )
		try:
			db.session.commit()
			return redirect('/add-blog')
		except:
			return 'There was an issue updating your task'

	else:
		return render_template('edit.html', blog=blog)

if __name__ == "__main__":
    app.run(debug=True)