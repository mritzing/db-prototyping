from flask import flash, render_template, request, redirect, Flask, url_for, session
from wtforms.fields import SelectField,StringField, TextAreaField, SubmitField  
from wtforms.validators import InputRequired
from wtforms import ValidationError, Form
from util import Parser
import sys
class molSearchForm(Form):
    choices = [('notation', 'Smiles String'),
               ('author', 'Author'),
               ('theoretical_mass', 'Molecular Mass')]
    select = SelectField('Search for:', choices=choices)
    search = StringField('')

class additionalInfoForm(Form):
    notation = StringField('Smiles String', validators = [InputRequired()])
    author = StringField('Author', validators=[InputRequired()])
    lab = StringField('Lab', validators=[InputRequired()])
    submit = SubmitField('Finish Upload', validators = [InputRequired()])
    #not required info
    sci_mass = StringField('Scientific Mass') #show calculated 
    forceFieldOptions = [('what','what'), ('are','are'),( 'these', 'these')]
    forceFieldSelect = SelectField('Force field', choices=forceFieldOptions)
    solution = StringField("Smiles")
    publications = TextAreaField('List related publications')
    #additionalInteractions = Stringfield('find ligands in db')
    #related files (search db again)

app = Flask(__name__)
app.secret_key = 'ewafwefaejf'




@app.route('/', methods=['GET', 'POST'])
def index():
    search = molSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('index.html', form = search)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    file = request.files['inputFile'] 
    addForm = additionalInfoForm(request.form)
    p = Parser()
    item = p.parseFile(file.read(), file)
    return (render_template('uploadForm.html', form = addForm, fileName = file, smilesStr= item[0], massStr = item[1], filename = getattr(file, 'filename', None)))

@app.route('/test1')
def test1():
    addForm = additionalInfoForm(request.form)
    return (render_template('uploadForm.html', form = addForm))

@app.route('/results')
def search_results(search):
    print("hit search")
    results = []
    search_string = search.data['search']
    if search.data['search'] == '':
        p = Parser()
        results = p.returnAllRes()
        print(results)
        return redirect('/')
    if not results:
        print("not found")
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        p = Parser()
        results = p.returnAllRes()
        print(results)
        return redirect('/')

if __name__ == '__main__':
    app.debug = True
    app.run()