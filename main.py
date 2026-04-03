import requests
import json
import os
import random  # Dùng để tạo mã số OTP ngẫu nhiên
import re  # Thêm re nếu chưa có ở đầu file để xử lý tách ID từ link
from datetime import datetime
from flask_mail import Mail, Message  # Thư viện gửi email
from datetime import datetime
from flask import Flask
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask import Flask, request, jsonify
from flask import Flask, render_template, request, jsonify
base_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
def extract_uid_from_link(link):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept-Language': 'en-US,en;q=0.9'
        }

        response = requests.get(
            link,
            allow_redirects=True,
            timeout=10,
            headers=headers
        )

        final_url = response.url
        print("FINAL URL:", final_url)

        html = response.text

        # ======================
        # ✅ FACEBOOK
        # ======================
        id_match = re.search(r'id=(\d+)', final_url)
        if id_match:
            return id_match.group(1)

        uid_match = re.search(r'"userID":"(\d+)"', html)
        if uid_match:
            return uid_match.group(1)

        uid_match2 = re.search(r'"actorID":"(\d+)"', html)
        if uid_match2:
            return uid_match2.group(1)

        # ======================
        # ✅ TIKTOK
        # ======================
        secuid_match = re.search(r'"secUid":"(.*?)"', html)
        if secuid_match:
            return secuid_match.group(1)

        userid_match = re.search(r'"id":"(\d+)"', html)
        if userid_match:
            return userid_match.group(1)

        username_match = re.search(r'tiktok\.com/@([^/?]+)', final_url)
        if username_match:
            return username_match.group(1)

        # ======================
        # ✅ INSTAGRAM
        # ======================
        ig_userid = re.search(r'"profilePage_(\d+)"', html)
        if ig_userid:
            return ig_userid.group(1)

        ig_userid2 = re.search(r'"id":"(\d+)"', html)
        if ig_userid2:
            return ig_userid2.group(1)

        ig_username = re.search(r'instagram\.com/([^/?]+)/?', final_url)
        if ig_username:
            username = ig_username.group(1)
            if username not in ["p", "reel", "stories"]:
                return username

        ig_post = re.search(r'instagram\.com/p/([^/?]+)', final_url)
        if ig_post:
            return ig_post.group(1)

        # ======================
        # ✅ YOUTUBE
        # ======================

        # 🔥 channelId chuẩn (UCxxxx)
        yt_channel = re.search(r'"channelId":"(UC[\w-]+)"', html)
        if yt_channel:
            return yt_channel.group(1)

        # 🔥 handle dạng @name
        yt_handle = re.search(r'youtube\.com/@([^/?]+)', final_url)
        if yt_handle:
            return yt_handle.group(1)

        # 🔥 link dạng /channel/UCxxxx
        yt_channel2 = re.search(r'youtube\.com/channel/(UC[\w-]+)', final_url)
        if yt_channel2:
            return yt_channel2.group(1)

        # 🔥 video → lấy videoId
        yt_video = re.search(r'v=([\w-]+)', final_url)
        if yt_video:
            return yt_video.group(1)

        yt_video2 = re.search(r'youtu\.be/([\w-]+)', final_url)
        if yt_video2:
            return yt_video2.group(1)

    except Exception as e:
        print("Lỗi UID:", e)

    return None
@app.route('/api/parse-link', methods=['POST'])
def parse_link():
    data = request.json
    link = data.get('link', '')

    print("LINK:", link)

    if not link:
        return jsonify({'success': False, 'message': 'Link không hợp lệ'})

    uid = extract_uid_from_link(link)

    print("UID:", uid)  # 👈 QUAN TRỌNG

    if uid:
        return jsonify({'success': True, 'uid': uid})
    else:
        return jsonify({'success': False, 'message': 'Không lấy được UID'})
static_folder=os.path.join(base_dir, 'static')
app.secret_key = "taphoachongoi_secret_key"
# --- CẤU HÌNH GỬI MAIL ---
# --- CẤU HÌNH MAILTRAP THEO ẢNH CỦA ÔNG ---
# --- CẤU HÌNH MAILTRAP CHUẨN ---
app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = '414f101eb0836f' 
app.config['MAIL_PASSWORD'] = '8d90473a212714'
# Thêm dòng này nếu chưa có
app.config['MAIL_DEFAULT_SENDER'] = 'admin@taphoachongoi.com' 

mail = Mail(app)
# --- CẤU HÌNH HỆ THỐNG ---
# --- CẤU HÌNH HỆ THỐNG CŨ (SẢN PHẨM) ---
SYSTEM_API_KEY = "sk_6091479bbac161fe6fc0e308edac8d46e672aa421eecd40c"
SYSTEM_BASE_URL = "http://node12.zampto.net:20291/api"
SYSTEM_HEADERS = {"X-API-Key": SYSTEM_API_KEY}

# --- CẤU HÌNH DVMXH (SUBGIARE) ---
KHOMMO_TOKEN = "68723cdd4153e26fe9e3a38274420c53AZOLu0sUn8ltNEiezI3rPKqhacBkSXpx"
NGANHANGSUB_API = "https://nganhangsub.vn/api/v2"
NGANHANGSUB_KEY = "eyJpdiI6IkhYRDBGellhaUNNRjlHN2JXR1pxR3c9PSIsInZhbHVlIjoia0dEMTAyVTUwUkFBWVUwMzRidlZvazR4SVJPVFBzMThCWU9JaXlLRlRuUT0iLCJtYWMiOiJhYjAyNGJlNDgxZGRlYmU3MzEzZTUzZDE5ZjgxNWNlZDk4NWZiZWUzZTY0M2RmMTdiMDA0ZjMzMDczNWNhMGIxIiwidGFnIjoiIn0="
USER_FILE = 'users.json'
NOTICE_FILE = 'announcement.json'
CUSTOM_PRICE_FILE = 'custom_prices.json'
CUSTOM_PRODUCT_FILE = 'custom_products.json'
ORDER_FILE = 'orders.json'

