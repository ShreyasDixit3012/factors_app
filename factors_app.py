from flask import Flask, render_template, request, escape
import arith_functions as a_f

from DBcm import UseDatabase

app = Flask(__name__)

app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': 'factorsadmin',
                          'password': 'factorpwd',
                          'database': 'factorsappDB',}



def log_request(req: 'flask_request', res: str) -> None:
    """Log details of the web request and the results"""
    
    with UseDatabase(app.config['dbconfig']) as cursor:
         _SQL = """insert into log
              (number, ip, browser_string, results)
              values
              (%s, %s, %s, %s)"""
         cursor.execute(_SQL, (req.form['number'],
                          req.remote_addr,
                          req.user_agent.browser,
                          res,))
    
    
    
@app.route('/factors', methods=['POST'])
def calcfactors() -> 'html':
    number = request.form['number']
    results = str(a_f.factors(int(number)))
    log_request(request, results)
    title = 'Here is your result:'
    return render_template('results.html',
                           the_results=results,
                           the_number=number,
                           the_title=title,)
    
@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_title='Welcome to FindingFactors!')

@app.route('/viewlog')
def view_the_log() -> 'html':
    """Display the contents of the log file as HTML table"""
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """select number, ip, browser_string, results from log"""
        cursor.execute(_SQL)
        contents = cursor.fetchall()
    titles = ('Number', 'Remote_addr', 'User_agent', 'Results')
    return render_template('viewlog.html',
                           the_title='View Log',
                           the_row_titles=titles,
                           the_data=contents,
                           )

if __name__ == '__main__':
    app.run(debug=True)

