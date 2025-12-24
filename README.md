# PythonQR

Một webapp nhỏ bằng Python để tạo QR Code động từ chuỗi dữ liệu truyền vào.

**Tính năng chính**
- Giao diện web đơn giản để nhập dữ liệu và kích thước.
- API `GET /generate` trả về ảnh PNG của QR code.
- Cấu hình qua `config.cfg` (cổng, kích thước mặc định, v.v.).

**Yêu cầu**
- Python 3.10+ (hoặc 3.8+ nên hoạt động)
- Thư viện: `Flask`, `qrcode`, `Pillow`

**Cài đặt nhanh**
1. Tạo và kích hoạt virtual environment (tùy OS):

```bash
python -m venv .venv
source .venv/bin/activate  # Linux / macOS
# .venv\Scripts\activate   # Windows (PowerShell/CMD)
```

2. Cài dependencies:

```bash
pip install Flask qrcode pillow
```

3. Kiểm tra `config.cfg` để tùy chỉnh: `DEFAULT_PORT`, `DEFAULT_SIZE`, `DEFAULT_BORDER`, `DEFAULT_DATA`, `DEBUG`.

**Chạy ứng dụng**

```bash
python QRcode.py
```

Mở trình duyệt tới `http://localhost:8989/` (hoặc cổng bạn cấu hình trong `config.cfg`).

**API**
- `GET /generate?data=<text>&size=<px>&border=<n>`
	- `data` (string): dữ liệu cho QR (URL hoặc chuỗi bất kỳ). Nếu không cung cấp sẽ dùng `DEFAULT_DATA`.
	- `size` (int): kích thước ảnh PNG theo pixel (mặc định từ `config.cfg`).
	- `border` (int): kích thước đường viền QR (mặc định từ `config.cfg`).

Ví dụ:

```bash
curl "http://localhost:8989/generate?data=https://example.com&size=300&border=1" --output qrcode.png
```

**Tệp cấu hình**
- `config.cfg` chứa các hằng số mặc định. Ví dụ hiện tại:

```
DEFAULT_DATA = "tranlammankg"
DEFAULT_SIZE = 300
DEFAULT_BORDER = 1
DEFAULT_PORT = 8989
DEBUG = True
```

**Giao diện web**
- `index.html` là giao diện client đơn giản dùng JavaScript `fetch` gọi endpoint `/generate` và hiển thị ảnh trả về.

**Ghi chú phát triển**
- File `test.py` hiện trống.
- Logging được ghi vào tệp `app_YYYY-MM-DD.log` (cấu hình trong `QRcode.py`).

**Muốn đóng gói (optional)**
- Nếu muốn đóng gói thành executable, dùng `pyinstaller` hoặc công cụ tương tự; đảm bảo copy `config.cfg` và template `index.html` vào bundle.

Nếu bạn muốn, tôi có thể: cập nhật `requirements.txt`, thêm script chạy, hoặc viết hướng dẫn đóng gói thành Docker image.

**Script chạy nhanh**
- `run.sh`: script shell nhỏ tạo virtualenv (nếu chưa có), cài dependencies từ `requirements.txt` và chạy `QRcode.py`.

Chạy script trên Linux/macOS:
```bash
chmod +x run.sh
./run.sh
```

**Docker**
1. Xây image Docker:

```bash
docker build -t pythonqr:latest .
```

2. Chạy container (map cổng 8989):

```bash
docker run -p 8989:8989 --rm pythonqr:latest
```

Ghi chú: `Dockerfile` sử dụng `gunicorn` để phục vụ ứng dụng; `config.cfg` và `index.html` được sao chép vào image nên các cấu hình mặc định sẽ được giữ. Nếu muốn chỉnh port qua biến môi trường, bạn có thể sửa `config.cfg` hoặc thay `CMD` trong Dockerfile.