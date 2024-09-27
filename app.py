from flask import Flask,render_template,request
from text_summarizer import summarizer 


app=Flask(__name__)

@app.route('/')
def index():
     return render_template('index.html')

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        rawtext = request.form['rawtext']  # Proper indentation here
        summary, org_text, org_len, sum_len = summarizer(rawtext)
        return render_template('summary.html', 
                               summary=summary, 
                               org_text=org_text, 
                               org_len=org_len, 
                               sum_len=sum_len)

    # Handle the GET request (if no form submission)
    return render_template('index.html')

      



if __name__ == "__main__":
    app.run(debug=True)