def get_resource_list():
    # Link API chuẩn ông vừa đưa
    url = "https://khommo.vn/api/products.php?api_key=68723cdd4153e26fe9e3a38274420c53AZOLu0sUn8ltNEiezI3rPKqhacBkSXpx"
    
    try:
        response = requests.get(url, timeout=10)
        
        # In ra để kiểm tra hàng đã về chưa
        print(f"Khommo API Result: {response.text[:200]}")
        
        if response.status_code == 200:
            return response.json() # Trả về mảng sản phẩm
        return []
    except Exception as e:
        print(f"Lỗi kết nối API Khommo: {e}")
        return []

# --- HÀM XỬ LÝ DỮ LIỆU ---
def load_json(filename, default_value):
    if not os.path.exists(filename): return default_value
    with open(filename, 'r', encoding='utf-8') as f:
        try: return json.load(f)
        except: return default_value

def save_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_users():
    return load_json(USER_FILE, [{"username": "admin", "password": "123", "email": "admin@gmail.com", "balance": 1000000, "role": "admin"}])

# --- LOGIC API & GIÁ ---
def fetch_api(endpoint, method="GET", data=None):
    url = f"https://khommo.com/api/v2{endpoint}" 
    headers = {"Api-Token": "TOKEN_CUA_BAC"}
    try:
        url = f"{SYSTEM_BASE_URL}{endpoint}" # Dùng URL hệ thống sản phẩm
        if method == "GET":
            res = requests.get(url, headers=SYSTEM_HEADERS, timeout=5)
        else:
            res = requests.post(url, headers=SYSTEM_HEADERS, json=data, timeout=5)
        return res.json()
    except: return None

def get_products_with_custom_prices():
    # 1. Lấy từ hệ thống cũ
    res = fetch_api("/products")
    system_p = res.get("products", []) if res else []
    
    # 2. Lấy từ Khommo (nhớ trỏ vào categories như tui nói lúc nãy)
    khommo_p = get_resource_list()
    if not isinstance(khommo_p, list): khommo_p = []

    # 3. Lấy sản phẩm bác tự "Add Product" thủ công
    manual_custom_p = load_json(CUSTOM_PRODUCT_FILE, [])

    # Gộp tất cả lại thành một nồi lẩu thập cẩm
    all_products = system_p + khommo_p + manual_custom_p
    
    # 4. QUAN TRỌNG: Đè giá từ file custom_prices.json
    custom_prices = load_json(CUSTOM_PRICE_FILE, {})
    
    for p in all_products:
        p_id = str(p.get('id'))
        if p_id in custom_prices:
            # Nếu bác đã sửa giá trong Admin, nó sẽ lấy giá đó (9999)
            p['price'] = int(custom_prices[p_id])
            
    return all_products
@app.route('/api/nganhangsub/services')
def nganhangsub_services():
    try:
        res = requests.post(
    "https://nganhangsub.vn/api/v2",
    data={
        "key": NGANHANGSUB_KEY,
        "action": "services"
    }
)

        print("STATUS:", res.status_code)
        print("RAW:", res.text)

        return jsonify(res.json())
    except Exception as e:
        return jsonify({"error": str(e)})
@app.route('/api/nganhangsub/order', methods=['POST'])
def nganhangsub_order():
    data = request.get_json()

    res = requests.post(
        "https://nganhangsub.vn/api/v2",
        data={
            "key": NGANHANGSUB_KEY,
            "action": "add",
            "service": data.get("service"),
            "link": data.get("link"),
            "quantity": data.get("quantity")
        }
    )
    return jsonify(res.json()) 
@app.route('/api/nganhangsub/balance')
def nganhangsub_balance():
    res = requests.post(
        "https://nganhangsub.vn/api/v2",
        data={
            "key": NGANHANGSUB_KEY,
            "action": "balance"
        }
    )
    return jsonify(res.json())
@app.template_filter('format_money')
def format_money(value):
    try:
        if value is None:
            return "0đ"
        return "{:,.0f}đ".format(float(value)).replace(",", ".")
    except:
        return "0đ"

# --- [QUAN TRỌNG] TRANG CHỦ LANDING ---
@app.route('/')
def home():
    return render_template('home.html')

# --- ROUTES ĐĂNG NHẬP & ĐĂNG KÝ ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = load_users()
        u_name, u_pass = request.form.get('username'), request.form.get('password')
        user = next((u for u in users if u['username'] == u_name and u['password'] == u_pass), None)
        if user:
            session.update({'user': u_name, 'role': user.get('role', 'user')})
            return redirect(url_for('dashboard'))
        flash("Sai tài khoản hoặc mật khẩu!", "error")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = load_users()
        u_name = request.form.get('username')
        u_email = request.form.get('email')
        u_pass = request.form.get('password')
        if any(u['username'] == u_name for u in users):
            flash("Tài khoản đã tồn tại!", "error")
        else:
            users.append({"username": u_name, "password": u_pass, "email": u_email, "balance": 0, "role": "user"})
            save_json(USER_FILE, users)
            flash("Đăng ký thành công!", "success")
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        u_name = request.form.get('username')
        u_email = request.form.get('email')
        old_p = request.form.get('old_password')
        new_p = request.form.get('new_password')
        
        users = load_users()
        # Tìm user khớp cả 3 thông tin: Username, Email và Mật khẩu cũ
        user = next((u for u in users if u['username'] == u_name 
                     and u.get('email') == u_email 
                     and u['password'] == old_p), None)
        
        if user:
            # Cập nhật mật khẩu mới
            for u in users:
                if u['username'] == u_name:
                    u['password'] = new_p
                    break
            save_json(USER_FILE, users)
            flash("Đổi mật khẩu thành công! Hãy đăng nhập lại.", "success")
            return redirect(url_for('login'))
        else:
            flash("Thông tin (Tài khoản/Email/MK cũ) không chính xác!", "error")
            
    return render_template('forgot_password.html')

@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    if 'reset_otp' not in session: return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        user_otp = request.form.get('otp')
        new_p = request.form.get('new_password')
        
        if user_otp == session.get('reset_otp'):
            users = load_users()
            for u in users:
                if u['username'] == session['reset_user']:
                    u['password'] = new_p # Đổi mật khẩu mới
                    break
            save_json(USER_FILE, users)
            session.pop('reset_otp', None) # Xóa mã sau khi dùng xong
            flash("Đổi mật khẩu thành công!", "success")
            return redirect(url_for('login'))
        flash("Mã OTP sai rồi ông ơi!", "error")
    return render_template('verify_otp.html')

