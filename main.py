# coding:utf-8
from flask import Flask, render_template, request, url_for

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import pandas as pd

app = Flask(__name__)

engine = create_engine('sqlite:///sqlite.db', echo=False)
Base = declarative_base()
Base.metadata.reflect(engine)

class cvr(Base):
    __table__ = Base.metadata.tables['cvr']


	

@app.route('/', methods = ['GET'])	
def dashboard():
     datestart = request.args.get('datestart', default = '2017-09-01')
     dateend = request.args.get('dateend', default = '2017-09-30')
     device = request.args.get('device', default = 'desktop')
     metric = request.args.get('metric', default = 'cvr')
	 
     Session = sessionmaker(bind=engine)
     session = Session()
     query = session.query(cvr).filter(cvr.date >= datestart).filter(cvr.date <= dateend).filter(cvr.device == device)
     df = pd.read_sql(query.statement, query.session.bind)
     session.close()
	 
     data_plot = {}
     data_plot['x'] = list(df['date'].astype(str))
     data_plot['y'] = list(df[metric])
	 
     return(render_template('dashboard.html', datestart = datestart, dateend = dateend, device = device, data_plot = data_plot, metric = metric))

if __name__ == '__main__':
    app.run(port=5000, debug=True)

