from flask import Flask, render_template, request, send_file, session, redirect, url_for, make_response
from fpdf import FPDF
from flask_session import Session  # セッション管理用
import os
import logging
from math import ceil
from werkzeug.utils import secure_filename
from PIL import Image
import fitz  # PyMuPDF
import json


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['UPLOAD_FOLDER'] = 'uploads'
Session(app)


logging.basicConfig(filename='error.log', level=logging.DEBUG)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['jpg', 'jpeg', 'png', 'pdf']


@app.route('/')
def home():
    session.clear()  # 新しいセッションを開始
    return render_template('home.html')  # 'home.html'をレンダリング


@app.route('/step1', methods=['GET', 'POST'])
def step1():
    if request.method == 'POST':
        session['corporation_name'] = request.form['corporation_name']
        session['office_name'] = request.form['office_name']
        session['representative_name'] = request.form['representative_name']
        session['manager_name'] = request.form['manager_name']
        session['phone_number'] = request.form['phone_number']
        session['creation_date'] = request.form['creation_date']
        session['revision_date'] = request.form['revision_date']
        session['location'] = request.form['location']
        session['environment'] = request.form['environment']
        session['facility_type'] = request.form['facility_type']
        session['residents_number'] = request.form['residents_number']
        session['residents_status'] = request.form['residents_status']
        session['staff_number'] = request.form['staff_number']
        session['site_area'] = request.form['site_area']
        session['floor_area'] = request.form['floor_area']
        session['floors'] = request.form['floors']
        session['rooms'] = request.form['rooms']
        session['philosophy'] = request.form['philosophy']
        session['purpose_1'] = request.form['purpose_1']
        session['purpose_2'] = request.form['purpose_2']
        session['purpose_3'] = request.form['purpose_3']
        session['roles'] = request.form.getlist('roles[]')
        session['departments'] = request.form.getlist('departments[]')
        session['names'] = request.form.getlist('names[]')
        session['notes'] = request.form.getlist('notes[]')
        # 組織図の取得
        if 'org_chart' in request.files:
            file = request.files['org_chart']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                session['org_chart'] = filepath  # ファイルのパスをセッションに保存
        # 地震関連ファイルの保存
        earthquake_files = request.files.getlist('earthquake_files[]')
        earthquake_filepaths = []
        for file in earthquake_files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                earthquake_filepaths.append(filepath)
        session['earthquake_files'] = earthquake_filepaths
        # 水害関連ファイルの保存
        flood_files = request.files.getlist('flood_files[]')
        flood_filepaths = []
        for file in flood_files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                flood_filepaths.append(filepath)
        session['flood_files'] = flood_filepaths
        session['priority_business'] = request.form.getlist('priority_business[]')
        session['priority_tasks'] = request.form.getlist('priority_tasks[]')
        session['priority_items'] = request.form.getlist('priority_items[]')
        return redirect(url_for('step2'))
    return render_template('step1.html') 


@app.route('/step2', methods=['GET', 'POST'])
def step2():
    if request.method == 'POST':
        session['current_status_seismic'] = request.form['current_status_seismic']
        session['current_status_flood_measures'] = request.form['current_status_flood_measures']


        target_building = request.form.getlist('target_building[]')
        measure_building = []
        current_status_building = {}


        for target in target_building:
            measures = request.form.getlist(f'measure_target_{target}[]')
            measure_building.extend(measures)
            for measure in measures:
                current_status_building[measure] = request.form.get(f'current_status_{measure}', '不明')


        session['target_building'] = target_building
        session['measure_building'] = measure_building
        session['current_status_building'] = current_status_building


        target_furniture = request.form.getlist('target_furniture[]')
        measure_furniture = []
        current_status_furniture = {}


        for target in target_furniture:
            measures = request.form.getlist(f'measure_target_{target}[]')
            measure_furniture.extend(measures)
            for measure in measures:
                current_status_furniture[measure] = request.form.get(f'current_status_{measure}', '不明')


        session['target_furniture'] = target_furniture
        session['measure_furniture'] = measure_furniture
        session['current_status_furniture'] = current_status_furniture


        target_external = request.form.getlist('target_external[]')
        measure_external = []
        current_status_external = {}


        for target in target_external:
            measures = request.form.getlist(f'measure_target_{target}[]')
            measure_external.extend(measures)
            for measure in measures:
                current_status_external[measure] = request.form.get(f'current_status_{measure}', '不明')


        session['target_external'] = target_external
        session['measure_external'] = measure_external
        session['current_status_external'] = current_status_external


        target_flood = request.form.getlist('target_flood[]')
        measure_flood = []
        current_status_flood = {}


        for target in target_flood:
            measures = request.form.getlist(f'measure_target_{target}[]')
            measure_flood.extend(measures)
            for measure in measures:
                current_status_flood[measure] = request.form.get(f'current_status_{measure}', '不明')


        session['target_flood'] = target_flood
        session['measure_flood'] = measure_flood
        session['current_status_flood'] = current_status_flood


        target_electricity = request.form.getlist('target_electricity[]')
        measure_electricity = []
        current_status_electricity = {}


        for target in target_electricity:
            measures = request.form.getlist(f'measure_target_{target}[]')
            measure_electricity.extend(measures)
            for measure in measures:
                current_status_electricity[measure] = request.form.get(f'current_status_{measure}', '不明')


        session['target_electricity'] = target_electricity
        session['measure_electricity'] = measure_electricity
        session['current_status_electricity'] = current_status_electricity


        # ガス
        target_gas = request.form.getlist('target_gas[]')
        measure_gas = []
        current_status_gas = {}
        for target in target_gas:
            measures = request.form.getlist(f'measure_target_{target}[]')
            measure_gas.extend(measures)
            for measure in measures:
                current_status_gas[measure] = request.form.get(f'current_status_{measure}', '不明')
        session['target_gas'] = target_gas
        session['measure_gas'] = measure_gas
        session['current_status_gas'] = current_status_gas


        # 飲料水
        target_drinking_water = request.form.getlist('target_drinking_water[]')
        measure_drinking_water = []
        current_status_drinking_water = {}
        for target in target_drinking_water:
            measures = request.form.getlist(f'measure_target_{target}[]')
            measure_drinking_water.extend(measures)
            for measure in measures:
                current_status_drinking_water[measure] = request.form.get(f'current_status_{measure}', '不明')
        session['target_drinking_water'] = target_drinking_water
        session['measure_drinking_water'] = measure_drinking_water
        session['current_status_drinking_water'] = current_status_drinking_water


        # 生活用水
        target_life_water_new = request.form.getlist('target_life_water_new[]')
        measure_life_water_new = []
        current_status_life_water_new = {}
        for target in target_life_water_new:
            measures = request.form.getlist(f'measure_target_{target}[]')
            measure_life_water_new.extend(measures)
            for measure in measures:
                current_status_life_water_new[measure] = request.form.get(f'current_status_{measure}', '不明')
        session['target_life_water_new'] = target_life_water_new
        session['measure_life_water_new'] = measure_life_water_new
        session['current_status_life_water_new'] = current_status_life_water_new


        # 通信
        target_communication = request.form.getlist('target_communication[]')
        measure_communication = []
        current_status_communication = {}
        for target in target_communication:
            measures = request.form.getlist(f'measure_target_{target}[]')
            measure_communication.extend(measures)
            for measure in measures:
                current_status_communication[measure] = request.form.get(f'current_status_{measure}', '不明')
        session['target_communication'] = target_communication
        session['measure_communication'] = measure_communication
        session['current_status_communication'] = current_status_communication


        # 情報システム
        target_info_system = request.form.getlist('target_info_system[]')
        measure_info_system = []
        current_status_info_system = {}
        for target in target_info_system:
            measures = request.form.getlist(f'measure_target_{target}[]')
            measure_info_system.extend(measures)
            for measure in measures:
                current_status_info_system[measure] = request.form.get(f'current_status_{measure}', '不明')
        session['target_info_system'] = target_info_system
        session['measure_info_system'] = measure_info_system
        session['current_status_info_system'] = current_status_info_system


        # 衛生面
        target_hygiene = request.form.getlist('target_hygiene[]')
        measure_hygiene = []
        current_status_hygiene = {}
        for target in target_hygiene:
            measures = request.form.getlist(f'measure_target_{target}[]')
            measure_hygiene.extend(measures)
            for measure in measures:
                current_status_hygiene[measure] = request.form.get(f'current_status_{measure}', '不明')
        session['target_hygiene'] = target_hygiene
        session['measure_hygiene'] = measure_hygiene
        session['current_status_hygiene'] = current_status_hygiene


        target_infrastructure = request.form.getlist('target_infrastructure[]')
        measure_infrastructure = []
        current_status_infrastructure = {}


        for target in target_infrastructure:
            measures = request.form.getlist(f'measure_target_{target}[]')
            measure_infrastructure.extend(measures)
            for measure in measures:
                current_status_infrastructure[measure] = request.form.get(f'current_status_{measure}', '不明')


        session['target_infrastructure'] = target_infrastructure
        session['measure_infrastructure'] = measure_infrastructure
        session['current_status_infrastructure'] = current_status_infrastructure


        target_emergency = request.form.getlist('target_emergency[]')
        measure_emergency = []
        current_status_emergency = {}


        for target in target_emergency:
            measures = request.form.getlist(f'measure_target_{target}[]')
            measure_emergency.extend(measures)
            for measure in measures:
                current_status_emergency[measure] = request.form.get(f'current_status_{measure}', '不明')


        session['target_emergency'] = target_emergency
        session['measure_emergency'] = measure_emergency
        session['current_status_emergency'] = current_status_emergency


        target_food = request.form.getlist('target_food[]')
        measure_food = []
        current_status_food = {}


        for target in target_food:
            measures = request.form.getlist(f'measure_target_{target}[]')
            measure_food.extend(measures)
            for measure in measures:
                current_status_food[measure] = request.form.get(f'current_status_{measure}', '不明')


        session['target_food'] = target_food
        session['measure_food'] = measure_food
        session['current_status_food'] = current_status_food


        target_medical = request.form.getlist('target_medical[]')
        current_status_medical = {}


        for target in target_medical:
            current_status_medical[target] = request.form.get(f'current_status_{target}', '不明')


        session['target_medical'] = target_medical
        session['current_status_medical'] = current_status_medical
    
        target_headquarters = request.form.getlist('target_headquarters[]')
        current_status_headquarters = {}


        for target in target_headquarters:
            current_status_headquarters[target] = request.form.get(f'current_status_{target}', '不明')


        session['target_headquarters'] = target_headquarters
        session['current_status_headquarters'] = current_status_headquarters


        target_prevention = request.form.getlist('target_prevention[]')
        current_status_prevention = {}


        for target in target_prevention:
            current_status_prevention[target] = request.form.get(f'current_status_{target}', '不明')


        session['target_prevention'] = target_prevention
        session['current_status_prevention'] = current_status_prevention


        target_vehicle = request.form.getlist('target_vehicle[]')
        current_status_vehicle = {}


        for target in target_vehicle:
            current_status_vehicle[target] = request.form.get(f'current_status_{target}', '不明')


        session['target_vehicle'] = target_vehicle
        session['current_status_vehicle'] = current_status_vehicle
        
        session['funding_measures'] = request.form['funding_measures']


        # 他施設・地域との連携の内容をセッションに保存
        session['partner_names'] = request.form.getlist('partner_names[]')
        session['partner_addresses'] = request.form.getlist('partner_addresses[]')
        session['partner_phones'] = request.form.getlist('partner_phones[]')
        session['partner_persons'] = request.form.getlist('partner_persons[]')
        session['partner_contents'] = request.form.getlist('partner_contents[]')


        # 同一法人内の他施設との連携の内容をセッションに保存
        session['internal_partner_names'] = request.form.getlist('internal_partner_names[]')
        session['internal_partner_addresses'] = request.form.getlist('internal_partner_addresses[]')
        session['internal_partner_phones'] = request.form.getlist('internal_partner_phones[]')
        session['internal_partner_persons'] = request.form.getlist('internal_partner_persons[]')
        session['internal_partner_contents'] = request.form.getlist('internal_partner_contents[]')


        # 協力医療機関リストの内容をセッションに保存
        session['medical_partner_names'] = request.form.getlist('medical_partner_names[]')
        session['medical_partner_addresses'] = request.form.getlist('medical_partner_addresses[]')
        session['medical_partner_phones'] = request.form.getlist('medical_partner_phones[]')
        session['medical_partner_persons'] = request.form.getlist('medical_partner_persons[]')
        session['medical_partner_contents'] = request.form.getlist('medical_partner_contents[]')


        # 協力医療機関以外の関係協力機関の内容をセッションに保存
        session['external_partner_names'] = request.form.getlist('external_partner_names[]')
        session['external_partner_addresses'] = request.form.getlist('external_partner_addresses[]')
        session['external_partner_phones'] = request.form.getlist('external_partner_phones[]')
        session['external_partner_persons'] = request.form.getlist('external_partner_persons[]')
        session['external_partner_contents'] = request.form.getlist('external_partner_contents[]')


        # 区市町村担当部署、地域包括支援センター、福祉避難所、管轄消防、自治会、建築指導、保健所等の内容をセッションに保存
        session['community_partner_names'] = request.form.getlist('community_partner_names[]')
        session['community_partner_addresses'] = request.form.getlist('community_partner_addresses[]')
        session['community_partner_phones'] = request.form.getlist('community_partner_phones[]')
        session['community_partner_persons'] = request.form.getlist('community_partner_persons[]')
        session['community_partner_contents'] = request.form.getlist('community_partner_contents[]')


        # BCP研修・訓練の実施
        session['bcp_training'] = request.form.getlist('bcp_training[]')


        # BCPの検証・見直し
        session['bcp_review'] = request.form.getlist('bcp_review[]')
        session['report_months'] = request.form.getlist('report_months[]')


        return redirect(url_for('step3'))
    return render_template('step2.html')


