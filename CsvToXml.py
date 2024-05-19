import csv
import os

# Fungsi untuk membaca data dari file CSV
def baca_data_csv(nama_file):
    data = []
    try:
        with open(nama_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        print(f"Error: File '{nama_file}' tidak ditemukan.")
    except Exception as e:
        print(f"Error saat membaca file CSV: {e}")
    return data

# Fungsi untuk membuat template AIML dari data dan pola pertanyaan
def buat_template_aiml(data):
    templates = ""
    for item in data:
        try:
            jenis_hardware = item['Nama']
            harga = item['Harga']
            templates += f'''
            <category>
              <pattern>{jenis_hardware}</pattern>
              <template>Harga {jenis_hardware} saat ini sekitar {harga}.</template>
            </category>
            <category>
              <pattern>* {jenis_hardware}</pattern>
              <template>Harga {jenis_hardware} saat ini sekitar {harga}.</template>
            </category>
            <category>
              <pattern>{jenis_hardware} *</pattern>
              <template>Harga {jenis_hardware} saat ini sekitar {harga}.</template>
            </category>
            <category>
              <pattern>* {jenis_hardware} *</pattern>
              <template>Harga {jenis_hardware} saat ini sekitar {harga}.</template>
            </category>
            '''
        except KeyError as e:
            print(f"Error: Kolom {e} tidak ditemukan dalam data.")
        except Exception as e:
            print(f"Error saat membuat template AIML: {e}")
    return templates

# Nama file CSV dan direktori sumber
nama_file_csv = 'DsProc.csv'
direktori_sumber = 'Dataset csv'

# Path lengkap ke file CSV
path_file_csv = os.path.join(direktori_sumber, nama_file_csv)

# Baca data dari file CSV
data_hardware = baca_data_csv(path_file_csv)

if data_hardware:  # Lanjutkan jika data berhasil dibaca
    # Buat template AIML dari data
    template_aiml = buat_template_aiml(data_hardware)

    # Nama file AIML dan direktori tujuan
    nama_file_aiml = 'proc.xml'
    direktori_tujuan = 'Dataset xml'

    # Pastikan direktori tujuan ada
    if not os.path.exists(direktori_tujuan):
        os.makedirs(direktori_tujuan)

    # Simpan template AIML ke dalam file di direktori tujuan
    path_file_aiml = os.path.join(direktori_tujuan, nama_file_aiml)
    try:
        with open(path_file_aiml, 'w') as file:
            file.write('<aiml version="2.0">\n')
            file.write(template_aiml)
            file.write('</aiml>')
        print("Template AIML telah berhasil dibuat dan disimpan dalam folder:", path_file_aiml)
    except Exception as e:
        print(f"Error saat menyimpan file AIML: {e}")
else:
    print("Tidak ada data yang dibaca dari file CSV.")
