from flask import Flask
from flask import render_template, redirect, url_for
from flask import request
from flask_sqlalchemy import SQLAlchemy
from table import mi, br
#import tkinter as tk

#from tkinter import messagebox
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://luyuxuan:dc0409@127.0.0.1:5432/luyuxuan'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hungshihching:poesypoesy@127.0.0.1:5432/hungshihching'


db = SQLAlchemy()
db.init_app(app)

@app.route('/movie2', methods=['POST', 'GET'])
def movie2():
    movie = request.values['movie']
    return redirect(url_for('movie3', movie=movie))

@app.route('/movie3?movie=<movie>', methods=['POST', 'GET'])
def movie3(movie):
        result = movie
        return render_template('movie.html', result=result)

@app.route('/cmovie2', methods=['POST', 'GET']) #熱映中
def cmovie():
    movie = request.values['movie']
    return redirect(url_for('cmovie3', movie=movie))

@app.route('/cmovie3?movie=<movie>', methods=['POST', 'GET'])
def cmovie2(movie):
        result = movie
        return render_template('cmovie.html', result=result)
    
@app.route('/theater.html') #theater
def theater():
    return render_template('theater.html')

@app.route('/theater2', methods=['POST', 'GET']) 
def theater2():
    theater = request.values['theater']
    return redirect(url_for('theater3', theater=theater))

@app.route('/theater3?theater=<theater>', methods=['POST', 'GET']) 
def theater3(theater):
    result = theater
    return render_template('theaterdetail.html', result=result)

@app.route('/seat') #booking
def seat():
    movie = request.values['mm']
    theater = request.values['theater']
    date = request.values['date']
    time = request.values['time']
    ticket1 = request.values['ticket1']
    ticket2 = request.values['ticket2']
    ticket3 = request.values['ticket3']
    food1 = request.values['food1']
    food2 = request.values['food2']
    food3 = request.values['food3']
    food4 = request.values['food4']
    food5 = request.values['food5']
    food6 = request.values['food6']
    food7 = request.values['food7']
    food8 = request.values['food8']
    brall = br.query.all()
    num = len(brall)+1
    price = 0
    if ticket1 != '選擇數量':
        price += 300*int(ticket1)
    if ticket2 != '選擇數量':
        price += 150*int(ticket2)
    if ticket3 != '選擇數量':
        price += 150*int(ticket3)
    if food1 != '選擇數量':
        price += 60*int(food1)
    if food2 != '選擇數量':
        price += 50*int(food2)
    if food3 != '選擇數量':
        price += 45*int(food3)
    if food4 != '選擇數量':
        price += 120*int(food4)
    if food5 != '選擇數量':
        price += 110*int(food5)
    if food6 != '選擇數量':
        price += 100*(food6)
    if food7 != '選擇數量':
        price += 90*int(food7)
    if food8 != '選擇數量':
        price += 90*int(food8)
        
    r = br(num, 'B0928026', theater, movie, date, time, ticket1, ticket2, ticket3, food1, food2, food3, food4, food5, food6, food7, food8, price)
    db.session.add(r)
    db.session.commit()
    return render_template('seat.html', movie=movie, theater=theater, date=date, time=time, ticket1=ticket1, ticket2=ticket2, ticket3=ticket3, food1=food1, food2=food2, food3=food3, food4=food4, food5=food5, food6=food6, food7=food7, food8=food8)

@app.route('/pay', methods=['POST', 'GET'])
def pay():
    seats = request.form.getlist('seats')
    return render_template('pay.html', result=seats)


@app.route('/onlinepayment.html')
def onlinepayment():
    return render_template('onlinepayment.html')

