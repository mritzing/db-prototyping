from flask import flash, render_template, request, redirect, Flask
from wtforms import Form, StringField, SelectField

class molSearchForm(Form):
    choices = [('notation', 'Smiles String'),
               ('author', 'Author'),
               ('theoretical_mass', 'Molecular Mass')]
    select = SelectField('Search for:', choices=choices)
    search = StringField('')

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    search = molSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('base.html', form=search)

@app.route('/results')
def search_results(search):
    results = []
    search_string = search.data['search']
    if search.data['search'] == '':
        print("s")
        #qry = db_session.query(Album)
        #results = qry.all()
    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run()