@app.route('/dvmxh')
def dvmxh_page():
    if 'user' not in session: return redirect(url_for('login'))
    
    # Lấy thông tin user
    users = load_users()
    user_data = next((u for u in users if u['username'] == session['user']), None)
    
    # Lấy data từ Khommo và giá đã lưu
    api_items = get_khommo_data()
    categories = api_items.get('categories', []) if isinstance(api_items, dict) else []
    
    # Đảm bảo load_json trả về một dict sạch
    saved_prices = load_json('khommo_prices.json', {})
    
    all_products = []
    for cat in categories:
        cat_name = cat.get('name', 'Khác')
        for p in cat.get('products', []):
            # 1. Ép ID về String để khớp với Key trong JSON
            p_id = str(p.get('id', ''))
            
            # 2. Xử lý giá gốc từ API (đề phòng lỗi float 404.6)
            try:
                orig_price = int(float(p.get('price') or 0))
            except:
                orig_price = 0
            
            # 3. LẤY GIÁ: Kiểm tra trong saved_prices trước
            # Dùng float() rồi int() để đảm bảo không bị lỗi định dạng khi so sánh
            final_price = saved_prices.get(p_id)
            if final_price is not None:
                try:
                    display_price = int(float(final_price))
                except:
                    display_price = orig_price
            else:
                display_price = orig_price
            
            all_products.append({
                "id": p_id,
                "name": p.get('name'),
                "price": display_price, # Giá đã được cập nhật
                "category": cat_name,
                "amount": p.get('amount', 0),
                "description": p.get('description', '') # Thêm description để popup hiện thông tin
            })

    return render_template('dvmxh.html', 
                           username=user_data['username'], 
                           balance=user_data['balance'],
                           products=all_products)
@app.route('/dashboard')
def dashboard():
    if 'user' not in session: 
        return redirect(url_for('login'))
    
    # LOAD LẠI FILE JSON NGAY TẠI ĐÂY ĐỂ CẬP NHẬT SỐ DƯ MỚI NHẤT
    users = load_users() 
    user_data = next((u for u in users if u['username'] == session['user']), None)
    
    if not user_data:
        return redirect(url_for('logout'))

    notice = load_json(NOTICE_FILE, {"content": "Chào mừng!", "date": "01/04/2026", "title": "Thông báo"})
    all_orders = load_json(ORDER_FILE, [])
    user_orders = [o for o in all_orders if o['username'] == session['user']]
    
    # Truyền balance từ user_data vừa load xong
    return render_template('dashboard.html', 
                           username=user_data['username'], 
                           balance=user_data['balance'], 
                           announcements=[notice], 
                           orders=user_orders)

@app.route('/products')
def products_page():
    if 'user' not in session: return redirect(url_for('login'))
    
    users = load_users()
    user_data = next((u for u in users if u['username'] == session['user']), None)
    
    # Gọi hàm đã gộp sạch sẽ ở trên
    full_list = get_products_with_custom_prices()
    
    all_orders = load_json(ORDER_FILE, [])
    user_orders = [o for o in all_orders if o['username'] == session['user']]
    
    return render_template('products.html', 
                           username=user_data['username'], 
                           balance=user_data['balance'], 
                           products=full_list, 
                           orders=user_orders)

@app.route('/orders')
def orders_page():
    if 'user' not in session: return redirect(url_for('login'))
    
    users = load_users()
    user_data = next((u for u in users if u['username'] == session['user']), None)
    
    # Load toàn bộ đơn hàng và lọc theo user đang đăng nhập
    all_orders = load_json(ORDER_FILE, [])
    user_orders = [o for o in all_orders if o['username'] == session['user']]
    
    # Trả về template orders.html (hoặc dùng chung dashboard tùy ông)
    return render_template('orders.html', 
                           username=user_data['username'], 
                           balance=user_data['balance'], 
                           orders=user_orders)
