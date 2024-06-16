from flask import Flask, render_template, request, send_file, session, redirect, url_for
from fpdf import FPDF
from flask_session import Session  # セッション管理用
import os
import logging
from werkzeug.utils import secure_filename

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
        session['priority_business'] = request.form.getlist('priority_business[]')
        session['priority_tasks'] = request.form.getlist('priority_tasks[]')
        session['priority_items'] = request.form.getlist('priority_items[]')
        return redirect(url_for('step2'))
    return render_template('step1.html') 

@app.route('/step2', methods=['GET', 'POST'])
def step2():
    if request.method == 'POST':
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

        return redirect(url_for('step3'))
    return render_template('step2.html')

@app.route('/step3', methods=['GET', 'POST'])
def step3():
    if request.method == 'POST':
        # フォームデータをセッションに保存
        session['entity'] = request.form['entity']
        session['responsibility'] = request.form['responsibility']
        # PDF生成のルートへリダイレクト
        return redirect(url_for('generate_pdf'))
    return render_template('step3.html')

@app.route('/generate_pdf', methods=['GET', 'POST'])
def generate_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('IPAexGothic', '', 'ipaexg.ttf', uni=True)

    # 新しいテーブルのヘッダー定義
    def add_table_header(pdf, title):
        pdf.cell(0, 10, title, 0, 1, 'L')
        pdf.set_fill_color(200, 200, 200)
        pdf.cell(30, 10, '対象', 1, 0, 'C', 1)
        pdf.cell(20, 10, '目安', 1, 0, 'C', 1)
        pdf.cell(20, 10, '備蓄量', 1, 0, 'C', 1)
        pdf.cell(20, 10, '必要量', 1, 0, 'C', 1)
        pdf.cell(20, 10, '過不足量', 1, 0, 'C', 1)
        pdf.cell(10, 10, '単位', 1, 0, 'C', 1)
        pdf.cell(20, 10, '保管場所', 1, 0, 'C', 1)
        pdf.cell(20, 10, '担当者', 1, 0, 'C', 1)
        pdf.cell(20, 10, '調達先', 1, 0, 'C', 1)
        pdf.cell(20, 10, '備考', 1, 1, 'C', 1)

    # 新しいテーブルを追加する関数
    def add_table_data(pdf, target_list, title):
        add_table_header(pdf, title)
        for target in target_list:
            pdf.cell(30, 10, target, 1)
            # 以下に新しいテーブルのカラムを追加
            pdf.cell(20, 10, '', 1)
            pdf.cell(20, 10, '', 1)
            pdf.cell(20, 10, '', 1)
            pdf.cell(20, 10, '', 1)
            pdf.cell(10, 10, '', 1)
            pdf.cell(20, 10, '', 1)
            pdf.cell(20, 10, '', 1)
            pdf.cell(20, 10, '', 1)
            pdf.cell(20, 10, '', 1, 1)

    # 対象を選択肢2から取得するセクション
    def add_table_data_from_measures(pdf, measure_list, title):
        add_table_header(pdf, title)
        for measure in measure_list:
            pdf.cell(30, 10, measure, 1)
            # 以下に新しいテーブルのカラムを追加
            pdf.cell(20, 10, '', 1)
            pdf.cell(20, 10, '', 1)
            pdf.cell(20, 10, '', 1)
            pdf.cell(20, 10, '', 1)
            pdf.cell(10, 10, '', 1)
            pdf.cell(20, 10, '', 1)
            pdf.cell(20, 10, '', 1)
            pdf.cell(20, 10, '', 1)
            pdf.cell(20, 10, '', 1, 1)
    
    # 題名を追加
    pdf.set_font('IPAexGothic', '', 24)  # フォントサイズを大きく設定
    pdf.cell(0, 20, '介護BCP', ln=True, align='C')  # 題名を中央揃えで追加
    pdf.set_font('IPAexGothic', '', 14)

    # セッションからデータを取得してPDFに追加
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
    entity = session.get('entity', '不明')
    responsibility = session.get('responsibility', '不明')

    pdf.cell(0, 10, '当施設の概要', 0, 1, 'L')  
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

    pdf.cell(60, 40, '企業理念・経営方針', 1)
    pdf.multi_cell(130, 40, philosophy, 1)
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

    pdf.ln(10)
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
        '電気スクーター': []
        }


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

    # セッションからデータを取得してPDFに追加
    measure_target_mapping = {
        'インフラ': session.get('measure_infrastructure', []),
        '防災備品': session.get('measure_emergency', []),
        '飲料、食品': session.get('measure_food', [])
    }

    # PDFにデータを追加
    add_table_data_from_measures(pdf, measure_target_mapping['インフラ'], 'インフラ')
    add_table_data_from_measures(pdf, measure_target_mapping['防災備品'], '防災備品')
    add_table_data_from_measures(pdf, measure_target_mapping['飲料、食品'], '飲料、食品')

    add_table_data(pdf, session.get('target_medical', []), '医薬品、衛生用品、日用品')
    add_table_data(pdf, session.get('target_headquarters', []), '対策本部の防災備品')
    add_table_data(pdf, session.get('target_prevention', []), '感染防止')

    entity = session.get('entity', '不明')
    responsibility = session.get('responsibility', '不明')
    pdf.cell(200, 10, txt=f"主体: {entity}", ln=True)
    pdf.cell(200, 10, txt=f"責任者: {responsibility}", ln=True)

    pdf_file = 'output.pdf'
    pdf.output(pdf_file)
    return send_file(pdf_file)

if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
