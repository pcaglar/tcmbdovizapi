# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from KekikFlask import app
from flask import Flask,make_response,request,render_template, jsonify, url_for,redirect
from KekikFlask._endpointler.doviz import DovizKur
from wtforms import Form,StringField,TextAreaField,validators

kurlarapi = DovizKur()


class MiktarForm(Form):
    miktar = StringField("Döviz Miktarı",validators=[validators.NumberRange(min=0, max=99999999)])



@app.route('/',methods = ["GET","POST"])
def ana_sayfa():
    Doviz_Value = kurlarapi.DegerSor()
    form = MiktarForm(request.form)
    
    
    if request.method == "POST":
        dovizmiktar = request.form.get("dovizmiktari")
        dovizturu = request.form.get("doviztur")
        alsatturu = request.form.get("alsattur")
        #topla = int(keyword)+5 
        print("123213111111")
        
        print(dovizturu)
        Doviz_Hesabi = kurlarapi.hesapla(dovizturu,alsatturu,dovizmiktar)
        
        #miktar = form.miktar.data
        #miktar = request.form.get('miktar')
        return render_template("ana_sayfa.html",toplam=Doviz_Hesabi, Doviz_Value = Doviz_Value,dovizturu=dovizturu)
        #return redirect(url_for("ana_sayfa"))
          
    else:
        return render_template(
            'ana_sayfa.html',
            baslik = "Döviz Apisi!",
            Doviz_Value = kurlarapi.DegerSor(),
            #keyword=keyword
            #Doviz_Value = kurlarapi.DegerSor().get("USD")
            
    
        ) 

#api çağrısı
@app.route('/api/doviz', methods=['GET', 'POST'])
def api_doviz():
    if request.method == "GET":
        return make_response(jsonify(kurlarapi.DegerSor()), 200)
    elif request.method == 'POST':
        content = request.json
        tarih= content['tarih']
        if "tur" in content:
          tur= content['tur']
          return make_response(jsonify(kurlarapi.Arsiv_tarih(tarih).get(tur.upper())), 201)  # 201 = ARSIV
        else:
          return make_response(jsonify(kurlarapi.Arsiv_tarih(tarih)), 201)  # 201 = ARSIV


#seçili dövize api çağrısı
@app.route('/api/doviz/<tur>', methods=['GET', 'POST'])
def api_her_doviz(tur):
    if request.method == "GET":
        Doviz_Value = kurlarapi.DegerSor().get(tur.upper())
        if Doviz_Value:
            return make_response(jsonify(Doviz_Value), 200)
        else:
            return make_response(jsonify(Doviz_Value), 404)
    elif request.method == "POST":  # Arsiv
        content = request.get_json(force=True)
        print(content)
        tarih= content["tarih"]
        Doviz_Value = kurlarapi.Arsiv_tarih(tarih).get(tur.upper())
        if Doviz_Value:
            return make_response(jsonify(Doviz_Value), 201)
        else:
            return make_response(jsonify(Doviz_Value), 404)

#tarihli api çağrısı
@app.route('/api/doviz/<yil>/<ay>/<gun>', methods=['GET'])
def gun_ay_yil_api(yil,ay,gun):
    if request.method == "GET":
        Doviz_Value = kurlarapi.Arsiv(gun,ay,yil)
        if Doviz_Value:
            return make_response(jsonify(Doviz_Value), 200)
        else:
            return make_response(jsonify(Doviz_Value), 404)

#seçili dövize tarihli api çağrısı
@app.route('/api/doviz/<yil>/<ay>/<gun>/<tur>', methods=['GET'])
def gun_ay_yil_tur_api(yil,ay,gun,tur):
    if request.method == "GET":
        Doviz_Value = kurlarapi.Arsiv(gun,ay,yil).get(tur.upper())
        if Doviz_Value:
            return make_response(jsonify(Doviz_Value), 200)
        else:
            return make_response(jsonify(Doviz_Value), 404)

#seçili dövize ve alış-satışa göre hesap yapan api
@app.route('/api/doviz/hesap/<tur>/<secenek>/<miktar>', methods=['GET'])
def hesap_yap(secenek,miktar,tur):
    if request.method == "GET":
        tur=tur.upper()
        Doviz_Hesabi = kurlarapi.hesapla(tur,secenek,miktar)
        if Doviz_Hesabi:
            return Doviz_Hesabi
        #else:
            #return make_response(jsonify(Doviz_Hesabi), 404)