# --- API MUA HÀNG (PHÂN TÁCH RÕ RÀNG) ---
# --- API MUA HÀNG FIX CHO CẢ 2 LOẠI CUSTOM ---
# --- API MUA HÀNG TRẢ VỀ ACC/PASS (DÙNG CHO CLONE/KEY/ACCOUNT) ---
@app.route('/api/buy', methods=['POST'])
def buy_product():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Chưa đăng nhập'}), 401
    
    data = request.get_json()
    p_id = str(data.get('product_id'))
    qty = int(data.get('quantity', 1))
    link = data.get('link', '')

    users = load_users()
    u_idx = next((i for i, u in enumerate(users) if u['username'] == session['user']), None)
    if u_idx is None: return jsonify({'success': False, 'message': 'User không tồn tại'})

    # ==========================================================
    # 🔥 BƯỚC 1: XỬ LÝ HÀNG CUSTOM (Account/Key/Clone)
    # ==========================================================
    custom_p1 = load_json("custom_products.json", [])
    custom_p2 = load_json("custom_services.json", [])
    all_custom = custom_p1 + custom_p2
    
    item = next((p for p in all_custom if str(p.get('id')) == p_id or str(p.get('service')) == p_id), None)

    if item:
        product_name = item.get('name')
        price = int(item.get('price') or item.get('rate') or 0)
        total = price * qty

        if users[u_idx]['balance'] < total:
            return jsonify({'success': False, 'message': f'Thiếu {(total - users[u_idx]["balance"]):,.0f}đ!'})

        # --- LẤY THÔNG TIN TÀI KHOẢN TỪ NỘI DUNG SẢN PHẨM ---
        # Giả sử trong item['content'] ông để danh sách acc, mỗi dòng 1 acc
        full_content = item.get('content', '') or item.get('description', '')
        lines = [l.strip() for l in full_content.split('\n') if l.strip()]
        
        if len(lines) < qty:
            return jsonify({'success': False, 'message': 'Hết hàng trong kho!'})

        # Lấy ra số lượng acc khách mua
        bought_accs = lines[:qty]
        remaining_accs = lines[qty:]
        result_str = "\n".join(bought_accs) # Đây là cái sẽ hiện ra cho khách

        # --- CẬP NHẬT LẠI KHO HÀNG (Xóa những acc đã bán) ---
        # Tìm đúng file để cập nhật lại nội dung còn lại
        updated = False
        for fname in ["custom_products.json", "custom_services.json"]:
            f_data = load_json(fname, [])
            for p in f_data:
                if str(p.get('id')) == p_id or str(p.get('service')) == p_id:
                    p['content'] = "\n".join(remaining_accs)
                    updated = True
                    break
            if updated:
                save_json(fname, f_data)
                break

        # Trừ tiền
        users[u_idx]['balance'] -= total
        save_json(USER_FILE, users)

        # Lưu lịch sử đơn hàng
        orders = load_json(ORDER_FILE, [])
        orders.insert(0, {
            "username": session['user'],
            "product_name": f"[ACCOUNT] {product_name}",
            "content": result_str, # Lưu lại acc đã mua vào đơn hàng
            "quantity": qty,
            "total": total,
            "status": "Hoàn thành",
            "date": datetime.now().strftime("%H:%M:%S %d/%m/%Y")
        })
        save_json(ORDER_FILE, orders)

        # Trả về cho Frontend kèm theo list tài khoản
        return jsonify({
            'success': True, 
            'message': 'Mua thành công!',
            'data': result_str  # CÁI NÀY LÀ TK | MK ĐỂ HIỆN LÊN MÀN HÌNH
        })
    # ==========================================================
    # 🔥 BƯỚC 2: NẾU KHÔNG PHẢI CUSTOM -> GỬI API SANG NGANHANGSUB
    # ==========================================================
    try:
        # Check giá từ client gửi lên hoặc từ file giá admin set
        custom_prices = load_json(CUSTOM_PRICE_FILE, {})
        if p_id in custom_prices:
            price = int(custom_prices[p_id])
        else:
            price = int(data.get("price", 0))

        total = price * qty
        if users[u_idx]['balance'] < total:
            return jsonify({'success': False, 'message': 'Số dư không đủ!'})

        # Gọi API bên NganHangSub
        res = requests.post(
            "https://nganhangsub.vn/api/v2",
            data={
                "key": NGANHANGSUB_KEY,
                "action": "add",
                "service": p_id,
                "link": link,
                "quantity": qty
            }
        ).json()

        if res.get("status") == "success" or res.get("data"):
            # Trừ tiền sau khi API báo thành công
            users[u_idx]['balance'] -= total
            save_json(USER_FILE, users)

            orders = load_json(ORDER_FILE, [])
            orders.insert(0, {
                "username": session['user'],
                "product_name": f"Dịch vụ Buff #{p_id}",
                "content": link,
                "quantity": qty,
                "total": total,
                "status": "Đang chạy",
                "date": datetime.now().strftime("%H:%M:%S %d/%m/%Y")
            })
            save_json(ORDER_FILE, orders)
            return jsonify({'success': True, 'message': 'Đã tạo đơn Buff thành công!'})
        else:
            msg = res.get("message") or res.get("error") or "Lỗi từ nhà cung cấp"
            return jsonify({'success': False, 'message': f"API từ chối: {msg}"})

    except Exception as e:
        return jsonify({'success': False, 'message': f"Lỗi hệ thống: {str(e)}"})
def get_uid_route():
    data = request.json
    link = data.get('link')
    
    # Giả sử đây là hàm bóc UID của ông
    uid = your_function_to_get_uid(link) 
    
    # THÊM DÒNG NÀY ĐỂ KIỂM TRA TRÊN TERMINAL CMD
    print(f"--- CHECK LINK: {link} => UID BÓC ĐƯỢC: {uid} ---")
    
    if uid:
        return jsonify({"success": True, "uid": uid})
    else:
        return jsonify({"success": False, "message": "Không tìm thấy UID!"})
def buy():
    data = request.json
    user_input = data.get('link') # Đây có thể là UID số hoặc Link gốc
    
    # KIỂM TRA NẾU LÀ LINK THÌ TỰ BÓC TRÊN SERVER LUÔN
    if "http" in user_input:
        uid = auto_get_uid(user_input) # Hàm bóc UID của ông
        if uid:
            final_id = uid
        else:
            return jsonify({"success": False, "message": "Link không hợp lệ, không bóc được UID!"})
    else:
        final_id = user_input
# --- ROUTES ADMIN ---

@app.route('/admin')
def admin_panel():
    if session.get('role') != 'admin': return redirect(url_for('dashboard'))
    
    api_res = fetch_api("/balance")
    # Lấy danh sách đã được "độ" giá hoàn chỉnh
    final_list = get_products_with_custom_prices()

    return render_template('admin.html', 
                           users=load_users(), 
                           api_balance=api_res.get("balance", 0) if api_res else 0, 
                           products=final_list)

@app.route('/manage-users')
def manage_users():
    # 1. Kiểm tra đăng nhập (Dùng đúng 'user' như code của ông ở các route khác)
    if 'user' not in session:
        return redirect(url_for('login'))

    # 2. Lấy data mới nhất từ hàm get_current_user_data (Hàm này ông đã có ở cuối file)
    data = get_current_user_data(session['user'])
    
    # 3. Load danh sách tất cả users để admin quản lý
    all_users = load_users()

    # 4. Trả về template với đầy đủ biến để đồng bộ ví
    return render_template('manage_users.html', 
                           username=session['user'], 
                           balance=data['balance'],  # Đã đồng bộ số dư
                           role=data['role'],        # Đã đồng bộ quyền
                           users=all_users)

@app.route('/api/admin/delete-user', methods=['POST'])
def delete_user_api():
    if session.get('role') != 'admin': return jsonify({'success': False}), 403
    
    data = request.get_json()
    username_to_delete = data.get('username')
    
    users = load_users()
    # Lọc bỏ thằng cần xóa
    new_users = [u for u in users if u['username'] != username_to_delete]
    
    # Lưu lại file JSON của ông (đổi tên file cho đúng)
    with open('users.json', 'w', encoding='utf-8') as f:
        json.dump(new_users, f, indent=4)
        
    return jsonify({'success': True})    

