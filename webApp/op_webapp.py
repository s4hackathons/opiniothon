from flask import Flask, render_template, request, redirect, url_for, abort, session
from flaskext.mysql import MySQL
import json
from datetime import date, timedelta, datetime
import time
import datetime

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'opinio'
app.config['MYSQL_DATABASE_PASSWORD'] = "Opinio@123"
app.config['MYSQL_DATABASE_DB'] = 'opinio_db'
app.config['MYSQL_DATABASE_HOST'] = '172.31.99.109'
mysql.init_app(app)


@app.route('/discount', methods=['POST', 'GET'])
def render_discount():
	print "render_discount"
	conn = mysql.get_db()
	cur = conn.cursor()
        
	try:
		print "querying"
		query = "select * from coupon;"
		cur.execute(query)
		data = cur.fetchall()
                data_list = []
		print type(data)
		for row in data:
			json_data = {}
			json_data["CouponCode"] = str(row[0])
			json_data["Description"] = str(row[1])
			#json_data = json.dumps(json_data)
			data_list.append(json_data)
		data_json = {}
		data_json["discountDetails"] = data_list
	except Exception, e:
		return "ERROR" + str(e)
	finally:
		conn.commit()
        response = json.dumps(data_json)
        #response.headers.add('Access-Control-Allow-Origin', '*')
	return response


@app.route('/discountDetails', methods=['POST', 'GET'])
def discountdetails():
	print "render_discount"
        print "Inside discount details"
	conn = mysql.get_db()
	cur = conn.cursor()
        userId=request.args.get('userId');
	try:
		print "querying"
		query = "select * from coupon;"
		cur.execute(query)
		data = cur.fetchall()
                data_list = []
		print type(data)
                w = [1.0,1.0,1.0,1.0,1.0]

		for row in data:
                        x = []
                        print "xx"
                        category = row[3];
                        print "yy " + userId + "zz" + category
                        query = "select * from PASTORDER where ID='"+userId+"' and CATEGORY='"+category+"';"
		        cur.execute(query)
		        data = cur.fetchall()
                        print "tested"
			if cur.rowcount == 0:
                            print "Inside1"
                            x.append(0.0);
                            x.append(0.0);			
			else:
			  for rdata in data:
                            print "final_testing1"
                            x.append(float(rdata[2])/100.0)
                            print "final_testing2", rdata[3]
			    last_time = datetime.datetime.strptime(rdata[3], '%d/%m/%Y').date()
                            print "final_testing4"
			    cur_time = datetime.datetime.now().date()
			    #cur_time = time.strftime("%Y-%m-%d")
                            print last_time, cur_time
			    ndays = abs((cur_time - last_time).days)
                            print "final_testing3"
			    if(ndays >= 60):
				x.append(0.0)
			    else:
				x.append(1.0 - float(ndays)/60.0)
			    
                        print "tested1"
			query = "select * from TIMESPENT where ID='"+userId+"' and CATEGORY='"+category+"';"
		        cur.execute(query)
		        data = cur.fetchall()
                        print "tested2"
			if cur.rowcount == 0:
                            print "Inside1"
                            x.append(0.0);
                            x.append(0.0);
			else:
			  for rdata in data:
                            x.append(float(rdata[2])/100.0)
                            print "tested3"
			    last_time = datetime.datetime.strptime(rdata[3], '%d/%m/%Y').date()
			    cur_time =  datetime.datetime.now().date()
			    #cur_time = time.strftime("%d/%m/%Y")
			    ndays = abs((cur_time - last_time).days)
			    if(ndays >= 60):
				x.append(0.0)
			    else:
				x.append(1.0 - float(ndays)/60.0)
			    
			print "tested4", row[4]
			x.append(float(row[4])/100.0)
                        print "tested5"
			weight_for_offer = 0.0;
			weight_sum = 0.0;
			j = 0
                        print "length", len(x)
			for i in x:
                                print "Inside3" , w[j]
				weight_for_offer = weight_for_offer + i*w[j]
				
                                print "Inside4" , w[j]
				weight_sum = weight_sum + w[j]
                                j = j+1
			print "tested6"
			weight_for_offer = weight_for_offer/weight_sum			 
			json_data = {}
			json_data["CouponCode"] = str(row[0])
			json_data["CouponScore"] = str(weight_for_offer)
			#json_data = json.dumps(json_data)
			data_list.append(json_data)
			print "please dont fail"
		data_json = {}
		data_json["discountDetails"] = data_list
	except Exception, e:
		return "ERROR" + str(e)
	finally:
		conn.commit()
        response = json.dumps(data_json)
	print response
	print "this is it"
        #console.log("Discount details" + response)
	return response
@app.route('/', methods=['POST', 'GET'])
def home_page():
	if request.method == 'GET':
		return render_template('CRMModel.html')




if __name__ == '__main__':
	app.run(debug=True)
