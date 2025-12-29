# Thông tin 63 tỉnh thành Việt Nam với tọa độ chính xác
# Mỗi profile sẽ được map với 1 tỉnh để mô phỏng người dùng từ các tỉnh khác nhau

VIETNAM_PROVINCES = [
    {"id": 1, "name": "Hà Nội", "latitude": 21.0285, "longitude": 105.8542},
    {"id": 2, "name": "Hồ Chí Minh", "latitude": 10.8231, "longitude": 106.6297},
    {"id": 3, "name": "Đà Nẵng", "latitude": 16.0544, "longitude": 108.2022},
    {"id": 4, "name": "Hải Phòng", "latitude": 20.8449, "longitude": 106.6881},
    {"id": 5, "name": "Cần Thơ", "latitude": 10.0452, "longitude": 105.7469},
    {"id": 6, "name": "An Giang", "latitude": 10.5215, "longitude": 105.1258},
    {"id": 7, "name": "Bà Rịa - Vũng Tàu", "latitude": 10.5417, "longitude": 107.2429},
    {"id": 8, "name": "Bắc Giang", "latitude": 21.2819, "longitude": 106.1975},
    {"id": 9, "name": "Bắc Kạn", "latitude": 22.1471, "longitude": 105.8348},
    {"id": 10, "name": "Bạc Liêu", "latitude": 9.2940, "longitude": 105.7215},
    {"id": 11, "name": "Bắc Ninh", "latitude": 21.1861, "longitude": 106.0763},
    {"id": 12, "name": "Bến Tre", "latitude": 10.2433, "longitude": 106.3757},
    {"id": 13, "name": "Bình Định", "latitude": 13.7830, "longitude": 109.2196},
    {"id": 14, "name": "Bình Dương", "latitude": 11.3254, "longitude": 106.4770},
    {"id": 15, "name": "Bình Phước", "latitude": 11.7511, "longitude": 106.7234},
    {"id": 16, "name": "Bình Thuận", "latitude": 10.9287, "longitude": 108.0972},
    {"id": 17, "name": "Cà Mau", "latitude": 9.1527, "longitude": 105.1960},
    {"id": 18, "name": "Cao Bằng", "latitude": 22.6356, "longitude": 106.2522},
    {"id": 19, "name": "Đắk Lắk", "latitude": 12.7100, "longitude": 108.2378},
    {"id": 20, "name": "Đắk Nông", "latitude": 12.2646, "longitude": 107.6098},
    {"id": 21, "name": "Điện Biên", "latitude": 21.8042, "longitude": 103.1076},
    {"id": 22, "name": "Đồng Nai", "latitude": 10.9467, "longitude": 106.8340},
    {"id": 23, "name": "Đồng Tháp", "latitude": 10.4938, "longitude": 105.6881},
    {"id": 24, "name": "Gia Lai", "latitude": 13.8078, "longitude": 108.1094},
    {"id": 25, "name": "Hà Giang", "latitude": 22.8025, "longitude": 104.9784},
    {"id": 26, "name": "Hà Nam", "latitude": 20.5835, "longitude": 105.9230},
    {"id": 27, "name": "Hà Tĩnh", "latitude": 18.3559, "longitude": 105.8878},
    {"id": 28, "name": "Hải Dương", "latitude": 20.9373, "longitude": 106.3145},
    {"id": 29, "name": "Hậu Giang", "latitude": 9.7579, "longitude": 105.6412},
    {"id": 30, "name": "Hòa Bình", "latitude": 20.6861, "longitude": 105.3131},
    {"id": 31, "name": "Hưng Yên", "latitude": 20.6464, "longitude": 106.0511},
    {"id": 32, "name": "Khánh Hòa", "latitude": 12.2585, "longitude": 109.0526},
    {"id": 33, "name": "Kiên Giang", "latitude": 10.0125, "longitude": 105.0810},
    {"id": 34, "name": "Kon Tum", "latitude": 14.3497, "longitude": 108.0005},
    {"id": 35, "name": "Lai Châu", "latitude": 22.3864, "longitude": 103.4702},
    {"id": 36, "name": "Lâm Đồng", "latitude": 11.5753, "longitude": 108.1429},
    {"id": 37, "name": "Lạng Sơn", "latitude": 21.8537, "longitude": 106.7612},
    {"id": 38, "name": "Lào Cai", "latitude": 22.4809, "longitude": 103.9755},
    {"id": 39, "name": "Long An", "latitude": 10.6956, "longitude": 106.4115},
    {"id": 40, "name": "Nam Định", "latitude": 20.4388, "longitude": 106.1621},
    {"id": 41, "name": "Nghệ An", "latitude": 19.2342, "longitude": 104.9200},
    {"id": 42, "name": "Ninh Bình", "latitude": 20.2506, "longitude": 105.9745},
    {"id": 43, "name": "Ninh Thuận", "latitude": 11.6739, "longitude": 108.8629},
    {"id": 44, "name": "Phú Thọ", "latitude": 21.2680, "longitude": 105.2045},
    {"id": 45, "name": "Phú Yên", "latitude": 13.0881, "longitude": 109.0929},
    {"id": 46, "name": "Quảng Bình", "latitude": 17.6102, "longitude": 106.3487},
    {"id": 47, "name": "Quảng Nam", "latitude": 15.5394, "longitude": 108.0192},
    {"id": 48, "name": "Quảng Ngãi", "latitude": 15.1214, "longitude": 108.8044},
    {"id": 49, "name": "Quảng Ninh", "latitude": 21.0064, "longitude": 107.2925},
    {"id": 50, "name": "Quảng Trị", "latitude": 16.7943, "longitude": 107.1856},
    {"id": 51, "name": "Sóc Trăng", "latitude": 9.6037, "longitude": 105.9739},
    {"id": 52, "name": "Sơn La", "latitude": 21.1022, "longitude": 103.7289},
    {"id": 53, "name": "Tây Ninh", "latitude": 11.3351, "longitude": 106.1098},
    {"id": 54, "name": "Thái Bình", "latitude": 20.4463, "longitude": 106.3365},
    {"id": 55, "name": "Thái Nguyên", "latitude": 21.5671, "longitude": 105.8252},
    {"id": 56, "name": "Thanh Hóa", "latitude": 19.8067, "longitude": 105.7851},
    {"id": 57, "name": "Thừa Thiên Huế", "latitude": 16.4637, "longitude": 107.5909},
    {"id": 58, "name": "Tiền Giang", "latitude": 10.4493, "longitude": 106.3420},
    {"id": 59, "name": "Trà Vinh", "latitude": 9.8127, "longitude": 106.2992},
    {"id": 60, "name": "Tuyên Quang", "latitude": 21.7767, "longitude": 105.2280},
    {"id": 61, "name": "Vĩnh Long", "latitude": 10.2395, "longitude": 105.9571},
    {"id": 62, "name": "Vĩnh Phúc", "latitude": 21.3609, "longitude": 105.5474},
    {"id": 63, "name": "Yên Bái", "latitude": 21.7168, "longitude": 104.8986},
]


def get_province_by_id(province_id: int):
    """Lấy thông tin tỉnh theo ID"""
    for province in VIETNAM_PROVINCES:
        if province["id"] == province_id:
            return province
    return VIETNAM_PROVINCES[0]  # Default: Hà Nội


def get_province_by_profile_number(profile_number: int):
    """
    Map profile number (1-63) với province ID
    profile_1 -> tỉnh 1, profile_2 -> tỉnh 2, ...
    """
    province_id = ((profile_number - 1) % 63) + 1
    return get_province_by_id(province_id)