@app.route('/api/admin/add-product', methods=['POST'])
def add_product():
    data = request.get_json()
    
    # 1. Load dữ liệu (Đặt tên là gì thì tí dùng tên đó)
    custom_products_list = load_json(CUSTOM_PRODUCT_FILE, []) 
    
    # 2. Tạo sản phẩm mới
    new_p = {
        "id": data.get('id'),
        "name": data.get('name'),
        "price": int(data.get('price')),
        "content": data.get('content'), # CMD báo content đã có dữ liệu rồi, giữ nguyên
        "stock": 99
    }
    
    # 3. SỬA LỖI Ở ĐÂY: Phải dùng đúng tên biến ở bước 1
    # Bác đang viết là custom_p.append nên nó lỗi NameError
    custom_products_list.append(new_p) 
    
    # 4. Lưu lại
    save_json(CUSTOM_PRODUCT_FILE, custom_products_list)
    
    return jsonify({'success': True})
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# --- CẤU HÌNH NẠP TIỀN ---
BANK_CONFIG = {
    "bank_name": "Vietcombank",
    "account_number": "1234567890",
    "account_holder": "BUI VIET DUC",
    "min_deposit": 10000,
    "qr_template": "https://img.vietqr.io/image/{bank_id}-{acc_no}-compact2.jpg?amount={amount}&addInfo={content}&accountName={acc_name}"
}

@app.route('/deposit')
def deposit_page():
    if 'user' not in session: return redirect(url_for('login'))
    
    users = load_users()
    user_data = next((u for u in users if u['username'] == session['user']), None)
    
    # Nội dung chuyển khoản tự động (ví dụ: NAP user123)
    transfer_content = f"NAP {user_data['username']}".upper()
    
    # Tạo link QR (để số tiền trống để khách tự nhập hoặc mặc định 0)
    qr_url = BANK_CONFIG["qr_template"].format(
        bank_id="vcb", # Mã ngân hàng (vcb, mb, icb...)
        acc_no=BANK_CONFIG["account_number"],
        amount="",
        content=transfer_content,
        acc_name=BANK_CONFIG["account_holder"].replace(" ", "%20")
    )
    
    return render_template('deposit.html', 
                           username=user_data['username'], 
                           balance=user_data['balance'],
                           bank=BANK_CONFIG,
                           transfer_content=transfer_content,
                           qr_url=qr_url)

@app.route('/members')
def members_page():
    # Không cần check login vì đây là trang công khai
    users = load_users()
    
    # Sắp xếp user theo số dư giảm dần (Top Đại Gia)
    # Chỉ lấy các trường cần thiết để bảo mật (ẩn email, password)
    public_users = []
    sorted_users = sorted(users, key=lambda x: x.get('balance', 0), reverse=True)
    
    for u in sorted_users:
        public_users.append({
            "username": u['username'],
            "balance": u['balance'],
            "role": u.get('role', 'user')
        })
    
    # Lấy thông tin user hiện tại nếu đã login (để highlight chính mình)
    current_user = session.get('user')
    
    return render_template('members.html', 
                           users=public_users, 
                           current_user=current_user)

@app.route('/api/admin/add-balance', methods=['POST']) # Đổi từ update-balance thành add-balance
def add_balance():
    if session.get('role') != 'admin': return jsonify({'success': False}), 403
    data = request.get_json()
    username = data.get('username')
    amount = int(data.get('amount', 0))
    
    users = load_users()
    u_idx = next((i for i, u in enumerate(users) if u['username'] == username), None)
    
    if u_idx is not None:
        users[u_idx]['balance'] += amount
        save_json(USER_FILE, users)
        return jsonify({'success': True, 'new_balance': users[u_idx]['balance']})
    return jsonify({'success': False, 'message': 'Không tìm thấy user'})

@app.route('/change-password', methods=['POST'])
def change_password():
    if 'user' not in session: 
        return jsonify({'success': False, 'message': 'Hết phiên đăng nhập!'}), 401
    
    # Lấy dữ liệu từ form
    email_input = request.form.get('email')
    old_pass = request.form.get('old_password')
    new_pass = request.form.get('new_password')
    
    if not email_input or not old_pass or not new_pass:
        return jsonify({'success': False, 'message': 'Vui lòng nhập đầy đủ thông tin!'})

    users = load_users()
    # Tìm user hiện tại trong danh sách
    u_idx = next((i for i, u in enumerate(users) if u['username'] == session['user']), None)
    
    if u_idx is not None:
        target_user = users[u_idx]
        
        # LOGIC KIỂM TRA: Gmail và Mật khẩu cũ phải khớp
        if target_user.get('email') != email_input:
            return jsonify({'success': False, 'message': 'Gmail xác nhận không chính xác!'})
        
        if target_user.get('password') != old_pass:
            return jsonify({'success': False, 'message': 'Mật khẩu cũ không đúng!'})
        
        # Kiểm tra độ dài mật khẩu mới
        if len(new_pass) < 3:
            return jsonify({'success': False, 'message': 'Mật khẩu mới quá ngắn!'})

        # Nếu mọi thứ đều đúng -> Cập nhật
        users[u_idx]['password'] = new_pass
        save_json(USER_FILE, users)
        return jsonify({'success': True, 'message': 'Đổi mật khẩu thành công!'})
    
    return jsonify({'success': False, 'message': 'Không tìm thấy tài khoản!'})

def get_current_user_data(username):
    users = load_users() # Đọc file JSON ngay lập tức
    user_data = next((u for u in users if u['username'] == username), None)
    if user_data:
        return {
            "balance": user_data.get('balance', 0), 
            "role": user_data.get('role', 'user')
        }
    return {"balance": 0, "role": "user"}

@app.route('/api/admin/change-user-password', methods=['POST'])
def admin_change_user_password():
    # Kiểm tra quyền admin
    if 'user' not in session or get_current_user_data(session['user']).get('role') != 'admin':
        return jsonify({'success': False, 'message': 'Không có quyền!'}), 403
    
    data = request.json
    username = data.get('username')
    new_password = data.get('new_password')
    
    users = load_users()
    for u in users:
        if u['username'] == username:
            u['password'] = new_password # Đổi thẳng mk cho user
            save_json(USER_FILE, users)
            return jsonify({'success': True, 'message': 'Đổi mật khẩu thành công'})
  
    return jsonify({'success': False, 'message': 'User không tồn tại'})