@app.route('/member.html', methods=['POST', 'GET']) #show member info
def member():
    if request.method == 'POST':
        idinput = request.form.get('memberid')
        pwdinput = request.form.get('password')
        idinput2 = request.form.get('memberid2')
        pwdinput2 = request.form.get('password2')
        pwdinput3 = request.form.get('password3')
        nameinput = request.form.get('name2')
        birinput = request.form.get('birthday2')
        telinput = request.form.get('phone2')
        emailinput = request.form.get('email2')
        miall = mi.query.all()
        result = ['result']
        for i in miall:
            if idinput == i.MemberID and pwdinput == i.Password: #login
                result.append(i.MemberID)
                result.append(i.Password)
                result.append(i.Name)
                result.append(i.Birthday)
                result.append(i.Phone)
                result.append(i.Email)
        if idinput is None and pwdinput2 == pwdinput3: #sign up
            m = mi(idinput2, pwdinput2, nameinput, birinput, telinput, emailinput)
            db.session.add(m)
            db.session.commit()
        return render_template('member.html', result=result)
    return render_template('member.html')

@app.route('/revise')
def revise():
    return render_template('revise.html')

@app.route('/forgetpwd.html')
def forgetpwd():
    return render_template('forgetpwd.html')

@app.route('/record.html', methods=['POST', 'GET'])
def record():
    if request.method == 'POST':
        idinput = request.form.get('memberid')
        pwdinput = request.form.get('password')
        miall = mi.query.all()
        brall = br.query.all()
        for i in miall:
            if idinput == i.MemberID and pwdinput == i.Password:
                memberid = i.MemberID
                for j in brall:
                    if memberid == j.MemberID:
                        recordid = j.RecordID
                        movie = j.Movie
                        theater = j.Theater
                        date = j.Date
                        time = j.Time
                        ticket1 = j.Ticket1
                        ticket2 = j.Ticket2
                        ticket3 = j.Ticket3
                        food1 = j.Food1
                        food2 = j.Food2
                        food3 = j.Food3
                        food4 = j.Food4
                        food5 = j.Food5
                        food6 = j.Food6
                        food7 = j.Food7
                        food8 = j.Food8
                        price = j.TotalPrice
                        return render_template('record.html', recordid=recordid, movie=movie, theater=theater, date=date, time=time, ticket1=ticket1, ticket2=ticket2, ticket3=ticket3, food1=food1, food2=food2, food3=food3, food4=food4, food5=food5, food6=food6, food7=food7, food8=food8, price=price)
    return render_template('record.html')

@app.route('/record2.html')
def record2():
    return render_template('record2.html')

@app.route('/record3')
def record3():
    return render_template('record3.html')

@app.route('/modify.html', methods=['POST', 'GET'])
def modify():
    if request.method == 'POST':
        idinput = request.form.get('memberid')
        pwdinput = request.form.get('password')
        miall = mi.query.all()
        result = ['result']
        for i in miall:
            if idinput == i.MemberID and pwdinput == i.Password:
                result.append(i.MemberID)
                result.append(i.Password)
                result.append(i.Name)
                result.append(i.Birthday)
                result.append(i.Phone)
                result.append(i.Email)
                return render_template('member2.html', result=result)
    return render_template('modify.html')

    
'''@app.route('/save', methods=['POST'])
def save():
    if request.method == 'POST':
        idinput = request.values['memberid']
        pwdinput = request.form.get('password')
        nameinput = request.form.get('name')
        birinput = request.form.get('birthday')
        telinput = request.form.get('phone')
        emailinput = request.form.get('email')
        m = mi.query.filter_by(MemberID=idinput).first()
        m.Password = pwdinput
        m.Name = nameinput
        m.Birthday = birinput
        m.Phone = telinput
        m.Email = emailinput
        db.session.commit()
        result = ['result']
        result.append(idinput)
        result.append(pwdinput)
        result.append(nameinput)
        result.append(birinput)
        result.append(telinput)
        result.append(emailinput)
        return render_template('member.html', result=result)
    return render_template('member.html')'''

@app.route('/') #home page
def index():
    db.create_all()
    return render_template('home.html')
    

if __name__ == '__main__':
    app.run()