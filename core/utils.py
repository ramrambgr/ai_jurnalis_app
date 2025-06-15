import PyPDF2
import docx
# from PIL import ExifTags
# from PIL.Image import Image as PILImage
from PIL import Image as PILImage, ExifTags
import piexif

# def dms_to_decimal(dms, ref):
#     try:
#         degrees = dms[0][0] / dms[0][1]
#         minutes = dms[1][0] / dms[1][1]
#         seconds = dms[2][0] / dms[2][1]
#         decimal = degrees + (minutes / 60) + (seconds / 3600)
#         if ref in ["S", "W"]:
#             decimal *= -1
#         return round(decimal, 6)
#     except Exception:
#         return None

# def extract_exif_data(image: PILImage):
#     exif_data = {}
#     try:
#         raw_exif = image.getexif()
#         if not raw_exif:
#             return {"Info": "Tidak ada metadata EXIF."}

#         # Konversi tag integer ke nama yang bisa dibaca
#         exif = {
#             ExifTags.TAGS.get(tag, tag): value
#             for tag, value in raw_exif.items()
#             if tag in ExifTags.TAGS
#         }

#         # Tanggal dan Kamera
#         exif_data["Tanggal"] = (
#             exif.get("DateTimeOriginal")
#             or exif.get("DateTimeDigitized")
#             or exif.get("DateTime")
#             or "Tidak tersedia"
#         )
#         exif_data["Kamera"] = exif.get("Model", "Tidak tersedia")

#         # GPS Info: akses aman
#         gps_info_tag = [tag for tag, name in ExifTags.TAGS.items() if name == "GPSInfo"]
#         gps_info_raw = raw_exif.get(gps_info_tag[0]) if gps_info_tag else None

#         if isinstance(gps_info_raw, dict):
#             gps_data = {
#                 ExifTags.GPSTAGS.get(k, k): v
#                 for k, v in gps_info_raw.items()
#             }

#             lat = gps_data.get("GPSLatitude")
#             lat_ref = gps_data.get("GPSLatitudeRef")
#             lon = gps_data.get("GPSLongitude")
#             lon_ref = gps_data.get("GPSLongitudeRef")

#             if lat and lat_ref and lon and lon_ref:
#                 lat_decimal = dms_to_decimal(lat, lat_ref)
#                 lon_decimal = dms_to_decimal(lon, lon_ref)
#                 if lat_decimal is not None and lon_decimal is not None:
#                     exif_data["Koordinat"] = {
#                         "Latitude": lat_decimal,
#                         "Longitude": lon_decimal,
#                         "Google Maps": f"https://www.google.com/maps?q={lat_decimal},{lon_decimal}"
#                     }
#                 else:
#                     exif_data["Koordinat"] = "Data GPS tidak valid"
#             else:
#                 exif_data["Koordinat"] = "Data GPS tidak lengkap"
#         else:
#             exif_data["Koordinat"] = "Tidak tersedia atau format GPSInfo tidak dikenali"

#     except Exception as e:
#         exif_data["Error"] = f"Gagal membaca EXIF: {str(e)}"

#     return exif_data

def convert_to_degrees(value):
    try:
        d, m, s = value
        return d[0] / d[1] + m[0] / m[1] / 60 + s[0] / s[1] / 3600
    except:
        return None

def dms_to_decimal(dms, ref):
    decimal = convert_to_degrees(dms)
    if decimal is not None:
        if ref in ['S', 'W']:
            decimal = -decimal
    return decimal

# Fungsi tambahan untuk membaca GPS dengan piexif (fallback)
def get_gps_piexif(image: PILImage.Image):
    try:
        exif_data = piexif.load(image.info['exif'])
        gps_data = exif_data.get("GPS", {})
        if not gps_data:
            return None

        lat = convert_to_degrees(gps_data[piexif.GPSIFD.GPSLatitude])
        lat_ref = gps_data[piexif.GPSIFD.GPSLatitudeRef].decode()
        if lat_ref != "N":
            lat = -lat

        lon = convert_to_degrees(gps_data[piexif.GPSIFD.GPSLongitude])
        lon_ref = gps_data[piexif.GPSIFD.GPSLongitudeRef].decode()
        if lon_ref != "E":
            lon = -lon

        return lat, lon
    except:
        return None

# Fungsi untuk mengambil data EXIF (termasuk GPS)
def extract_exif_data(image: PILImage.Image):
    exif_data = {}
    try:
        raw_exif = image.getexif()
        if not raw_exif:
            return {"Info": "Tidak ada metadata EXIF."}

        # Konversi tag integer ke nama yang lebih dapat dibaca
        exif = {
            ExifTags.TAGS.get(tag, tag): value
            for tag, value in raw_exif.items()
            if tag in ExifTags.TAGS
        }

        # Ambil Tanggal dan Kamera
        exif_data["Tanggal"] = (
            exif.get("DateTimeOriginal")
            or exif.get("DateTimeDigitized")
            or exif.get("DateTime")
            or "Tidak tersedia"
        )
        exif_data["Kamera"] = exif.get("Model", "Tidak tersedia")

        # Menangani GPS Info dengan fallback
        gps_info_tag = [k for k, v in ExifTags.TAGS.items() if v == "GPSInfo"]
        gps_info_raw = raw_exif.get(gps_info_tag[0]) if gps_info_tag else None

        if gps_info_raw and isinstance(gps_info_raw, dict):
            gps_data = {
                ExifTags.GPSTAGS.get(k, k): v
                for k, v in gps_info_raw.items()
            }

            lat = gps_data.get("GPSLatitude")
            lat_ref = gps_data.get("GPSLatitudeRef")
            lon = gps_data.get("GPSLongitude")
            lon_ref = gps_data.get("GPSLongitudeRef")

            if lat and lat_ref and lon and lon_ref:
                lat_decimal = dms_to_decimal(lat, lat_ref)
                lon_decimal = dms_to_decimal(lon, lon_ref)

                if lat_decimal is not None and lon_decimal is not None:
                    exif_data["Koordinat"] = {
                        "Latitude": lat_decimal,
                        "Longitude": lon_decimal,
                        "Google Maps": f"https://www.google.com/maps?q={lat_decimal},{lon_decimal}"
                    }
                else:
                    exif_data["Koordinat"] = "Data GPS tidak valid"
            else:
                exif_data["Koordinat"] = "Data GPS tidak lengkap"
        else:
            # Fallback ke piexif jika GPSInfo tidak ditemukan dalam EXIF
            gps = get_gps_piexif(image)
            if gps:
                exif_data["Koordinat"] = {
                    "Latitude": gps[0],
                    "Longitude": gps[1],
                    "Google Maps": f"https://www.google.com/maps?q={gps[0]},{gps[1]}"
                }
            else:
                exif_data["Koordinat"] = "Tidak tersedia atau format GPSInfo tidak dikenali"

    except Exception as e:
        exif_data["Error"] = f"Gagal membaca EXIF: {str(e)}"

    return exif_data
    
def read_reference_file(ref_file):
    if not ref_file:
        return None
    try:
        if ref_file.name.endswith(".txt"):
            return ref_file.read().decode("utf-8")
        elif ref_file.name.endswith(".docx"):
            doc = docx.Document(ref_file)
            return "\n".join([p.text for p in doc.paragraphs])
        elif ref_file.name.endswith(".pdf"):
            reader = PyPDF2.PdfReader(ref_file)
            return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    except Exception as e:
        return f"❌ Gagal membaca file referensi: {e}"
    return None