@app.route('/step3', methods=['GET', 'POST'])
def step3():
    if request.method == 'POST':
        items = request.form.getlist('items[]')
        quantities = request.form.getlist('quantities[]')
        stocks = request.form.getlist('stocks[]')
        units = request.form.getlist('units[]')
        locations = request.form.getlist('locations[]')
        persons = request.form.getlist('persons[]')
        suppliers = request.form.getlist('suppliers[]')
        dates = request.form.getlist('dates[]')
        notes = request.form.getlist('notes[]')


        inventory = []
        for item, quantity, stock, unit, location, person, supplier, date, note in zip(items, quantities, stocks, units, locations, persons, suppliers, dates, notes):
            inventory.append({
                'item': item,
                'quantity': quantity,
                'stock': stock,
                'unit': unit,
                'location': location,
                'person': person,
                'supplier': supplier,
                'date': date,
                'note': note
            })


        session['inventory'] = inventory
        return redirect(url_for('step4'))
    return render_template('step3.html')




@app.route('/step4', methods=['GET', 'POST'])
def step4():
    if request.method == 'POST':
        # BCP発動基準のデータを保存
        session['bcp_criteria'] = request.form.getlist('bcp_criteria[]')
        session['earthquake_city'] = request.form.get('earthquake_city', '')
        session['earthquake_intensity'] = request.form.get('earthquake_intensity', '')
        session['tsunami_warning'] = request.form.get('tsunami_warning', '')
        session['flood_warning'] = request.form.get('flood_warning', '')
        # 参集基準
        session['day_staff'] = request.form.getlist('day_staff[]')
        session['night_staff'] = request.form.getlist('night_staff[]')
        session['other_day_staff'] = request.form.get('other_day_staff', '')
        session['other_night_staff'] = request.form.get('other_night_staff', '')
        # 拠点
        session['earthquake_first_base'] = request.form['earthquake_first_base']
        session['earthquake_second_base'] = request.form['earthquake_second_base']
        session['flood_first_base'] = request.form['flood_first_base']
        session['flood_second_base'] = request.form['flood_second_base']
        # 新しい職員の安否確認・参集基準の設定
        session['report_methods'] = request.form.getlist('report_methods[]')
        session['other_report_method'] = request.form.get('other_report_method')
        session['report_content'] = request.form.getlist('report_content[]')


        # 対応体制
        session['response_positions'] = request.form.getlist('positions[]')
        session['response_names'] = request.form.getlist('names[]')
        # 施設内の避難場所
        session['internal_evacuation_site_1'] = request.form.get('internal_evacuation_site_1')
        session['internal_evacuation_site_2'] = request.form.get('internal_evacuation_site_2')
        # 施設外の避難場所
        session['external_evacuation_site_1'] = request.form.get('external_evacuation_site_1')
        session['external_evacuation_site_2'] = request.form.get('external_evacuation_site_2')


        business_criteria = {
            'night': request.form.get('business_criteria_night'),
            '6h': request.form.get('business_criteria_6h'),
            '1d': request.form.get('business_criteria_1d'),
            '3d': request.form.get('business_criteria_3d'),
            '7d': request.form.get('business_criteria_7d')
        }
        session['business_criteria'] = business_criteria


        meal_service = {
            'night': request.form.get('meal_service_night'),
            '6h': request.form.get('meal_service_6h'),
            '1d': request.form.get('meal_service_1d'),
            '3d': request.form.get('meal_service_3d'),
            '7d': request.form.get('meal_service_7d')
        }
        session['meal_service'] = meal_service


        meal_assistance = {
            'night': request.form.get('meal_assistance_night'),
            '6h': request.form.get('meal_assistance_6h'),
            '1d': request.form.get('meal_assistance_1d'),
            '3d': request.form.get('meal_assistance_3d'),
            '7d': request.form.get('meal_assistance_7d')
        }
        session['meal_assistance'] = meal_assistance


        oral_care = {
            'night': request.form.get('oral_care_night'),
            '6h': request.form.get('oral_care_6h'),
            '1d': request.form.get('oral_care_1d'),
            '3d': request.form.get('oral_care_3d'),
            '7d': request.form.get('oral_care_7d')
        }
        session['oral_care'] = oral_care


        hydration = {
            'night': request.form.get('hydration_night'),
            '6h': request.form.get('hydration_6h'),
            '1d': request.form.get('hydration_1d'),
            '3d': request.form.get('hydration_3d'),
            '7d': request.form.get('hydration_7d')
        }
        session['hydration'] = hydration


        bathing_assistance = {
            'night': request.form.get('bathing_assistance_night'),
            '6h': request.form.get('bathing_assistance_6h'),
            '1d': request.form.get('bathing_assistance_1d'),
            '3d': request.form.get('bathing_assistance_3d'),
            '7d': request.form.get('bathing_assistance_7d')
        }
        session['bathing_assistance'] = bathing_assistance






        # 職員の休憩宿泊
        session['rest_location_priority1'] = request.form.get('rest_location_priority1', '')
        session['rest_location_priority2'] = request.form.get('rest_location_priority2', '')
        session['rest_location_external'] = request.form.get('rest_location_external', '')
        session['accommodation_priority1'] = request.form.get('accommodation_priority1', '')
        session['accommodation_priority2'] = request.form.get('accommodation_priority2', '')
        session['accommodation_external'] = request.form.get('accommodation_external', '')


        session['target_recovery_res'] = request.form.getlist('target_recovery_res[]')
        measure_recovery_res = []
        current_status_recovery_res = {}


        for target in session['target_recovery_res']:
            measures = request.form.getlist(f'measure_target_{target}[]')
            measure_recovery_res.extend(measures)
            for measure in measures:
                current_status_recovery_res[measure] = request.form.get(f'current_status_{measure}', '不明')


        session['measure_recovery_res'] = measure_recovery_res
        session['current_status_recovery_res'] = current_status_recovery_res


        # measure_options をセッションに保存
        measure_options = json.loads(request.form['measure_options'])
        session['measure_options'] = measure_options


        session['public_content'] = request.form.getlist('public_content[]')
        session['public_range'] = request.form.getlist('public_range[]')
        session['public_method'] = request.form.getlist('public_method[]')


        # 地域との連携 被災時の職員の派遣の選択内容を保存
        session['local_cooperation_dispatch'] = request.form.getlist('local_cooperation_dispatch[]')
        # 地域との連携 福祉避難所の運営 福祉避難所の指定の選択内容を保存
        session['welfare_shelter'] = request.form.get('welfare_shelter')
        # 地域との連携 福祉避難所の運営 福祉避難所の事前準備の選択内容を保存
        session['welfare_shelter_preparation'] = request.form.getlist('welfare_shelter_preparation[]')


        # PDF生成のルートへリダイレクト
        return redirect(url_for('generate_pdf'))
    return render_template('step4.html')


