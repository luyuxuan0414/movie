from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() #連接資料庫
        
        
class mi(db.Model): #memberInfo
    __tablename__ = "MemberInfo"
    MemberID = db.Column(db.String, primary_key = True)
    Password = db.Column(db.String, nullable = False)
    Name = db.Column(db.String, nullable = False)
    Birthday = db.Column(db.Integer, nullable = False)
    Phone = db.Column(db.Integer, nullable = False)
    Email = db.Column(db.String, nullable = False)
    
    def __init__(self, MemberID, Password, Name, Birthday, Phone, Email):
        self.MemberID = MemberID
        self.Password = Password
        self.Name = Name
        self.Birthday = Birthday
        self.Phone = Phone
        self.Email = Email
        
class br(db.Model): #bookingrecord
    __tablename__ = "BookingRecord"
    RecordID = db.Column(db.String, primary_key = True)
    MemberID = db.Column(db.String, nullable = False)
    Theater = db.Column(db.String, nullable = False)
    Movie = db.Column(db.Integer, nullable = False)
    Date = db.Column(db.Integer, nullable = False)
    Time = db.Column(db.String, nullable = False)
    Ticket1 = db.Column(db.String)
    Ticket2 = db.Column(db.String)
    Ticket3 = db.Column(db.String)
    Food1 = db.Column(db.String)
    Food2 = db.Column(db.String)
    Food3 = db.Column(db.String)
    Food4 = db.Column(db.String)
    Food5 = db.Column(db.String)
    Food6 = db.Column(db.String)
    Food7 = db.Column(db.String)
    Food8 = db.Column(db.String)
    TotalPrice = db.Column(db.String)
    
    
    def __init__(self, RecordID, MemberID, Theater, Movie, Date, Time, Ticket1, Ticket2, Ticket3, Food1, Food2, Food3, Food4, Food5, Food6, Food7, Food8, TotalPrice):
        self.RecordID = RecordID
        self.MemberID = MemberID
        self.Theater = Theater
        self.Movie = Movie
        self.Date = Date
        self.Time = Time
        self.Ticket1 = Ticket1
        self.Ticket2 = Ticket2
        self.Ticket3 = Ticket3
        self.Food1 = Food1
        self.Food2 = Food2
        self.Food3 = Food3
        self.Food4 = Food4
        self.Food5 = Food5
        self.Food6 = Food6
        self.Food7 = Food7
        self.Food8 = Food8
        self.TotalPrice = TotalPrice
        