@app.route('/api/admin/announcement', methods=['POST'])
def update_announcement_api():
    # Kiểm tra quyền admin cho chắc chắn
    if session.get('role') != 'admin': 
        return jsonify({'success': False, 'message': 'Không có quyền!'}), 403
    
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    
    if not title or not content:
        return jsonify({'success': False, 'message': 'Thiếu nội dung!'})

    # Tạo object thông báo mới
    new_notice = {
        "title": title,
        "content": content,
        "date": datetime.now().strftime("%d/%m/%Y")
    }
    
    # Lưu vào file announcement.json (biến NOTICE_FILE ông đã định nghĩa ở đầu file)
    save_json(NOTICE_FILE, new_notice)
    
    return jsonify({'success': True, 'message': 'Cập nhật thông báo thành công!'})

@app.route('/api/dvmxh/get-services', methods=['POST'])
def get_services():
    try:
        # Dòng này cực quan trọng để tránh lỗi 415
        # force=True giúp Flask bỏ qua việc kiểm tra Header nếu cần
        data_input = request.get_json(force=True, silent=True) or {}
        
        # Gọi API Khommo (Thay URL và API Key của bác vào đây)
        api_url = "https://khommo.com/api/service/get-list" # Kiểm tra lại URL đúng của Khommo nhé
        api_key = "MA_API_CUA_BAC" 
        
        # Giả sử bác gọi API như này
        # response = requests.post(api_url, data={'api_key': api_key})
        # res_data = response.json()

        # Đây là dữ liệu mẫu để test, bác thay bằng dữ liệu thật từ API Khommo
        res_data = {
            "status": "success",
            "categories": [
                {"id": "47", "name": "Acc TikTok", "price": 1000, "stock": 99},
                {"id": "48", "name": "Acc Facebook", "price": 2000, "stock": 50}
            ]
        }
        
        return jsonify(res_data)

    except Exception as e:
        print(f"Lỗi rồi: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

import requests
from flask import request, jsonify, session

@app.route('/api/user/profile', methods=['GET'])
def get_khommo_profile():
    url = f"https://khommo.vn/api/profile.php?api_key={API_KEY}"
    try:
        res = requests.get(url)
        return jsonify(res.json())
    except:
        return jsonify({"status": "error"}), 500
# 3. Kiểm tra chi tiết đơn hàng (Order)
@app.route('/api/dvmxh/order-detail/<order_id>', methods=['GET'])
def get_order_detail(order_id):
    # Link bác gửi: https://khommo.vn/api/order.php?api_key=...&order=...
    url = f"https://khommo.vn/api/order.php?api_key={API_KEY}&order={order_id}"
    try:
        res = requests.get(url)
        return jsonify(res.json())
    except:
        return jsonify({"status": "error"}), 500
@app.route('/api/dvmxh/order', methods=['POST'])
def api_khommo_buy():
    try:
        req_data = request.get_json(force=True)
        p_id = req_data.get('category_id')
        qty = int(req_data.get('amount', 0))

        # 1. Lấy thông tin giá từ Khommo để tính tiền
        p_info_res = requests.get(f"https://khommo.vn/api/product.php?api_key={API_KEY}&product={p_id}")
        p_info = p_info_res.json()
        item = p_info[0] if isinstance(p_info, list) else p_info
        
        price = int(item.get('price', 0))
        total_pay = price * qty

        # 2. Lấy số dư thực tế của User từ Database của bác (Ví dụ dùng session)
        # user = User.query.filter_by(username=session['username']).first()
        # if user.balance < total_pay:
        #    return jsonify({"status": "error", "message": "Số dư không đủ để thanh toán!"})

        # 3. Nếu đủ tiền -> Gọi lệnh mua bên Khommo (Cần check lại link buy.php của họ)
        buy_url = f"https://khommo.vn/api/buy.php?api_key={API_KEY}&product={p_id}&quantity={qty}"
        buy_res = requests.get(buy_url).json()

        if buy_res.get('status') == 'success':
            # 4. Trừ tiền user trong DB của bác ở đây
            # user.balance -= total_pay
            # db.session.commit()
            return jsonify({"status": "success", "message": "Mua hàng thành công!"})
        else:
            return jsonify({"status": "error", "message": buy_res.get('message', 'Lỗi nhà cung cấp')})

    except Exception as e:
        return jsonify({"status": "error", "message": f"Lỗi hệ thống: {str(e)}"}), 500
# API lấy danh sách sản phẩm (Account/Key)
@app.route('/api/admin/get-products', methods=['GET'])
def admin_get_products():
    try:
        res = requests.get(f"https://khommo.vn/api/product.php?api_key={API_KEY}")
        return jsonify({"success": True, "data": res.json()})
    except:
        return jsonify({"success": False, "message": "Lỗi API"})

# API cập nhật giá (Bác dùng chung cho cả 2 loại)
@app.route('/api/admin/update-price', methods=['POST'])
def admin_update_price():
    try:
        # force=True để nó không bắt bẻ Content-Type
        data = request.get_json(force=True, silent=True)
        
        # Log ra màn hình đen (Terminal) để bác soi xem JS gửi cái gì lên
        print(f"--- Dữ liệu nhận được: {data} ---")

        if not data:
            return jsonify({"success": False, "message": "JSON bị trống hoặc sai định dạng"}), 400

        p_id = str(data.get('id'))
        new_price = data.get('price')

        if not p_id or new_price is None:
            return jsonify({"success": False, "message": "Thiếu id hoặc price"}), 400

        # Lưu vào file JSON của bác
        custom_prices = load_json(CUSTOM_PRICE_FILE, {})
        custom_prices[p_id] = int(new_price)
        save_json(CUSTOM_PRICE_FILE, custom_prices)

        return jsonify({"success": True, "message": "Ngon lành rồi bác!"})
    except Exception as e:
        print(f"Lỗi Python: {e}")
        return jsonify({"success": False, "message": str(e)}), 500
@app.route('/api/admin/update-buff-price', methods=['POST'])
def update_buff_price():
    data = request.get_json()
    service_id = data.get('id')
    new_price = data.get('new_price')
    # Logic update giá vào Database hoặc File cấu hình của bác
    # db.execute("UPDATE buff_services SET price = ? WHERE id = ?", (new_price, service_id))
    return jsonify({"success": True, "message": "Đã cập nhật giá Buff"})
@app.route('/api/admin/delete-product', methods=['POST'])
def delete_product():
    if session.get('role') != 'admin': 
        return jsonify({'success': False, 'message': 'Không có quyền'}), 403
    
    try:
        # Lấy data an toàn hơn
        data = request.get_json(silent=True) or {}
        # Chấp nhận cả 2 kiểu đặt tên để tránh lỗi JavaScript gửi lệch
        p_id = str(data.get('id') or data.get('product_id') or "")

        if not p_id:
            return jsonify({'success': False, 'message': 'Không nhận được ID sản phẩm'}), 400

        # Xử lý xóa trong file custom_products.json
        products = load_json(CUSTOM_PRODUCT_FILE, [])
        new_products = [p for p in products if str(p.get('id')) != p_id]
        
        if len(products) == len(new_products):
            return jsonify({'success': False, 'message': f'Không tìm thấy sản phẩm ID {p_id} trong danh sách custom'}), 404

        save_json(CUSTOM_PRODUCT_FILE, new_products)
        return jsonify({'success': True})
    except Exception as e:
        print(f"Lỗi xóa: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500
@app.route('/forgot_password')
def forgot_password_route():
    # Phải đảm bảo file forgot_password.html nằm TRONG thư mục templates
    return render_template('forgot_password.html')
@app.route('/api/admin/delete-custom-product', methods=['POST'])
def delete_custom_product():
    if session.get('role') != 'admin': 
        return jsonify({'success': False, 'message': 'Không có quyền'}), 403
    
    try:
        data = request.get_json(force=True)
        p_id = str(data.get('id')) # Lấy ID sản phẩm muốn xóa

        if not p_id:
            return jsonify({'success': False, 'message': 'Thiếu ID'}), 400

        # 1. Xóa trong danh sách sản phẩm tự tạo (custom_products.json)
        custom_products = load_json(CUSTOM_PRODUCT_FILE, [])
        # Chỉ giữ lại những thằng KHÔNG trùng ID
        new_products = [p for p in custom_products if str(p.get('id')) != p_id]
        save_json(CUSTOM_PRODUCT_FILE, new_products)

        # 2. (Tùy chọn) Xóa luôn giá ảo của nó trong custom_prices.json cho sạch
        custom_prices = load_json(CUSTOM_PRICE_FILE, {})
        if p_id in custom_prices:
            del custom_prices[p_id]
            save_json(CUSTOM_PRICE_FILE, custom_prices)

        print(f"--- Đã xóa sản phẩm ID: {p_id} ---")
        return jsonify({'success': True, 'message': 'Xóa thành công!'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
# app.py
# Bác dán đoạn này vào trên dòng 774 nhé
def get_khommo_data():
    # Dùng đúng TOKEN bác đã khai báo ở đầu file
    url = f"https://khommo.vn/api/products.php?api_key={KHOMMO_TOKEN}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            # In ra CMD để bác soi cho sướng
            data = response.json()
            print(f"--- ĐÃ LẤY ĐƯỢC {len(data)} SP TỪ KHOMMO ---")
            return data
        return []
    except Exception as e:
        print(f"Lỗi kết nối Khommo: {e}")
        return []
@app.route('/admin/khommo')
def admin_khommo_final_check():
    if session.get('role') != 'admin': 
        return redirect('/')
    
    api_items = get_khommo_data() 
    # Nếu api_items là dict và có key 'categories', ta lấy list đó
    categories = api_items.get('categories', []) if isinstance(api_items, dict) else api_items
    
    saved_prices = load_json('khommo_prices.json', {})
    api_products = []
    # categories lấy từ api_items.get('categories', [])
    for cat in categories:
        sub_products = cat.get('products', []) # Móc sản phẩm con ra
        
        for p in sub_products:
            p_id = str(p.get('id', ''))
            
            # Ép kiểu an toàn qua float trước khi sang int
            raw_price = p.get('price') or 0
            try:
                orig_price = int(float(raw_price))
            except:
                orig_price = 0
            
            sell_price = saved_prices.get(p_id, orig_price)
            
            api_products.append({
                "id": p_id,
                "name": p.get('name', 'Không tên'),
                "category": cat.get('name'), 
                "original_price": orig_price,
                "sell_price": sell_price
            })
    
    print(f"--- ĐÃ BÓC TÁCH THÀNH CÔNG: {len(api_products)} SẢN PHẨM ---")
    return render_template('admin_khommo.html', api_products=api_products)
# Bác phải có đúng đường dẫn này thì nút Lưu mới chạy được
@app.route('/api/admin/khommo/update-price', methods=['POST'])
def update_khommo_price():
    try:
        data = request.json
        product_id = str(data.get('id'))  # Chuyển ID về chuỗi để đồng nhất
        new_price = data.get('price')
        
        # 1. Đọc dữ liệu cũ từ file lên để tránh mất các giá đã lưu trước đó
        # Sử dụng hàm load_json bác đã có hoặc dùng logic dưới đây
        try:
            with open('khommo_prices.json', 'r', encoding='utf-8') as f:
                saved_prices = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            saved_prices = {}

        # 2. Cập nhật giá mới (Ép về kiểu số thực hoặc nguyên cho sạch)
        saved_prices[product_id] = int(float(new_price))
        
        # 3. GHI THẬT vào file (Đây là bước quan trọng nhất)
        with open('khommo_prices.json', 'w', encoding='utf-8') as f:
            json.dump(saved_prices, f, indent=4, ensure_ascii=False)
        
        print(f"--- Đã cập nhật ID {product_id} thành {new_price} VNĐ ---")
        return jsonify({"success": True, "message": "Lưu thành công!"})
        
    except Exception as e:
        print(f"Lỗi khi lưu giá: {str(e)}")
        return jsonify({"success": False, "message": str(e)})
@app.route('/interaction')
def interaction_page():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    users = load_users()
    user_data = next((u for u in users if u['username'] == session['user']), None)

    try:
        res = requests.post(
            "https://nganhangsub.vn/api/v2",
            data={
                "key": NGANHANGSUB_KEY,
                "action": "services"
            }
        )
        services = res.json()
    except:
        services = []

    # 🔥 fix null
    for s in services:
        s["rate"] = s.get("rate") or 0

    # 🔥 LOAD GIÁ ADMIN
    saved_prices = load_json("buff_prices.json", {})
    for s in services:
        s_id = str(s.get("service"))
        if s_id in saved_prices:
            s["rate"] = saved_prices[s_id]

    # 🔥 QUAN TRỌNG NHẤT (ÔNG THIẾU CHỖ NÀY)
    custom_services = load_json("custom_services.json", [])
    services = services + custom_services

    return render_template('interaction.html',
                           username=user_data['username'],
                           balance=user_data['balance'],
                           services=services)
@app.route('/history')
def history_page():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    users = load_users()
    user_data = next((u for u in users if u['username'] == session['user']), None)

    all_orders = load_json(ORDER_FILE, [])

    # 🔥 FIX QUAN TRỌNG
    user_orders = [o for o in all_orders if str(o.get('username')) == str(session['user'])]
    print("USER LOGIN:", session['user'])
    print("ORDERS:", all_orders[:2])
    return render_template('history.html',
                           username=user_data['username'],
                           balance=user_data['balance'],
                           orders=user_orders)
@app.route('/admin/mxh')
def admin_mxh():
    if session.get('role') != 'admin':
        return redirect(url_for('dashboard'))

    users = load_users()
    user_data = next((u for u in users if u['username'] == session['user']), None)

    # 🔥 gọi API
    try:
        res = requests.post(
            "https://nganhangsub.vn/api/v2",
            data={
                "key": NGANHANGSUB_KEY,
                "action": "services"
            }
        )
        services = res.json()
    except:
        services = []

    # 🔥 fix null
    for s in services:
        s["rate"] = s.get("rate") or 0

    # 🔥 load giá custom
    saved_prices = load_json("buff_prices.json", {})

    # 🔥 áp giá đã sửa
    for s in services:
        s_id = str(s.get("service"))
        if s_id in saved_prices:
            s["rate"] = saved_prices[s_id]
    custom_services = load_json("custom_services.json", [])
    services = services + custom_services
    return render_template("admin_mxh.html",
                           services=services,
                           balance=user_data['balance'],
                           username=user_data['username'])
@app.route('/api/admin/edit-price', methods=['POST'])
def edit_price():
    try:
        data = request.get_json()
        print("🔥 DATA NHẬN:", data)

        service_id = str(data.get('id'))

        # 🔥 FIX Ở ĐÂY
        price_raw = data.get('price') or data.get('rate')

        if not price_raw:
            return jsonify({'success': False, 'message': 'Thiếu giá'}), 400

        new_price = int(float(price_raw))

        prices = load_json("buff_prices.json", {})
        prices[service_id] = new_price
        save_json("buff_prices.json", prices)

        return jsonify({'success': True})

    except Exception as e:
        print("Lỗi lưu giá:", e)
        return jsonify({'success': False}), 500
@app.route('/api/admin/add-service', methods=['POST'])
def add_service():
    try:
        data = request.get_json()
        print("DATA ADD:", data)

        service_id = str(data.get('id'))
        name = data.get('name')
        category = data.get('category')
        price = int(float(data.get('price') or 0))

        if not service_id or not name:
            return jsonify({'success': False, 'message': 'Thiếu dữ liệu'}), 400

        services = load_json("custom_services.json", [])

        services.append({
            "service": service_id,
            "name": name,
            "category": category,
            "rate": price
        })

        save_json("custom_services.json", services)

        return jsonify({'success': True})

    except Exception as e:
        print("Lỗi add:", e)
        return jsonify({'success': False, 'message': str(e)}), 500
@app.route('/api/admin/update-order', methods=['POST'])
def update_order():
    if session.get('role') != 'admin':
        return jsonify({'success': False, 'message': 'Không có quyền'}), 403

    data = request.get_json()
    index = data.get('index')
    new_status = data.get('status')

    orders = load_json(ORDER_FILE, [])

    try:
        index = int(index)
        orders[index]['status'] = new_status
        save_json(ORDER_FILE, orders)

        return jsonify({'success': True, 'message': 'Đã cập nhật trạng thái'})
    except:
        return jsonify({'success': False, 'message': 'Lỗi update'})
@app.route('/api/admin/delete-service', methods=['POST'])
def admin_delete_service():
    if session.get('role') != 'admin': 
        return jsonify({'success': False, 'message': 'Không có quyền!'}), 403
    
    data = request.get_json()
    # Ép kiểu về string để so sánh cho chuẩn (tránh lỗi 123 != "123")
    target_id = str(data.get('id'))

    # Danh sách các file cần quét và xóa sạch ID này
    files_to_clean = [
        CUSTOM_PRODUCT_FILE,   # custom_products.json
        'custom_services.json',
        CUSTOM_PRICE_FILE      # custom_prices.json
    ]

    for filename in files_to_clean:
        if os.path.exists(filename):
            data_list = load_json(filename, [])
            
            if isinstance(data_list, list):
                # Xóa nếu ID nằm trong danh sách (list)
                # Check cả field 'id' và 'service' vì code ông dùng cả 2 tên
                new_data = [
                    item for item in data_list 
                    if str(item.get('id')) != target_id and str(item.get('service')) != target_id
                ]
                save_json(filename, new_data)
                
            elif isinstance(data_list, dict):
                # Xóa nếu ID là Key trong Dictionary (như file custom_prices)
                if target_id in data_list:
                    del data_list[target_id]
                    save_json(filename, data_list)

    print(f"--- ĐÃ XÓA TRIỆT ĐỂ ID: {target_id} ---")
    return jsonify({'success': True, 'message': 'Xóa sạch sẽ!'})
if __name__ == '__main__':
    # host='0.0.0.0' giúp các thiết bị khác (điện thoại) thấy được máy tính của ông
    app.run(host='0.0.0.0', port=5000, debug=True)
