so_gio_lam = float(input("Nhập số giờ làm mỗi tuần của nhà ngươi: "))
luong_gio = float(input("Nhập lương trên mỗi giờ tiêu chuẩn của ngươi đi: "))
gio_tieu_chuan = 44
gio_vuot_chuan = max(0, so_gio_lam - gio_tieu_chuan)
thuc_linh = gio_tieu_chuan*luong_gio + gio_vuot_chuan*luong_gio*1.5
print(f"Tổng tiền lươn thực tế mà nhà ngươi được lĩnh là: {thuc_linh}")
