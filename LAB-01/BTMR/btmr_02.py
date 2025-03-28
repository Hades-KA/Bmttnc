import re  # Thư viện hỗ trợ xử lý biểu thức chính quy (regex)

# Bước 1: Nhập chuỗi cần xử lý
chuoi = input("Nhập chuỗi cần xử lý: ")

# Bước 2: Tìm tất cả các số nguyên trong chuỗi, bao gồm cả số âm
so_nguyen = re.findall(r'-?\d+', chuoi)

# Bước 3: Khởi tạo biến để tính tổng
tong_duong = 0
tong_am = 0

# Bước 4: Duyệt qua từng số trong danh sách, chuyển về số nguyên và tính tổng
for so in so_nguyen:
    so = int(so)  # Chuyển từ chuỗi sang số nguyên
    if so >= 0:
        tong_duong += so
    else:
        tong_am += so
        
# Bước 5: In kết quả
print("Giá trị dương:", tong_duong)
print("Giá trị âm:", tong_am)