@app.route('/generate_pdf', methods=['GET', 'POST'])
def generate_pdf():
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('IPAexGothic', '', 'ipaexg.ttf', uni=True)


        def add_table_header(pdf, title):
            pdf.cell(0, 10, title, 0, 1, 'L')
            pdf.set_fill_color(200, 200, 200)
            pdf.cell(30, 10, '項目', 1, 0, 'C', 1)
            pdf.cell(15, 10, '必要量', 1, 0, 'C', 1)
            pdf.cell(15, 10, '現備蓄量', 1, 0, 'C', 1)
            pdf.cell(10, 10, '単位', 1, 0, 'C', 1)
            pdf.cell(25, 10, '保管場所', 1, 0, 'C', 1)
            pdf.cell(20, 10, '担当者', 1, 0, 'C', 1)
            pdf.cell(20, 10, '調達先', 1, 0, 'C', 1)
            pdf.cell(25, 10, '日付', 1, 0, 'C', 1)
            pdf.cell(30, 10, '備考', 1, 1, 'C', 1)


        def add_table_data(pdf, inventory):
            add_table_header(pdf, '備蓄品管理')
            for item in inventory:
                pdf.cell(30, 10, item['item'], 1)
                pdf.cell(15, 10, item['quantity'], 1)
                pdf.cell(15, 10, item['stock'], 1)
                pdf.cell(10, 10, item['unit'], 1)
                pdf.cell(25, 10, item['location'], 1)
                pdf.cell(20, 10, item['person'], 1)
                pdf.cell(20, 10, item['supplier'], 1)
                pdf.cell(25, 10, item['date'], 1)
                pdf.cell(30, 10, item['note'], 1, 1)


        # 題名を追加
        pdf.set_font('IPAexGothic', '', 24)  # フォントサイズを大きく設定
        pdf.ln(50) 
        pdf.cell(0, 20, '業務継続計画（BCP)', ln=True, align='C')
        pdf.cell(0, 20, '自然災害編', ln=True, align='C') 
        pdf.ln(50) 


        # セッションからデータを取得してPDFに追加
        corporation_name = session.get('corporation_name', '不明')
        office_name = session.get('office_name', '不明')
        representative_name = session.get('representative_name', '不明')
        manager_name = session.get('manager_name', '不明')
        phone_number = session.get('phone_number', '不明')
        creation_date = session.get('creation_date', '不明')
        revision_date = session.get('revision_date', '不明')
        location = session.get('location', '不明')
        environment = session.get('environment', '不明')
        facility_type = session.get('facility_type', '不明')
        residents_number = session.get('residents_number', '不明')
        residents_status = session.get('residents_status', '不明')
        staff_number = session.get('staff_number', '不明')
        site_area = session.get('site_area', '不明')
        floor_area = session.get('floor_area', '不明')
        floors = session.get('floors', '不明')
        rooms = session.get('rooms', '不明')
        philosophy = session.get('philosophy', '不明')
        purpose_1 = session.get('purpose_1', '不明')
        purpose_2 = session.get('purpose_2', '不明')
        purpose_3 = session.get('purpose_3', '不明')
        org_chart_path = session.get('org_chart', '不明')
        priority_business = session.get('priority_business', [])
        priority_tasks = session.get('priority_tasks', [])
        priority_items = session.get('priority_items', [])
        target_building = session.get('target_building', [])
        measure_building = session.get('measure_building', [])
        current_status_building = session.get('current_status_building', {})
        target_furniture = session.get('target_furniture', [])
        measure_furniture = session.get('measure_furniture', [])
        current_status_furniture = session.get('current_status_furniture', {})
        target_external = session.get('target_external', [])
        measure_external = session.get('measure_external', [])
        current_status_external = session.get('current_status_external', {})
        target_flood = session.get('target_flood', [])
        measure_flood = session.get('measure_flood', [])
        current_status_flood = session.get('current_status_flood', {})
        target_infrastructure = session.get('target_infrastructure', [])
        measure_infrastructure = session.get('measure_infrastructure', [])
        current_status_infrastructure = session.get('current_status_infrastructure', {})
        target_emergency = session.get('target_emergency', [])
        measure_emergency = session.get('measure_emergency', [])
        current_status_emergency = session.get('current_status_emergency', {})
        target_food = session.get('target_food', [])
        measure_food = session.get('measure_food', [])
        current_status_food = session.get('current_status_food', {})
        target_medical = session.get('target_medical', [])
        current_status_medical = session.get('current_status_medical', {})
        target_headquarters = session.get('target_headquarters', [])
        current_status_headquarters = session.get('current_status_headquarters', {})
        target_prevention = session.get('target_prevention', [])
        current_status_prevention = session.get('current_status_prevention', {})
        target_vehicle = session.get('target_vehicle', [])
        current_status_vehicle = session.get('current_status_vehicle', {})
        funding_measures = session.get('funding_measures', '不明')
        current_status_electricity = session.get('current_status_electricity', {})
        measure_electricity = session.get('measure_electricity', [])
        current_status_gas = session.get('current_status_gas', {})
        measure_gas = session.get('measure_gas', [])
        current_status_drinking_water = session.get('current_status_drinking_water', {})
        measure_drinking_water = session.get('measure_drinking_water', [])
        current_status_life_water_new = session.get('current_status_life_water_new', {})
        measure_life_water_new = session.get('measure_life_water_new', [])
        current_status_communication = session.get('current_status_communication', {})
        measure_communication = session.get('measure_communication', [])
        current_status_info_system = session.get('current_status_info_system', {})
        measure_info_system = session.get('measure_info_system', [])
        current_status_hygiene = session.get('current_status_hygiene', {})
        measure_hygiene = session.get('measure_hygiene', [])


        pdf.set_font('IPAexGothic', '', 12)
        pdf.cell(40, 10, '法人名', 1)
        pdf.cell(150, 10, corporation_name, 1, 1)
        pdf.cell(40, 10, '施設・事務所名', 1)
        pdf.cell(150, 10, office_name, 1, 1)
        pdf.cell(40, 10, '代表者名', 1)
        pdf.cell(150, 10, representative_name, 1, 1)
        pdf.cell(40, 10, '管理者名', 1)
        pdf.cell(150, 10, manager_name, 1, 1)
        pdf.cell(40, 10, '電話番号', 1)
        pdf.cell(150, 10, phone_number, 1, 1)
        pdf.cell(40, 10, '作成日', 1)
        pdf.cell(150, 10, creation_date, 1, 1)
        pdf.cell(40, 10, '改訂日', 1)
        pdf.cell(150, 10, revision_date, 1, 1)
        pdf.ln(100)


        pdf.set_font('IPAexGothic', '', 16)
        pdf.cell(0, 10, '総論', 0, 1, 'L') 
        pdf.set_font('IPAexGothic', '', 10.5)


        pdf.cell(0, 10, '当施設の概要', 0, 1, 'L') 
        pdf.cell(40, 10, '法人名', 1)
        pdf.cell(150, 10, corporation_name, 1, 1)
        pdf.cell(40, 10, '施設・事務所名', 1)
        pdf.cell(150, 10, office_name, 1, 1)
        pdf.cell(40, 10, '代表者名', 1)
        pdf.cell(150, 10, representative_name, 1, 1)
        pdf.cell(40, 10, '管理者名', 1)
        pdf.cell(150, 10, manager_name, 1, 1)
        pdf.cell(40, 10, '電話番号', 1)
        pdf.cell(150, 10, phone_number, 1, 1) 
        pdf.cell(40, 10, '所在地', 1)
        pdf.cell(150, 10, location, 1, 1)
        pdf.cell(40, 10, '立地環境', 1)
        pdf.cell(150, 10, environment, 1, 1)
        pdf.cell(40, 10, '施設区分', 1)
        pdf.cell(150, 10, facility_type, 1, 1)
        pdf.cell(40, 10, '入所者数', 1)
        pdf.cell(150, 10, residents_number, 1, 1)
        pdf.cell(40, 10, '入所者の状況', 1)
        pdf.cell(150, 10, residents_status, 1, 1)
        pdf.cell(40, 10, '職員数', 1)
        pdf.cell(150, 10, staff_number, 1, 1)
        pdf.cell(40, 10, '敷地面積', 1)
        pdf.cell(150, 10, site_area, 1, 1)
        pdf.cell(40, 10, '延べ床面積', 1)
        pdf.cell(150, 10, floor_area, 1, 1)
        pdf.cell(40, 10, '階数', 1)
        pdf.cell(150, 10, floors, 1, 1)
        pdf.cell(40, 10, '部屋数', 1)
        pdf.cell(150, 10, rooms, 1, 1)
        pdf.ln(10)


        pdf.cell(60, 20, '企業理念・経営方針', 1)
        pdf.multi_cell(130, 20, philosophy, 1)
        pdf.cell(60, 20, 'BCP策定の目的1', 1)
        pdf.multi_cell(130, 20, purpose_1, 1)
        pdf.cell(60, 20, 'BCP策定の目的2', 1)
        pdf.multi_cell(130, 20, purpose_2, 1)
        pdf.cell(60, 20, 'BCP策定の目的3', 1)
        pdf.multi_cell(130, 20, purpose_3, 1)
        pdf.ln(60)


        # メンバー情報をテーブル形式で追加
        pdf.set_fill_color(220, 220, 220)
        pdf.cell(0, 10, '推進体制', 0, 1, 'L')
        pdf.cell(40, 10, '主な役割', 1)
        pdf.cell(40, 10, '部署・役職', 1)
        pdf.cell(40, 10, '氏名', 1)
        pdf.cell(70, 10, '補足', 1, 1)
        
        roles = session.get('roles', [])
        departments = session.get('departments', [])
        names = session.get('names', [])
        notes = session.get('notes', [])
        
        for role, department, name, note in zip(roles, departments, names, notes):
            pdf.cell(40, 10, role, 1)
            pdf.cell(40, 10, department, 1)
            pdf.cell(40, 10, name, 1)
            pdf.cell(70, 10, note, 1, 1)
        pdf.ln(10)


        pdf.cell(0, 10, '施設の組織図', 0, 1, 'L')
        if org_chart_path != '不明':
            current_y = pdf.get_y()  # 現在のY座標を取得
            pdf.image(org_chart_path, x=10, y=current_y + 10, w=150)  # 画像を挿入
            pdf.ln(200)  # 画像の高さ分だけ下にスペースを追加


        def add_pdf_as_images(pdf, filepath):
            document = fitz.open(filepath)
            for page_num in range(len(document)):
                page = document.load_page(page_num)
                pix = page.get_pixmap()
                image_path = f'temp_image_{page_num}.png'
                pix.save(image_path)
                pdf.image(image_path, x=10, w=100)
                pdf.ln(10)  # 画像の下にスペースを追加
                os.remove(image_path)  # 一時画像ファイルを削除


        # 地震関連ファイルの出力
        pdf.cell(0, 10, 'リスクの把握 - 地震', 0, 1, 'L')
        earthquake_files = session.get('earthquake_files', [])
        for filepath in earthquake_files:
            if filepath.lower().endswith(('.png', '.jpg', '.jpeg')):
                pdf.image(filepath, x=10, w=100)
                pdf.ln(10)  # 画像の下にスペースを追加
            elif filepath.lower().endswith('.pdf'):
                add_pdf_as_images(pdf, filepath)


        # 水害関連ファイルの出力
        pdf.cell(0, 10, 'リスクの把握 - 水害', 0, 1, 'L')
        flood_files = session.get('flood_files', [])
        for filepath in flood_files:
            if filepath.lower().endswith(('.png', '.jpg', '.jpeg')):
                pdf.image(filepath, x=10, w=100)
                pdf.ln(10)  # 画像の下にスペースを追加
            elif filepath.lower().endswith('.pdf'):
                add_pdf_as_images(pdf, filepath)
        pdf.ln(10)


        pdf.cell(0, 10, '被害想定', 0, 1, 'L')


        pdf.cell(0, 10, '優先する事業', 0, 1, 'L')
        start_x = pdf.get_x()
        start_y = pdf.get_y()
        for business in priority_business:
            pdf.cell(0, 10, business, 0, 1, 'L')
        end_y = pdf.get_y()
        pdf.rect(start_x - 2, start_y, 200, end_y - start_y)  # 優先する事業を囲む黒い枠を追加
        pdf.ln(10)
        
        pdf.cell(0, 10, '優先業務', 0, 1, 'L')
        start_x = pdf.get_x()
        start_y = pdf.get_y()
        for task in priority_tasks:
            pdf.cell(0, 10, task, 0, 1, 'L')
        end_y = pdf.get_y()
        pdf.rect(start_x - 2, start_y, 200, end_y - start_y)  # 優先業務を囲む黒い枠を追加
        pdf.ln(10)


        pdf.cell(0, 10, '優先される物品', 0, 1, 'L')
        start_x = pdf.get_x()
        start_y = pdf.get_y()
        for item in priority_items:
            pdf.cell(0, 10, item, 0, 1, 'L')
        end_y = pdf.get_y()
        pdf.rect(start_x - 2, start_y, 200, end_y - start_y)  # 優先される物品を囲む黒い枠を追加
        pdf.ln(10)
    
        pdf.set_font('IPAexGothic', '', 16)
        pdf.cell(0, 10, '平常時', 0, 1, 'L') 
        pdf.set_font('IPAexGothic', '', 10.5)
        pdf.ln(10)


        # 耐震措置の現状
        current_status_seismic = session.get('current_status_seismic', '不明')
        pdf.cell(0, 10, '耐震措置の現状', 0, 1, 'L')
        pdf.multi_cell(0, 10, current_status_seismic, 1)
        pdf.ln(10)


        # 水害対策の現状
        current_status_flood_measures = session.get('current_status_flood_measures', '不明')
        pdf.cell(0, 10, '水害対策の現状', 0, 1, 'L')
        pdf.multi_cell(0, 10, current_status_flood_measures, 1)
        pdf.ln(10)


        measure_target_mapping = {
            '躯体(柱、壁、床)': ['柱の補強', 'Ｘ型補強', 'コンクリート欠損', 'コンクリートひび', 'コンクリート脱落', 'コンクリート風化', '地震に特化した物品バール'],
            '天井': ['天井の石膏ボードの落下防止'],
            '窓': ['廊下・出入口のガラス飛散防止フィルムの貼付け', 'ガラスの落下・はずれ・ゆるみ・変形'],
            'ドア': ['ドアのはずれ・ゆるみ・変形'],
            '事務所の什器': ['キャビネットは転倒防止のため壁に固定する', 'キャビネットは転倒防止のため突っ張り棒で固定する', '落下の危険性がないようにする'],
            '食堂の什器': ['壁を補強して転倒防止のため壁に固定する', 'ガラス飛散防止フィルムの貼付け', '壁を補強して転倒防止のため突っ張り棒で固定する'],
            '風呂場の什器': ['大型入浴機器を固定する', '棚を壁に固定する'],
            'ロビー・集会所・会議室の什器': ['床に固定する', '壁に固定する', '突っ張り棒で固定する'],
            '利用者居室の什器': ['家具を壁に固定する', '突っ張り棒で固定する'],
            'ノートパソコン': ['机に固定する(ノート)', '重要なデータはバックアップをとり保管する(ノート)', '破損や電源が入らないなど異常はないか確認する(ノート)'],
            'デスクトップパソコン': ['机に固定する(デスク)', '重要なデータはバックアップをとり保管する(デスク)', '破損や電源が入らないなど異常はないか確認する(デスク)'],
            'ディスプレイ': ['机に固定する(ディスプレイ)', '重要なデータはバックアップをとり保管する(ディスプレイ)', '破損や電源が入らないなど異常はないか確認する(ディスプレイ)'],
            'タブレット(iPad)': ['重要なデータはバックアップをとり保管する(iPad)', '破損や電源が入らないなど異常はないか確認する(iPad)'],
            'タブレット(Android)': ['重要なデータはバックアップをとり保管する(Android)', '破損や電源が入らないなど異常はないか確認する(Android)'],
            '携帯電話': ['重要なデータはバックアップをとり保管する(携帯)', '破損や電源が入らないなど異常はないか確認する(携帯)'],
            'スマートフォン': ['重要なデータはバックアップをとり保管する(スマホ)', '破損や電源が入らないなど異常はないか確認する(スマホ)'],
            '固定電話': ['机に固定する(固定電話)'],
            '衛星電話': ['破損や電源が入らないなど異常はないか確認する(衛星)'],
            '金庫': ['飛び出し防止・転倒防止のため床に固定する', '飛び出し防止・転倒防止のため壁に固定する'],
            '受水槽': ['倒壊の可能性有無、防護壁の設置'],
            'ＬＰガス': ['ＬＰガスボンベの固定の強化'],
            '燃油タンク': ['地面への固定アンカーの腐食の有無、金具交換'],
            '太陽光発電': ['太陽光発電装置の固定の強化'],
            '蓄電装置': ['蓄電装置の固定の強化'],
            '出入口': ['建物入口に止水板があるか', '建物入り口に防水扉があるか', '建物入り口に支障となる物品等がおいてないか'],
            '施設周辺': ['避難等に支障となるものはないか'],
            '逆流防止': ['側溝や排水溝が機能するか', '風呂やトイレ等の排水溝からの逆流防止ができているか'],
            '屋外重要設備': ['受電・変電設備の浸水対策', '受水槽の浸水対策', 'LPガスの浸水対策', '蓄電装置の浸水対策'],
            '電気': ['発電機(LPガス)', '発電機燃料(LPガス)', '発電機オイル', '電源リール', 'テーブルタップ'],
            'ガス': ['LPガス', '五徳', '着火ライター'],
            '水道': ['ポリタンク'],
            '通信手段': ['ラジオ', 'トランシーバー', '携帯電話充電器', 'モバイルバッテリー'],
            '情報機器': ['パソコン', 'プリンター', 'データバックアップ・ハードディスク', 'ヘッドライト'],
            '照明機器': ['懐中電灯', '投光器', 'ランタン', '乾電池', 'ろうそく', 'マッチ', 'ライター'],
            '冷暖房': ['石油ストーブ', '灯油', 'カイロ', '湯たんぽ', '保冷剤', '扇風機'],
            '水害対策': ['土のう', 'ゴムボート'],
            '避難用具': ['ヘルメット、懐中電灯', '防災頭巾', 'メガホン、拡声器', '担架', 'リヤカー', '車椅子', '携帯用酸素吸入器', '救助工具セット', '大形テント', 'ブルーシート', 'ロープ', 'ガムテープ'],
            '職員衣服': ['軍手', '雨合羽', '防寒具'],
            '交通手段': ['バイク', '自転車'],
            '現金': ['現金'],
            '衛生': ['紙おむつ', '尿パッド', 'ドライシャンプー', '歯ブラシ', '石けん', 'タオル', '肌着', '生理用品', 'ビニール袋'],
            'トイレ': ['簡易トイレ', '仮設トイレ', 'トイレットペーパー'],
            '睡眠': ['段ボールベッド', '毛布', '寝袋'],
            '飲料': ['飲料水(２リットル/本)', 'ジュース類(果物、野菜)', 'お茶'],
            '食品': ['保存食(アルファ化米)', '米(無洗米)', 'レトルト粥', '缶詰', '経管栄養食', '高カロリー食', 'インスタント食品', '栄養ドリンク'],
            '衛生用品': ['紙コップ、紙皿', '割り箸、使い捨てスプーン', 'ペーパーナプキン、ティッシュペーパー', 'ペーパータオル、ウェットティッシュ', 'ポリ袋、ゴミ袋、ラップ、ブルーシート、ポリタンク（５L）'],
            '厨房関連': ['カセットコンロ、カセットボンベ', 'ホットプレート', '屋外用コンロ（かまど）', 'ナベ、調理器具'],
            '消毒剤薬': [],
            '脱脂綿、絆創膏 ': [],
            '包帯、三角巾 ': [],
            'ウェットティッシュ': [],
            'ホワイトボード': [],
            'マーカー(黒、赤)': [],
            '黒板消し': [],
            'ＢＣＰマニュアル': [],
            '持ち出しファイル': [],
            '記録用紙': [],
            '筆記用具': [],
            '模造紙': [],
            '付箋紙': [],
            '養生テープ': [],
            'ガムテープ': [],
            'サインペン': [],
            '施設レイアウト図': [],
            '周辺地域地図': [],
            '推進体制図': [],
            '連絡先リスト': [],
            'マスク（不織布製マスク）': [],
            'サージカルマスク': [],
            '体温計（非接触型体温計）': [],
            'ゴム手袋（使い捨て）': [],
            'フェイスシールド': [],
            'ゴーグル': [],
            '使い捨て袖付きエプロン': [],
            'ガウン': [],
            'キャップ': [],
            '次亜塩素酸ナトリウム液': [],
            '消毒用アルコール': [],
            'ガーゼ・コットン': [],
            'トイレットペーパー': [],
            'ティッシュペーパー': [],
            '保湿ティッシュ': [],
            '石鹸・液体せっけん': [],
            '紙おむつ': [],
            '自動車': [],
            'バイク': [],
            '自転車': [],
            '電動自転車': [],
            '電気スクーター': [],
            # 電気の項目を追加
            '医療機器（喀痰吸引）': ['自家発電機（喀痰吸引）', '蓄電池（喀痰吸引）', '太陽光パネルの設置（喀痰吸引）', 'その他電気供給源（喀痰吸引）', '400Kw x 8 時間使用可能（喀痰吸引）', '燃料備蓄（喀痰吸引）', 'ガソリンスタンドとの優先供給協定締結（喀痰吸引）', '自動車のバッテリーや電気自動車の電源活用（喀痰吸引）'],
            '医療機器（人工呼吸器）': ['自家発電機（人工呼吸器）', '蓄電池（人工呼吸器）', '太陽光パネルの設置（人工呼吸器）', 'その他電気供給源（人工呼吸器）', '400Kw x 8 時間使用可能（人工呼吸器）', '燃料備蓄（人工呼吸器）', 'ガソリンスタンドとの優先供給協定締結（人工呼吸器）', '自動車のバッテリーや電気自動車の電源活用（人工呼吸器）'],
            '情報機器（PC）': ['自家発電機（PC）', '蓄電池（PC）', '太陽光パネルの設置（PC）', 'その他電気供給源（PC）', '400Kw x 8 時間使用可能（PC）', '燃料備蓄（PC）', 'ガソリンスタンドとの優先供給協定締結（PC）', '自動車のバッテリーや電気自動車の電源活用（PC）'],
            '情報機器（テレビ）': ['自家発電機（テレビ）', '蓄電池（テレビ）', '太陽光パネルの設置（テレビ）', 'その他電気供給源（テレビ）', '400Kw x 8 時間使用可能（テレビ）', '燃料備蓄（テレビ）', 'ガソリンスタンドとの優先供給協定締結（テレビ）', '自動車のバッテリーや電気自動車の電源活用（テレビ）'],
            '情報機器（インターネット）': ['自家発電機（インターネット）', '蓄電池（インターネット）', '太陽光パネルの設置（インターネット）', 'その他電気供給源（インターネット）', '400Kw x 8 時間使用可能（インターネット）', '燃料備蓄（インターネット）', 'ガソリンスタンドとの優先供給協定締結（インターネット）', '自動車のバッテリーや電気自動車の電源活用（インターネット）'],
            '冷蔵庫・冷凍庫': ['自家発電機（冷蔵庫・冷凍庫）', '蓄電池（冷蔵庫・冷凍庫）', '太陽光パネルの設置（冷蔵庫・冷凍庫）', 'その他電気供給源（冷蔵庫・冷凍庫）', '400Kw x 8 時間使用可能（冷蔵庫・冷凍庫）', '燃料備蓄（冷蔵庫・冷凍庫）', 'ガソリンスタンドとの優先供給協定締結（冷蔵庫・冷凍庫）', '保冷剤（冷蔵庫・冷凍庫）', 'その他（冷蔵庫・冷凍庫）'],
            '照明器具': ['自家発電機（照明器具）', '蓄電池（照明器具）', '太陽光パネルの設置（照明器具）', 'その他電気供給源（照明器具）', '自動車のバッテリーや電気自動車の電源活用（照明器具）'],
            '冷暖房器具': ['自家発電機（冷暖房器具）', '蓄電池（冷暖房器具）', '太陽光パネルの設置（冷暖房器具）', 'その他電気供給源（冷暖房器具）', '自動車のバッテリーや電気自動車の電源活用（冷暖房器具）'],
            '暖房機器': ['湯たんぽ', '毛布', '使い捨てカイロ', '灯油ストーブ'],
            '調理器具': ['カセットコンロ', 'ホットプレート', 'ＬＰガスボンベ＋五徳コンロ'],
            '給湯設備': ['入浴は中止し清拭'],
            'その他、代替の熱源': ['都市ガスをＬＰガスに替える'],
            
            '飲料': ['1人が1日に3L必要なため充分量の備蓄をする（食事分を含む）'],
            '食事': ['非常食に用いる'],
            '口腔ケア': ['職員数に応じてサービス提供する必要分を備蓄する'],


            'トイレ_new': ['簡易トイレ（トイレ）', '仮設トイレ（トイレ）', 'オムツ（トイレ）'],
            '清拭_new': ['代替えウエットティッシュを使う（清拭）'],
            '入浴_new': ['当面休止し清拭を行う'],
            '清掃・消毒_new': ['代替えウエットティッシュを使う（清掃・消毒）'],
            
            'スマートフォン_new': ['発電機で充電'],
            'MCA無線機': ['無線機用の乾電池を備蓄'],
            
            'パソコン': ['発電機で電源を供給（パソコン）'],
            'プリンター': ['発電機で電源を供給（プリンター）'],
            'Wi-Fi': ['発電機で電源を供給（Wi-Fi）'],
            
            '水洗トイレ': ['必要な水を確保する'],
            '仮設トイレ': ['レンタル先を確認する'],
            '簡易トイレ': ['備蓄する（簡易トイレ）'],
            'オムツ': ['備蓄する（オムツ）'],
        }
        
        pdf.cell(0, 10, '建物・設備の安全対策（地震、水害）', 0, 1, 'L')
        pdf.cell(0, 10, '建物関連', 0, 1, 'L')
        pdf.set_fill_color(200, 200, 200)
        pdf.cell(40, 10, '対象', 1, 0, 'C', 1)
        pdf.cell(110, 10, '対策', 1, 0, 'C', 1)
        pdf.cell(40, 10, '現状', 1, 1, 'C', 1)
        
        for measure in measure_building:
            target = next((t for t, m in measure_target_mapping.items() if measure in m), '不明')
            pdf.cell(40, 10, target, 1)
            pdf.cell(110, 10, measure, 1)
            pdf.cell(40, 10, current_status_building.get(measure, '不明'), 1, 1)


        pdf.ln(10)


        pdf.cell(0, 10, '什器・コンピュータ', 0, 1, 'L')
        pdf.set_fill_color(200, 200, 200)
        pdf.cell(40, 10, '対象', 1, 0, 'C', 1)
        pdf.cell(110, 10, '対策', 1, 0, 'C', 1)
        pdf.cell(40, 10, '現状', 1, 1, 'C', 1)


        for measure in measure_furniture:
            target = next((t for t, m in measure_target_mapping.items() if measure in m), '不明')
            pdf.cell(40, 10, target, 1)
            pdf.cell(110, 10, measure, 1)
            pdf.cell(40, 10, current_status_furniture.get(measure, '不明'), 1, 1)


        pdf.ln(10)


        pdf.cell(0, 10, '建物外部の施設', 0, 1, 'L')
        pdf.set_fill_color(200, 200, 200)
        pdf.cell(40, 10, '対象', 1, 0, 'C', 1)
        pdf.cell(110, 10, '対策', 1, 0, 'C', 1)
        pdf.cell(40, 10, '現状', 1, 1, 'C', 1)
        
        for measure in measure_external:
            target = next((t for t, m in measure_target_mapping.items() if measure in m), '不明')
            pdf.cell(40, 10, target, 1)
            pdf.cell(110, 10, measure, 1)
            pdf.cell(40, 10, current_status_external.get(measure, '不明'), 1, 1)


        pdf.ln(10)


        pdf.cell(0, 10, '水害対策関連', 0, 1, 'L')
        pdf.set_fill_color(200, 200, 200)
        pdf.cell(40, 10, '対象', 1, 0, 'C', 1)
        pdf.cell(110, 10, '対策', 1, 0, 'C', 1)
        pdf.cell(40, 10, '現状', 1, 1, 'C', 1)


        for measure in measure_flood:
            target = next((t for t, m in measure_target_mapping.items() if measure in m), '不明')
            pdf.cell(40, 10, target, 1)
            pdf.cell(110, 10, measure, 1)
            pdf.cell(40, 10, current_status_flood.get(measure, '不明'), 1, 1)
        pdf.ln(10)


        # 電気
        pdf.cell(0, 10, '稼働させるべき設備及び必要な備品', 0, 1, 'L')
        pdf.cell(0, 10, '電気', 0, 1, 'L')
        pdf.set_fill_color(200, 200, 200)
        pdf.cell(40, 10, '設備', 1, 0, 'C', 1)
        pdf.cell(110, 10, '代替え案', 1, 0, 'C', 1)
        pdf.cell(40, 10, '現状', 1, 1, 'C', 1)


        for measure in measure_electricity:
            target = next((t for t, m in measure_target_mapping.items() if measure in m), '不明')
            pdf.cell(40, 10, target, 1)
            pdf.cell(110, 10, measure, 1)
            pdf.cell(40, 10, current_status_electricity.get(measure, '不明'), 1, 1)
        pdf.ln(10)


        # ガス
        pdf.cell(0, 10, 'ガス', 0, 1, 'L')
        pdf.set_fill_color(200, 200, 200)
        pdf.cell(40, 10, '設備', 1, 0, 'C', 1)
        pdf.cell(110, 10, '代替え案', 1, 0, 'C', 1)
        pdf.cell(40, 10, '現状', 1, 1, 'C', 1)


        for measure in measure_gas:
            target = next((t for t, m in measure_target_mapping.items() if measure in m), '不明')
            pdf.cell(40, 10, target, 1)
            pdf.cell(110, 10, measure, 1)
            pdf.cell(40, 10, current_status_gas.get(measure, '不明'), 1, 1)
        pdf.ln(10)


        # 飲料水
        pdf.cell(0, 10, '飲料水', 0, 1, 'L')
        pdf.set_fill_color(200, 200, 200)
        pdf.cell(40, 10, '設備', 1, 0, 'C', 1)
        pdf.cell(110, 10, '代替え案', 1, 0, 'C', 1)
        pdf.cell(40, 10, '現状', 1, 1, 'C', 1)


        for measure in measure_drinking_water:
            target = next((t for t, m in measure_target_mapping.items() if measure in m), '不明')
            pdf.cell(40, 10, target, 1)
            pdf.cell(110, 10, measure, 1)
            pdf.cell(40, 10, current_status_drinking_water.get(measure, '不明'), 1, 1)
        pdf.ln(10)


        # 生活用水
        pdf.cell(0, 10, '生活用水', 0, 1, 'L')
        pdf.set_fill_color(200, 200, 200)
        pdf.cell(40, 10, '設備', 1, 0, 'C', 1)
        pdf.cell(110, 10, '代替え案', 1, 0, 'C', 1)
        pdf.cell(40, 10, '現状', 1, 1, 'C', 1)


        for measure in measure_life_water_new:
            # "_new" を削除して target を生成
            target = next((t for t, m in measure_target_mapping.items() if measure in m), '不明').replace('_new', '')
            pdf.cell(40, 10, target, 1)
            pdf.cell(110, 10, measure, 1)
            pdf.cell(40, 10, current_status_life_water_new.get(measure, '不明'), 1, 1)
        pdf.ln(10)


        # 通信
        pdf.cell(0, 10, '通信', 0, 1, 'L')
        pdf.set_fill_color(200, 200, 200)
        pdf.cell(40, 10, '設備', 1, 0, 'C', 1)
        pdf.cell(110, 10, '代替え案', 1, 0, 'C', 1)
        pdf.cell(40, 10, '現状', 1, 1, 'C', 1)


        for measure in measure_communication:
            target = next((t for t, m in measure_target_mapping.items() if measure in m), '不明').replace('_new', '')
            pdf.cell(40, 10, target, 1)
            pdf.cell(110, 10, measure, 1)
            pdf.cell(40, 10, current_status_communication.get(measure, '不明'), 1, 1)
        pdf.ln(10)


        # 情報システムのPDF出力
        pdf.cell(0, 10, '情報システム', 0, 1, 'L')
        pdf.set_fill_color(200, 200, 200)
        pdf.cell(40, 10, '設備', 1, 0, 'C', 1)
        pdf.cell(110, 10, '代替え案', 1, 0, 'C', 1)
        pdf.cell(40, 10, '現状', 1, 1, 'C', 1)


        for measure in measure_info_system:
            target = next((t for t, m in measure_target_mapping.items() if measure in m), '不明')
            pdf.cell(40, 10, target, 1)
            pdf.cell(110, 10, measure, 1)
            pdf.cell(40, 10, current_status_info_system.get(measure, '不明'), 1, 1)
        pdf.ln(10)


        # 衛生面
        pdf.cell(0, 10, '衛生面', 0, 1, 'L')
        pdf.set_fill_color(200, 200, 200)
        pdf.cell(40, 10, '設備', 1, 0, 'C', 1)
        pdf.cell(110, 10, '代替え案', 1, 0, 'C', 1)
        pdf.cell(40, 10, '現状', 1, 1, 'C', 1)


        for measure in measure_hygiene:
            target = next((t for t, m in measure_target_mapping.items() if measure in m), '不明')
            pdf.cell(40, 10, target, 1)
            pdf.cell(110, 10, measure, 1)
            pdf.cell(40, 10, current_status_hygiene.get(measure, '不明'), 1, 1)
        pdf.ln(10)


        pdf.cell(0, 10, 'インフラ', 0, 1, 'L')
        pdf.set_fill_color(200, 200, 200)
        pdf.cell(40, 10, '対象', 1, 0, 'C', 1)
        pdf.cell(110, 10, '対策', 1, 0, 'C', 1)
        pdf.cell(40, 10, '現状', 1, 1, 'C', 1)


        for measure in measure_infrastructure:
            target = next((t for t, m in measure_target_mapping.items() if measure in m), '不明')
            pdf.cell(40, 10, target, 1)
            pdf.cell(110, 10, measure, 1)
            pdf.cell(40, 10, current_status_infrastructure.get(measure, '不明'), 1, 1)
        pdf.ln(10)


        pdf.cell(0, 10, '防災備品', 0, 1, 'L')
        pdf.set_fill_color(200, 200, 200)
        pdf.cell(40, 10, '対象', 1, 0, 'C', 1)
        pdf.cell(110, 10, '対策', 1, 0, 'C', 1)
        pdf.cell(40, 10, '現状', 1, 1, 'C', 1)


        for measure in measure_emergency:
            target = next((t for t, m in measure_target_mapping.items() if measure in m), '不明')
            pdf.cell(40, 10, target, 1)
            pdf.cell(110, 10, measure, 1)
            pdf.cell(40, 10, current_status_emergency.get(measure, '不明'), 1, 1)


        pdf.ln(10)


        pdf.cell(0, 10, '飲料、食品', 0, 1, 'L')
        pdf.set_fill_color(200, 200, 200)
        pdf.cell(40, 10, '対象', 1, 0, 'C', 1)
        pdf.cell(110, 10, '対策', 1, 0, 'C', 1)
        pdf.cell(40, 10, '現状', 1, 1, 'C', 1)


        for measure in measure_food:
            target = next((t for t, m in measure_target_mapping.items() if measure in m), '不明')
            pdf.cell(40, 10, target, 1)
            pdf.cell(110, 10, measure, 1)
            pdf.cell(40, 10, current_status_food.get(measure, '不明'), 1, 1)
        pdf.ln(10)


        pdf.cell(0, 10, '医薬品、衛生用品、日用品', 0, 1, 'L')
        pdf.set_fill_color(200, 200, 200)
        pdf.cell(70, 10, '対象', 1, 0, 'C', 1)
        pdf.cell(120, 10, '現状', 1, 1, 'C', 1)


        for target in target_medical:
            pdf.cell(70, 10, target, 1)
            pdf.cell(120, 10, current_status_medical.get(target, '不明'), 1, 1)
        pdf.ln(10) 


        pdf.cell(0, 10, '対策本部の防災備品', 0, 1, 'L')
        pdf.set_fill_color(200, 200, 200)
        pdf.cell(70, 10, '対象', 1, 0, 'C', 1)
        pdf.cell(120, 10, '現状', 1, 1, 'C', 1)


        for target in target_headquarters:
            pdf.cell(70, 10, target, 1)
            pdf.cell(120, 10, current_status_headquarters.get(target, '不明'), 1, 1)
        pdf.ln(10)


        pdf.cell(0, 10, '感染防止', 0, 1, 'L')
        pdf.set_fill_color(200, 200, 200)
        pdf.cell(70, 10, '対象', 1, 0, 'C', 1)
        pdf.cell(120, 10, '現状', 1, 1, 'C', 1)


        for target in target_prevention:
            pdf.cell(70, 10, target, 1)
            pdf.cell(120, 10, current_status_prevention.get(target, '不明'), 1, 1)
        pdf.ln(10)


        pdf.cell(0, 10, '車両', 0, 1, 'L')
        pdf.set_fill_color(200, 200, 200)
        pdf.cell(70, 10, '対象', 1, 0, 'C', 1)
        pdf.cell(120, 10, '現状', 1, 1, 'C', 1)


        for target in target_vehicle:
            pdf.cell(70, 10, target, 1)
            pdf.cell(120, 10, current_status_vehicle.get(target, '不明'), 1, 1)
        pdf.ln(10)    


        pdf.cell(0, 10, '資金手当', 0, 1, 'L')
        pdf.multi_cell(0, 10, funding_measures, 1)
        pdf.ln(10)


        # 他施設・地域との連携内容をPDFに追加
        pdf.cell(0, 10, '他施設・地域との連携', 0, 1, 'L')
        pdf.set_fill_color(200, 200, 200)
        pdf.cell(30, 10, '名称', 1, 0, 'C', 1)
        pdf.cell(50, 10, '住所', 1, 0, 'C', 1)
        pdf.cell(30, 10, '電話', 1, 0, 'C', 1)
        pdf.cell(30, 10, '担当者', 1, 0, 'C', 1)
        pdf.cell(50, 10, '連携内容', 1, 1, 'C', 1)
        
        partner_names = session.get('partner_names', [])
        partner_addresses = session.get('partner_addresses', [])
        partner_phones = session.get('partner_phones', [])
        partner_persons = session.get('partner_persons', [])
        partner_contents = session.get('partner_contents', [])
        
        for name, address, phone, person, content in zip(partner_names, partner_addresses, partner_phones, partner_persons, partner_contents):
            pdf.cell(30, 10, name, 1)
            pdf.cell(50, 10, address, 1)
            pdf.cell(30, 10, phone, 1)
            pdf.cell(30, 10, person, 1)
            pdf.cell(50, 10, content, 1, 1)


        pdf.ln(10)


        # 同一法人内の他施設との連携内容をPDFに追加
        pdf.cell(0, 10, '同一法人内の他施設との連携', 0, 1, 'L')
        pdf.set_fill_color(200, 200, 200)
        pdf.cell(30, 10, '名称', 1, 0, 'C', 1)
        pdf.cell(50, 10, '住所', 1, 0, 'C', 1)
        pdf.cell(30, 10, '電話', 1, 0, 'C', 1)
        pdf.cell(30, 10, '担当者', 1, 0, 'C', 1)
        pdf.cell(50, 10, '連携内容', 1, 1, 'C', 1)
        
        internal_partner_names = session.get('internal_partner_names', [])
        internal_partner_addresses = session.get('internal_partner_addresses', [])
        internal_partner_phones = session.get('internal_partner_phones', [])
        internal_partner_persons = session.get('internal_partner_persons', [])
        internal_partner_contents = session.get('internal_partner_contents', [])
        
        for name, address, phone, person, content in zip(internal_partner_names, internal_partner_addresses, internal_partner_phones, internal_partner_persons, internal_partner_contents):
            pdf.cell(30, 10, name, 1)
            pdf.cell(50, 10, address, 1)
            pdf.cell(30, 10, phone, 1)
            pdf.cell(30, 10, person, 1)
            pdf.cell(50, 10, content, 1, 1)


        pdf.ln(10)


        # 協力医療機関リスト内容をPDFに追加
        pdf.cell(0, 10, '協力医療機関リスト', 0, 1, 'L')
        pdf.set_fill_color(200, 200, 200)
        pdf.cell(30, 10, '名称', 1, 0, 'C', 1)
        pdf.cell(50, 10, '住所', 1, 0, 'C', 1)
        pdf.cell(30, 10, '電話', 1, 0, 'C', 1)
        pdf.cell(30, 10, '担当者', 1, 0, 'C', 1)
        pdf.cell(50, 10, '連携内容', 1, 1, 'C', 1)
        
        medical_partner_names = session.get('medical_partner_names', [])
        medical_partner_addresses = session.get('medical_partner_addresses', [])
        medical_partner_phones = session.get('medical_partner_phones', [])
        medical_partner_persons = session.get('medical_partner_persons', [])
        medical_partner_contents = session.get('medical_partner_contents', [])
        
        for name, address, phone, person, content in zip(medical_partner_names, medical_partner_addresses, medical_partner_phones, medical_partner_persons, medical_partner_contents):
            pdf.cell(30, 10, name, 1)
            pdf.cell(50, 10, address, 1)
            pdf.cell(30, 10, phone, 1)
            pdf.cell(30, 10, person, 1)
            pdf.cell(50, 10, content, 1, 1)


        pdf.ln(10)


        # 協力医療機関以外の関係協力機関内容をPDFに追加
        pdf.cell(0, 10, '協力医療機関以外の関係協力機関', 0, 1, 'L')
        pdf.set_fill_color(200, 200, 200)
        pdf.cell(30, 10, '名称', 1, 0, 'C', 1)
        pdf.cell(50, 10, '住所', 1, 0, 'C', 1)
        pdf.cell(30, 10, '電話', 1, 0, 'C', 1)
        pdf.cell(30, 10, '担当者', 1, 0, 'C', 1)
        pdf.cell(50, 10, '連携内容', 1, 1, 'C', 1)
        
        external_partner_names = session.get('external_partner_names', [])
        external_partner_addresses = session.get('external_partner_addresses', [])
        external_partner_phones = session.get('external_partner_phones', [])
        external_partner_persons = session.get('external_partner_persons', [])
        external_partner_contents = session.get('external_partner_contents', [])
        
        for name, address, phone, person, content in zip(external_partner_names, external_partner_addresses, external_partner_phones, external_partner_persons, external_partner_contents):
            pdf.cell(30, 10, name, 1)
            pdf.cell(50, 10, address, 1)
            pdf.cell(30, 10, phone, 1)
            pdf.cell(30, 10, person, 1)
            pdf.cell(50, 10, content, 1, 1)


        pdf.ln(10)


        # 区市町村担当部署、地域包括支援センター、福祉避難所、管轄消防、自治会、建築指導、保健所等内容をPDFに追加
        pdf.cell(0, 10, '区市町村担当部署、地域包括支援センター、福祉避難所、管轄消防、自治会、建築指導、保健所等', 0, 1, 'L')
        pdf.set_fill_color(200, 200, 200)
        pdf.cell(30, 10, '名称', 1, 0, 'C', 1)
        pdf.cell(50, 10, '住所', 1, 0, 'C', 1)
        pdf.cell(30, 10, '電話', 1, 0, 'C', 1)
        pdf.cell(30, 10, '担当者', 1, 0, 'C', 1)
        pdf.cell(50, 10, '連携内容', 1, 1, 'C', 1)
        
        community_partner_names = session.get('community_partner_names', [])
        community_partner_addresses = session.get('community_partner_addresses', [])
        community_partner_phones = session.get('community_partner_phones', [])
        community_partner_persons = session.get('community_partner_persons', [])
        community_partner_contents = session.get('community_partner_contents', [])
        
        for name, address, phone, person, content in zip(community_partner_names, community_partner_addresses, community_partner_phones, community_partner_persons, community_partner_contents):
            pdf.cell(30, 10, name, 1)
            pdf.cell(50, 10, address, 1)
            pdf.cell(30, 10, phone, 1)
            pdf.cell(30, 10, person, 1)
            pdf.cell(50, 10, content, 1, 1)


        pdf.ln(10)


        # BCP研修・訓練の実施
        pdf.cell(0, 10, 'BCP研修・訓練の実施', 0, 1, 'L')
        bcp_training = session.get('bcp_training', [])
        if bcp_training:
            pdf.set_fill_color(240, 240, 240)  # ボックスの色
            training_text = "\n".join(bcp_training)
            pdf.multi_cell(0, 10, training_text, 1, 'L', 1)
        pdf.ln(10)


        # BCPの検証・見直し
        pdf.cell(0, 10, 'BCPの検証・見直し', 0, 1, 'L')
        bcp_review = session.get('bcp_review', [])
        report_months = session.get('report_months', [])
        if bcp_review or report_months:
            pdf.set_fill_color(240, 240, 240)  # ボックスの色
            review_text = "\n".join(bcp_review)
            if "毎年２回に管理者が理事会に報告する。" in bcp_review:
                review_text += "\n報告月: " + " ".join(report_months)
            pdf.multi_cell(0, 10, review_text, 1, 'L', 1)
        pdf.ln(10)




        inventory = session.get('inventory', [])
        add_table_data(pdf, inventory)
        pdf.ln(10)


        pdf.set_font('IPAexGothic', '', 16)
        pdf.cell(0, 10, '緊急時', 0, 1, 'L') 
        pdf.set_font('IPAexGothic', '', 10.5)
        pdf.ln(10)


        # BCP発動基準の追加
        pdf.cell(0, 10, 'BCP 発動基準', 0, 1, 'L')
        bcp_criteria = session.get('bcp_criteria', [])
        
        if '地震' in bcp_criteria:
            earthquake_city = session.get('earthquake_city', '不明')
            earthquake_intensity = session.get('earthquake_intensity', '不明')
            pdf.multi_cell(0, 10, f"地震：本書に定める緊急時体制は、{earthquake_city}市周辺において、震度{earthquake_intensity}以上の地震が発生したとき。", 1, 'L', 1)
        if '津波' in bcp_criteria:
            tsunami_warning = session.get('tsunami_warning', '不明')
            pdf.multi_cell(0, 10, f"津波：気象庁の津波{tsunami_warning}が発令された場合。", 1, 'L', 1)
        if '水害' in bcp_criteria:
            flood_warning = session.get('flood_warning', '不明')
            pdf.multi_cell(0, 10, f"水害：避難する時間も考慮して考える。施設所在地の都道府県で大型台風の直撃が見込まれる場合。気象庁の警戒レベル{flood_warning}が発令された場合。", 1, 'L', 1)
        if '雪害' in bcp_criteria:
            pdf.multi_cell(0, 10, "雪害：気象庁の大雪注意報等、気象庁の大雪警報等がが発令された場合。", 1, 'L', 1)
        if '高潮' in bcp_criteria:
            pdf.multi_cell(0, 10, "高潮：気象庁の高潮注意報、気象庁の高潮警報が発令された場合。", 1, 'L', 1)
        pdf.ln(10)


        pdf.cell(0, 10, '行動基準', 0, 1, 'L')
        # 画像を追加
        image_path = '/Users/hiroshimatakara/Desktop/app/スクリーンショット 2024-07-13 17.27.48.png'
        if os.path.exists(image_path):
            pdf.image(image_path, x=10, y=None, w=190)




        # 参集基準のデータをPDFに追加
        pdf.cell(0, 10, '参集基準', 0, 1, 'L')




        day_staff = session.get('day_staff', [])
        night_staff = session.get('night_staff', [])
        other_day_staff = session.get('other_day_staff', '')
        other_night_staff = session.get('other_night_staff', '')




        pdf.cell(0, 10, '対象職員：昼間:', 0, 1, 'L')
        pdf.cell(0, 10, ', '.join(day_staff), 0, 1, 'L')
        if other_day_staff:
            pdf.cell(0, 10, f'その他 - {other_day_staff}', 0, 1, 'L')


        pdf.cell(0, 10, '対象職員：夜間:', 0, 1, 'L')
        pdf.cell(0, 10, ', '.join(night_staff), 0, 1, 'L')
        if other_night_staff:
            pdf.cell(0, 10, f'その他 - {other_night_staff}', 0, 1, 'L')
        pdf.ln(10)


        pdf.cell(0, 10, '対応拠点:', 0, 1, 'L')
        pdf.cell(0, 10, f'地震 - 第一拠点: {session.get("earthquake_first_base", "")}', 0, 1, 'L')
        pdf.cell(0, 10, f'地震 - 第二拠点: {session.get("earthquake_second_base", "")}', 0, 1, 'L')
        pdf.cell(0, 10, f'水害 - 第一拠点: {session.get("flood_first_base", "")}', 0, 1, 'L')
        pdf.cell(0, 10, f'水害 - 第二拠点: {session.get("flood_second_base", "")}', 0, 1, 'L')
        pdf.ln(10)


        # 対応体制の追加
        pdf.cell(0, 10, '対応体制', 0, 1, 'L')
        pdf.set_fill_color(200, 200, 200)
        pdf.cell(40, 10, '役職', 1, 0, 'C', 1)
        pdf.cell(40, 10, '名前', 1, 0, 'C', 1)
        pdf.cell(110, 10, '対策本部における職務', 1, 1, 'C', 1)


        response_positions = session.get('response_positions', [])
        response_names = session.get('response_names', [])
        position_duties = {
            "対策本部長": "対策本部組織の統括、全体統括・緊急対応に関する意思決定",
            "事務局長": "対策本部長のサポート・対策本部の運営実務の統括・関係各部署への指示",
            "事務局メンバー": "事務局長のサポート・関係各部署との窓口・社外対応の窓口",
            "広報・情報班": "社外対応(指定権者)・医療機関との連携・関連機関、他施設、関連業者との連携・ホームページ、広報、地域住民への情報公開・活動記録を取る",
            "設備・調達班": "感染防護具の管理、調達・災害の事前対策の実施・災害発生時の物資の調達",
            "現場責任者": "施設内の統括・保健所、医療機関、受診・相談センターへの連絡・利用者、ご家族、職員への情報提供・発信",
            "医療・看護班": "感染拡大防止対策に関する統括・感染防止策の策定、教育・医療ケア",
            "介護班": "介護業務の継続",
            "給食班": "給食業務の継続"
        }


        for position, name in zip(response_positions, response_names):
            duty = position_duties.get(position, '不明')
            pdf.cell(40, 10, position, 1)
            pdf.cell(40, 10, name, 1)
            pdf.cell(110, 10, duty, 1, 1)
        pdf.ln(10)


        pdf.cell(0, 10, '職員の安否確認:', 0, 1, 'L')
        pdf.multi_cell(0, 10, '-職員の安否確認を速やかに行う。\n-速やかに安否確認結果を記録できるよう安否確認シートを準備しておく。')
        pdf.multi_cell(0, 10, '＜施設内＞\n・職員の安否確認は、利用者の安否確認とあわせて各エリアでエリアリーダーが点呼を行い管理者に報告する。')
        pdf.multi_cell(0, 10, '＜施設外・自宅等＞\n・施設外・自宅等で被災した場合は、以下の方法で施設に自身の安否情報を報告する。')


        # 報告方法
        pdf.cell(0, 10, '報告方法:', 0, 1, 'L')
        report_methods = session.get('report_methods', [])
        for method in report_methods:
            pdf.cell(0, 10, f'- {method}', 0, 1, 'L')
        other_report_method = session.get('other_report_method')
        if other_report_method:
            pdf.cell(0, 10, f'- その他: {other_report_method}', 0, 1, 'L')


        pdf.cell(0, 10, '報告内容:', 0, 1, 'L')
        report_content = session.get('report_content', [])
        if report_content:
            for item in report_content:
                pdf.cell(0, 10, f'- {item}', 0, 1)
        else:
            pdf.cell(0, 10, '選択された項目はありません', 0, 1)
        pdf.ln(10)


        # 入居者・利用者の安否確認の追加
        pdf.cell(0, 10, '入居者・利用者の安否確認:', 0, 1, 'L')
        pdf.multi_cell(0, 10, '●入居者・利用者の安否確認を速やかに行う。\n'
                            '●速やかに安否確認結果を記録できるよう安否確認シートを準備しておく。\n'
                            '＜施設内＞\n'
                            '・安否確認は、利用者の安否確認とあわせて各エリアでエリアリーダーが点呼を行い、管理者に報告する。\n')
        pdf.ln(10)
    
        # 施設内の避難場所
        internal_evacuation_site_1 = session.get('internal_evacuation_site_1', '不明')
        internal_evacuation_site_2 = session.get('internal_evacuation_site_2', '不明')
        pdf.cell(0, 10, '施設内の避難場所', 0, 1, 'L')
        pdf.cell(0, 10, f'第1避難場所: {internal_evacuation_site_1}', 1, 1, 'L')
        pdf.cell(0, 10, f'第2避難場所: {internal_evacuation_site_2}', 1, 1, 'L')
        pdf.ln(10)


        # 施設外の避難場所
        external_evacuation_site_1 = session.get('external_evacuation_site_1', '不明')
        external_evacuation_site_2 = session.get('external_evacuation_site_2', '不明')
        pdf.cell(0, 10, '施設外の避難場所', 0, 1, 'L')
        pdf.cell(0, 10, f'第1避難場所: {external_evacuation_site_1}', 1, 1, 'L')
        pdf.cell(0, 10, f'第2避難場所: {external_evacuation_site_2}', 1, 1, 'L')
        pdf.ln(10)


        pdf.cell(0, 10, '重要業務の継続', 0, 1, 'L')
        # テーブルのヘッダー
        pdf.set_fill_color(200, 200, 200)
        pdf.cell(24, 10, '経過 目安', 1, 0, 'C', 1)
        pdf.cell(33.3, 10, '夜間 職員のみ', 1, 0, 'C', 1)
        pdf.cell(33.3, 10, '発災後 6時間', 1, 0, 'C', 1)
        pdf.cell(33.3, 10, '発災後 1日', 1, 0, 'C', 1)
        pdf.cell(33.3, 10, '発災後 3日', 1, 0, 'C', 1)
        pdf.cell(33.3, 10, '発災後 7日', 1, 1, 'C', 1)


        # 出勤率
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(24, 10, '出勤率', 1, 0, 'L', 1)
        pdf.cell(33.3, 10, '出勤率3％', 1, 0, 'C', 1)
        pdf.cell(33.3, 10, '出勤率30％', 1, 0, 'C', 1)
        pdf.cell(33.3, 10, '出勤率50％', 1, 0, 'C', 1)
        pdf.cell(33.3, 10, '出勤率70％', 1, 0, 'C', 1)
        pdf.cell(33.3, 10, '出勤率90％', 1, 1, 'C', 1)


        # 在庫量
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(24, 10, '在庫量', 1, 0, 'L', 1)
        pdf.cell(33.3, 10, '在庫100％', 1, 0, 'C', 1)
        pdf.cell(33.3, 10, '在庫90％', 1, 0, 'C', 1)
        pdf.cell(33.3, 10, '在庫70％', 1, 0, 'C', 1)
        pdf.cell(33.3, 10, '在庫20％', 1, 0, 'C', 1)
        pdf.cell(33.3, 10, '在庫正常', 1, 1, 'C', 1)


        # ライフライン
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(24, 10, 'ライフライン', 1, 0, 'L', 1)
        pdf.cell(33.3, 10, '停電、断水', 1, 0, 'C', 1)
        pdf.cell(33.3, 10, '停電、断水', 1, 0, 'C', 1)
        pdf.cell(33.3, 10, '停電、断水', 1, 0, 'C', 1)
        pdf.cell(33.3, 10, '断水', 1, 0, 'C', 1)
        pdf.cell(33.3, 10, '復旧', 1, 1, 'C', 1)


        # データをセッションから取得してテーブルに追加
        def add_criteria_row(pdf, criteria_name, criteria):
            pdf.cell(24, 10, criteria_name, 1)
            pdf.cell(33.3, 10, criteria.get('night', '未選択'), 1)
            pdf.cell(33.3, 10, criteria.get('6h', '未選択'), 1)
            pdf.cell(33.3, 10, criteria.get('1d', '未選択'), 1)
            pdf.cell(33.3, 10, criteria.get('3d', '未選択'), 1)
            pdf.cell(33.3, 10, criteria.get('7d', '未選択'), 1)
            pdf.ln(10)


        business_criteria = session.get('business_criteria', {})
        meal_service = session.get('meal_service', {})
        meal_assistance = session.get('meal_assistance', {})
        oral_care = session.get('oral_care', {})
        hydration = session.get('hydration', {})
        bathing_assistance = session.get('bathing_assistance', {})

        pdf.set_font('IPAexGothic', '', 4.5)
        add_criteria_row(pdf, '業務基準', business_criteria)
        add_criteria_row(pdf, '給食', meal_service)
        add_criteria_row(pdf, '食事介助', meal_assistance)
        add_criteria_row(pdf, '口腔ケア', oral_care)
        add_criteria_row(pdf, '水分補給', hydration)
        add_criteria_row(pdf, '入浴介助', bathing_assistance)
        pdf.ln(10)
        pdf.set_font('IPAexGothic', '', 10.5)

        pdf.ln(10)
        # タイトル
        pdf.cell(0, 10, '重要業務の継続:夜間職員のみ', 0, 1, 'L')
        # テーブルの行
        def add_row(pdf, label, value):
            pdf.cell(30, 10, label, 1, 0, 'L', 1)
            pdf.cell(150, 10, value, 1, 1, 'C', 1)

        # テーブルのデータをセッションから取得して追加
        business_criteria = session.get('business_criteria', {}).get('night', '未選択')
        meal_service = session.get('meal_service', {}).get('night', '未選択')
        meal_assistance = session.get('meal_assistance', {}).get('night', '未選択')
        oral_care = session.get('oral_care', {}).get('night', '未選択')
        hydration = session.get('hydration', {}).get('night', '未選択')
        bathing_assistance = session.get('bathing_assistance', {}).get('night', '未選択')

        add_row(pdf, '出勤率', '出勤率3％')
        add_row(pdf, '在庫量', '在庫100％')
        add_row(pdf, 'ライフライン', '停電、断水')
        add_row(pdf, '業務基準', business_criteria)
        add_row(pdf, '給食', meal_service)
        add_row(pdf, '食事介助', meal_assistance)
        add_row(pdf, '口腔ケア', oral_care)
        add_row(pdf, '水分補給', hydration)
        add_row(pdf, '入浴介助', bathing_assistance)

        pdf.ln(10)
        # タイトル
        pdf.cell(0, 10, '重要業務の継続:発災後6時間', 0, 1, 'L')
        # テーブルの行
        def add_row(pdf, label, value):
            pdf.cell(30, 10, label, 1, 0, 'L', 1)
            pdf.cell(150, 10, value, 1, 1, 'C', 1)

        # テーブルのデータをセッションから取得して追加
        business_criteria = session.get('business_criteria', {}).get('6h', '未選択')
        meal_service = session.get('meal_service', {}).get('6h', '未選択')
        meal_assistance = session.get('meal_assistance', {}).get('6h', '未選択')
        oral_care = session.get('oral_care', {}).get('6h', '未選択')
        hydration = session.get('hydration', {}).get('6h', '未選択')
        bathing_assistance = session.get('bathing_assistance', {}).get('6h', '未選択')

        add_row(pdf, '出勤率', '出勤率3％')
        add_row(pdf, '在庫量', '在庫100％')
        add_row(pdf, 'ライフライン', '停電、断水')
        add_row(pdf, '業務基準', business_criteria)
        add_row(pdf, '給食', meal_service)
        add_row(pdf, '食事介助', meal_assistance)
        add_row(pdf, '口腔ケア', oral_care)
        add_row(pdf, '水分補給', hydration)
        add_row(pdf, '入浴介助', bathing_assistance)

        pdf.ln(10)
        # タイトル
        pdf.cell(0, 10, '重要業務の継続:発災後1日', 0, 1, 'L')
        # テーブルの行
        def add_row(pdf, label, value):
            pdf.cell(30, 10, label, 1, 0, 'L', 1)
            pdf.cell(150, 10, value, 1, 1, 'C', 1)

        # テーブルのデータをセッションから取得して追加
        business_criteria = session.get('business_criteria', {}).get('1d', '未選択')
        meal_service = session.get('meal_service', {}).get('1d', '未選択')
        meal_assistance = session.get('meal_assistance', {}).get('1d', '未選択')
        oral_care = session.get('oral_care', {}).get('1d', '未選択')
        hydration = session.get('hydration', {}).get('1d', '未選択')
        bathing_assistance = session.get('bathing_assistance', {}).get('1d', '未選択')

        add_row(pdf, '出勤率', '出勤率3％')
        add_row(pdf, '在庫量', '在庫100％')
        add_row(pdf, 'ライフライン', '停電、断水')
        add_row(pdf, '業務基準', business_criteria)
        add_row(pdf, '給食', meal_service)
        add_row(pdf, '食事介助', meal_assistance)
        add_row(pdf, '口腔ケア', oral_care)
        add_row(pdf, '水分補給', hydration)
        add_row(pdf, '入浴介助', bathing_assistance)

        pdf.ln(10)
        # タイトル
        pdf.cell(0, 10, '重要業務の継続:発災後3日', 0, 1, 'L')
        # テーブルの行
        def add_row(pdf, label, value):
            pdf.cell(30, 10, label, 1, 0, 'L', 1)
            pdf.cell(150, 10, value, 1, 1, 'C', 1)

        # テーブルのデータをセッションから取得して追加
        business_criteria = session.get('business_criteria', {}).get('3d', '未選択')
        meal_service = session.get('meal_service', {}).get('3d', '未選択')
        meal_assistance = session.get('meal_assistance', {}).get('3d', '未選択')
        oral_care = session.get('oral_care', {}).get('3d', '未選択')
        hydration = session.get('hydration', {}).get('3d', '未選択')
        bathing_assistance = session.get('bathing_assistance', {}).get('3d', '未選択')

        add_row(pdf, '出勤率', '出勤率3％')
        add_row(pdf, '在庫量', '在庫100％')
        add_row(pdf, 'ライフライン', '停電、断水')
        add_row(pdf, '業務基準', business_criteria)
        add_row(pdf, '給食', meal_service)
        add_row(pdf, '食事介助', meal_assistance)
        add_row(pdf, '口腔ケア', oral_care)
        add_row(pdf, '水分補給', hydration)
        add_row(pdf, '入浴介助', bathing_assistance)

        pdf.ln(10)
        # タイトル
        pdf.cell(0, 10, '重要業務の継続:発災後7日', 0, 1, 'L')
        # テーブルの行
        def add_row(pdf, label, value):
            pdf.cell(30, 10, label, 1, 0, 'L', 1)
            pdf.cell(150, 10, value, 1, 1, 'C', 1)

        # テーブルのデータをセッションから取得して追加
        business_criteria = session.get('business_criteria', {}).get('7d', '未選択')
        meal_service = session.get('meal_service', {}).get('7d', '未選択')
        meal_assistance = session.get('meal_assistance', {}).get('7d', '未選択')
        oral_care = session.get('oral_care', {}).get('7d', '未選択')
        hydration = session.get('hydration', {}).get('7d', '未選択')
        bathing_assistance = session.get('bathing_assistance', {}).get('7d', '未選択')

        add_row(pdf, '出勤率', '出勤率3％')
        add_row(pdf, '在庫量', '在庫100％')
        add_row(pdf, 'ライフライン', '停電、断水')
        add_row(pdf, '業務基準', business_criteria)
        add_row(pdf, '給食', meal_service)
        add_row(pdf, '食事介助', meal_assistance)
        add_row(pdf, '口腔ケア', oral_care)
        add_row(pdf, '水分補給', hydration)
        add_row(pdf, '入浴介助', bathing_assistance)
        pdf.ln(10)



        # 職員の休憩、宿泊場所
        pdf.cell(0, 10, '職員の休憩、宿泊場所:', 0, 1, 'L')
        pdf.cell(0, 10, f'休憩場所 第1優先: {session.get("rest_location_priority1", "")}', 0, 1, 'L')
        pdf.cell(0, 10, f'休憩場所 第2優先: {session.get("rest_location_priority2", "")}', 0, 1, 'L')
        pdf.cell(0, 10, f'休憩場所 施設外: {session.get("rest_location_external", "")}', 0, 1, 'L')
        pdf.cell(0, 10, f'宿泊場所 第1優先: {session.get("accommodation_priority1", "")}', 0, 1, 'L')
        pdf.cell(0, 10, f'宿泊場所 第2優先: {session.get("accommodation_priority2", "")}', 0, 1, 'L')
        pdf.cell(0, 10, f'宿泊場所 施設外: {session.get("accommodation_external", "")}', 0, 1, 'L')
        pdf.ln(10)


        pdf.cell(0, 10, '勤務シフト:', 0, 1, 'L')
        pdf.cell(0, 10, '＜勤務シフトの原則＞最低週１日は休日とする。')
        pdf.ln(10)


        # セッションからデータを取得
        measure_options = session.get('measure_options', {})
        # 復旧対応 破損個所の確認表の整備のセクションを追加
        pdf.cell(0, 10, '復旧対応 破損個所の確認表の整備', 0, 1, 'L')
        pdf.set_fill_color(200, 200, 200)
        pdf.cell(40, 10, '対象', 1, 0, 'C', 1)
        pdf.cell(110, 10, '対策', 1, 0, 'C', 1)
        pdf.cell(40, 10, '破損状況', 1, 1, 'C', 1)


        target_recovery_res = session.get('target_recovery_res', [])
        measure_recovery_res = session.get('measure_recovery_res', [])
        current_status_recovery_res = session.get('current_status_recovery_res', {})


        for target in target_recovery_res:
            for measure in measure_options.get(target, []):
                pdf.cell(40, 10, target.replace('_res', ''), 1)
                pdf.cell(110, 10, measure, 1)
                pdf.cell(40, 10, current_status_recovery_res.get(measure, '不明'), 1, 1)


        pdf.ln(10)
        
        # 他施設・地域との連携、同一法人内の他施設との連携、協力医療機関リスト、協力医療機関以外の関係協力機関、区市町村担当部署等の連携内容をPDFに追加
        pdf.cell(0, 10, '復旧対応 業者連絡先一覧の整備', 0, 1, 'L')
        pdf.set_fill_color(200, 200, 200)
        pdf.cell(30, 10, '名称', 1, 0, 'C', 1)
        pdf.cell(50, 10, '住所', 1, 0, 'C', 1)
        pdf.cell(30, 10, '電話', 1, 0, 'C', 1)
        pdf.cell(30, 10, '担当者', 1, 0, 'C', 1)
        pdf.cell(50, 10, '連携内容', 1, 1, 'C', 1)


        # データの取得と統合
        partner_data = [
            ('他施設・地域との連携', session.get('partner_names', []), session.get('partner_addresses', []), session.get('partner_phones', []), session.get('partner_persons', []), session.get('partner_contents', [])),
            ('同一法人内の他施設との連携', session.get('internal_partner_names', []), session.get('internal_partner_addresses', []), session.get('internal_partner_phones', []), session.get('internal_partner_persons', []), session.get('internal_partner_contents', [])),
            ('協力医療機関リスト', session.get('medical_partner_names', []), session.get('medical_partner_addresses', []), session.get('medical_partner_phones', []), session.get('medical_partner_persons', []), session.get('medical_partner_contents', [])),
            ('協力医療機関以外の関係協力機関', session.get('external_partner_names', []), session.get('external_partner_addresses', []), session.get('external_partner_phones', []), session.get('external_partner_persons', []), session.get('external_partner_contents', [])),
            ('区市町村担当部署、地域包括支援センター、福祉避難所、管轄消防、自治会、建築指導、保健所等', session.get('community_partner_names', []), session.get('community_partner_addresses', []), session.get('community_partner_phones', []), session.get('community_partner_persons', []), session.get('community_partner_contents', []))
        ]


        # 各連携内容のデータをPDFに追加
        for section_title, names, addresses, phones, persons, contents in partner_data:
            for name, address, phone, person, content in zip(names, addresses, phones, persons, contents):
                pdf.cell(30, 10, name, 1)
                pdf.cell(50, 10, address, 1)
                pdf.cell(30, 10, phone, 1)
                pdf.cell(30, 10, person, 1)
                pdf.cell(50, 10, content, 1, 1)


        pdf.ln(10)


        # 復旧対応 情報発信の整備のセクションを追加
        pdf.cell(0, 10, '復旧対応 情報発信の整備', 0, 1, 'L')
        pdf.multi_cell(0, 10, '''●公表のタイミング、範囲、内容、方法についてあらかじめ方針を定めておく。
        風評被害を招く恐れもあるため、広報・情報班が、一元的に丁寧な対応や説明を行う。
        ''')


        public_content = session.get('public_content', [])
        public_range = session.get('public_range', [])
        public_method = session.get('public_method', [])


        pdf.cell(0, 10, '公表内容:', 0, 1, 'L')
        for content in public_content:
            pdf.cell(0, 10, f'- {content}', 0, 1, 'L')
        
        pdf.cell(0, 10, '範囲:', 0, 1, 'L')
        for range_item in public_range:
            pdf.cell(0, 10, f'- {range_item}', 0, 1, 'L')
        
        pdf.cell(0, 10, '方法:', 0, 1, 'L')
        for method in public_method:
            pdf.cell(0, 10, f'- {method}', 0, 1, 'L')
        pdf.ln(10)


        pdf.cell(0, 10, '連携体制の構築', 0, 1, 'L')
        lines = [
            "●連携体制構築の検討",
            "・平常時から他施設・他法人と協力関係を築くことが大切。",
            "・単に協定書を結ぶだけではなく、普段から良好な関係を作る。",
            "・主な連携先と提携状況を【補足１４】に記述する。",
            " ①近隣の法人",
            " ②所属している団体を通じての協力関係の整備",
            " ③自治体を通じて地域での協力体制を構築など",
            "●連携体制の構築・参画",
            "・単独での事業継続が困難な事態を想定して施設・事業所を取り巻く関係各位と協力関係を日ごろから構築しておく。",
            "・地域で相互支援ネットワークが構築されている場合は、それらに加入を検討する。",
            "●連携の推進ステップ",
            "①連携先との協議",
            "連携先と連携内容を協議中であれば、それら協議内容や今後の計画などを記載する。",
            "②連携協定書の締結",
            "地域との連携に関する協議が整えば、その証として連携協定書を締結し、写しを添付する。",
            "③地域のネットワーク等の構築・参画",
            "施設・事業所の倒壊や多数の職員の被災等、単独での事業継続が困難な事態を想定して、施設・事業所を取り巻く",
            "関係各位と協力関係を日ごろから構築しておく。",
            "地域で相互に支援しあうネットワークが構築されている場合はそれらに加入することを検討する。"
        ]
        for line in lines:
            pdf.cell(0, 10, line, 0, 1, 'L')


        pdf.ln(10)
        
        pdf.cell(0, 10, '連携対応', 0, 1, 'L')
        lines = [
            "①事前準備",
            "連携協定に基づき、被災時に相互に連携し支援しあえるように検討した事項や今後準備すべき事項などを記載する。",
            "・連携先と可能な範囲で相互に利用者の受入を行う。",
            "②入所者・利用者情報の整理",
            "避難先施設でも適切なケアを受けることができるよう、最低限必要な利用者情報を「利用者カード」などに、",
            "あらかじめまとめておく。",
            "・避難先に必ずしも担当の職員も同行して利用者の引継ぎを行えるとは限らない。",
            "避難先で適切なケアを受けることができるよう利用情報を記載した「利用者カード」を作成しておくことでリスクを",
            "低減する。",
            "③共同訓練",
            "連携先と共同で行う訓練概要について記載する。",
            "・連携先や地域の方とともに定期的に訓練を行い、施設の実状を理解いただき、対応力を高める。"
        ]
        for line in lines:
            pdf.cell(0, 10, line, 0, 1, 'L')


        pdf.ln(10)


        # 地域との連携 被災時の職員の派遣のセクションを追加
        pdf.cell(0, 10, '地域との連携 被災時の職員の派遣', 0, 1, 'L')
        local_cooperation_dispatch = session.get('local_cooperation_dispatch', [])
        if local_cooperation_dispatch:
            for item in local_cooperation_dispatch:
                pdf.cell(0, 10, f'- {item}', 0, 1, 'L')
        else:
            pdf.cell(0, 10, '', 0, 1, 'L')
        pdf.ln(10)


        pdf.cell(0, 10, '地域との連携 福祉避難所の運営 福祉避難所の事前準備', 0, 1, 'L')
        pdf.multi_cell(0, 10, "③福祉避難所開設の事前準備\n福祉避難所として運営できるように事前に必要な物資の確保や施設整備などを進める。\nまた、受入にあたっては支援人材の確保が重要であり、自施設の職員だけでなく、専門人材の支援が受けられるよう社会福祉協議会などの関係団体や支援団体等と支援体制について協議し、ボランティアの受入方針等について検討しておく。\n＜主な準備事項例＞")


        welfare_shelter_preparation = session.get('welfare_shelter_preparation', [])
        for item in welfare_shelter_preparation:
            pdf.cell(0, 10, f'・{item}', 0, 1, 'L')
        pdf.ln(10)
        


        # 地域との連携 福祉避難所の運営 福祉避難所の指定のセクションを追加
        pdf.cell(0, 10, '地域との連携 福祉避難所の運営 福祉避難所の指定', 0, 1, 'L')
        welfare_shelter = session.get('welfare_shelter', '')
        if welfare_shelter == '福祉避難所である':
            pdf.multi_cell(0, 10, "①福祉避難所の指定\n福祉避難所の指定を受けた場合は、自治体との協定書を添付するとともに、受入可能人数、受入場所、受入期間、受入条件など諸条件を整理して記載する。")
        elif welfare_shelter == '福祉避難所でない':
            pdf.multi_cell(0, 10, "②福祉避難所の指定がない場合\n社会福祉施設の公共性を鑑みれば、可能な限り福祉避難所の指定を受けることが望ましいが仮に指定を受けない場合でも被災時に外部から要援護者や近隣住民等の受入の要望に沿うことができるよう上記のとおり諸条件を整理しておく。\nその際、想定を超える人数の要援護者や近隣住民等が、施設・事業所へ支援を求めて来る場合も想定し、対応の仕方等を事前に検討しておく。")
        else:
            pdf.cell(0, 10, '選択された項目はありません', 0, 1, 'L')
        pdf.ln(10)

        pdf.cell(0, 10, '通所サービス固有', 0, 1, 'L')
        if '通所(デイサービス)' in priority_business:
            pdf.multi_cell(0, 10, """（２）災害が予想される場合の対応
    ●台風などで甚大な被害が予想される場合などにおいては、サービスの休止・縮小を余儀なくされることを想定し、あらかじめその基準を定めておくとともに、居宅介護支援事業所にも情報共有の上、利用者やその家族にも説明する。
    ●その上で、必要に応じ、サービスの前倒し等も検討する。
    （３）災害発生時の対応
    ● サービス提供を長期間休止する場合は、居宅介護支援事業所と連携し、必要に応じて他事業所の訪問サービス等への変更を検討する。
    ●利用中に被災した場合は、利用者の安否確認後、あらかじめ把握している緊急連絡先を活用し、利用者家族への安否状況の連絡を行う。
    ●利用者の安全確保や家族への連絡状況を踏まえ、順次利用者の帰宅を支援する。
    その際、送迎車の利用が困難な場合も考慮して、手段を検討する。
    ●帰宅にあたって、可能であれば利用者家族の協力も得る。関係機関とも連携しながら事業所での宿泊や近くの避難所への移送等で対応する。""")
            
        pdf.ln(10)
        pdf.cell(0, 10, '訪問サービス固有', 0, 1, 'L')
        if '訪問(与薬、食事)' in priority_business or '訪問(入浴)' in priority_business:
            pdf.multi_cell(0, 10, """（２）災害が予想される場合の対応
    ●台風などで甚大な被害が予想される場合などにおいては、サービスの休止・縮小を余儀なくされることを想定し、あらかじめその基準を定めておくとともに、居宅介護支援事業所にも情報共有の上、利用者やその家族にも説明する。
    ●その上で、必要に応じ、サービスの前倒し等も検討する。
    （３）災害発生時の対応
    ● サービス提供を長期間休止する場合は、居宅介護支援事業所と連携し、必要に応じて他事業所の訪問サービス等への変更を検討する。
    ●あらかじめ検討した対応方法に基づき、利用者への安否確認等や、利用者宅を訪問中または移動中の場合の対応を行う。
    ●居宅介護支援事業所や地域の関係機関と連携の上、可能な場合には、避難先においてサービスを提供する。""")
        pdf.ln(10)

        pdf.cell(0, 10, '居宅介護支援サービス固有', 0, 1, 'L')
        if '居宅支援(ケアマネージャー)' in priority_business:
            pdf.multi_cell(0, 10, """（２）災害が予想される場合の対応
    ●訪問サービスや通所サービスについて、「台風などで甚大な被害が予想される場合などにおいては、サービスの休止・縮小を余儀なくされることを想定し、あらかじめその基準を定めておく」とされており、利用者が利用する各事業所が定める基準について、事前に情報共有し、把握しておくこと。その上で、必要に応じ、サービスの前倒し等も検討する。
    ●また、自サービスについても、台風などで甚大な被害が予想される場合などにおいては、休止・縮小を余儀なくされることを想定し、その際の対応方法を定めておくとともに、他の居宅介護支援事業所、居宅サービス事業所、地域の関係機関に共有の上、利用者やその家族にも説明する。
    （３）災害発生時の対応
    ●災害発生時で、事業が継続できる場合には、可能な範囲で、個別訪問等による早期の状態把握を通じ、居宅サービスの実施状況の把握を行い、被災生活により状態の悪化が懸念される利用者に対して、必要な支援が提供されるよう、居宅サービス事業所、地域の関係機関との連絡調整等を行う。
    （例）通所・訪問サービスについて、利用者が利用している事業所が、サービス提供を長期間休止する場合は、必要に応じて他事業所の通所サービスや、訪問サービス等への変更を検討する。
    ●また、避難先においてサービス提供が必要な場合も想定され、居宅サービス事業所、地域の関係機関と連携しながら、利用者の状況に応じて、必要なサービスが提供されるよう調整を行う。
    ●災害発生時で事業が継続できない場合には、他の居宅介護支援事業所、居宅サービス事業所、地域の関係機関と事前に検討・調整した対応を行う。""")

        pdf_file = 'output.pdf'
        pdf.output(pdf_file)
        return send_file(pdf_file)


    except Exception as e:
        logging.error(f"Error generating PDF: {e}")
        return str(e), 500
    
if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(host='0.0.0.0', port=5001)





