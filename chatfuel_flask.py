from flask import Flask, request
import sqlite3
import json

class college_details:
    def __init__ (self, college_name=None,  college_website=None):
        self.college_name=college_name
        self.link=college_website
        self.rank=0
        self.pu_uni=None
        self.stream=None
        self.area=None
    def get_data(self):
        print(f'{self.college_name} {self.college_website} {self.rank}')

c=college_details()

app= Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def receive_message():
    if request.method=='POST':
        output = request.get_json()
        print(output)
        #send_data(output)
        c.college_name, c.rank,c.link= send_data(output)
        print("college:",c.college_name)
        return""

    elif request.method =='GET':
        json_body={
  "set_attributes":
    {
      "rank": c.rank,
      "college": c.college_name,
      "link":c.link
    }

}
        return json.dumps(json_body)

def send_data(output):
    c.area= output["Area"]
    print("area:",c.area)
    c.rank= output["rank"]
    c.pu_uni=output["PU/Uni"]
    c.stream=output["stream"]
    conn = sqlite3.connect('college_db.sqlite3')
    cur= conn.cursor()
    if c.pu_uni=="Pre-University":
        stream="College_PU."+(str(c.stream)).lower()
        print("stream:",stream)
        cur.execute('''Select College_PU.college, College_PU.rank, College_PU.link from College_PU join Area on College_PU.area_id=area.id where College_PU.rank> ? and area.name= ? and %s=1 order by College_PU.rank'''% (stream), (c.rank,c.area) )
        row = cur.fetchone()
        cur.close()
        print(row)
    elif c.pu_uni=="University":
        cur.execute('''Select College_Uni.college, College_Uni.rank, College_Uni.link from College_Uni join Area join Stream_Uni on College_Uni.area_id=area.id and College_Uni.stream_uni_id=Stream_uni.id where College_Uni.rank> ? and Area.name= ? and Stream_uni.stream= ? order by College_Uni.rank''',(c.rank, c.area,c.stream))
        row = cur.fetchone()
        print(row)
        cur.close()
    return row



if __name__ == '__main__':
    app.debug=True
    app.run()
    app.run(debug)