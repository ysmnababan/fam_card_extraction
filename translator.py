import re  
from datetime import datetime

translation_mapping = {
    "laki laki": "男性",
    "pria": "男性",
    "perempuan": "女性",
    "wanita": "女性",
    "islam": "イスラム教",
    "kristen": "キリスト教",
    "katolik": "カトリック",
    "hindu": "ヒンドゥー教",
    "buddha": "仏教",
    "belum kawin": "未婚",
    "kawin tercatat": "既婚",
    "kawin": "既婚",
    "cerai hidup": "離婚",
    "cerai mati": "死別",
    "pelajar/mahasiswa": "学生",
    "pelajar" :"学生",
    "mahasiswa" :"学生",
    "belum/tidak bekerja": "未就労",
    "belum bekerja": "未就労",
    "tidak bekerja": "未就労",
    "mengurus rumah tangga": "家事",
    "pensiunan": "定年",
    "pegawai negeri sipil": "公務員",
    "pns": "公務員",
    "tni": "軍人",
    "petani/pekebun": "農家",
    "petani": "農家",
    "pekebun": "農家",
    "peternak": "畜産",
    "karyawan swasta": "会社員",
    "buruh harian lepas": "アルバイト",
    "buruh tani/perkebunan": "農民",
    "pembantu rumah tangga": "家事手伝い",
    "tukang cukur": "理容師",
    "tukang listrik": "電気技師",
    "tukang batu": "石工",
    "tukang kayu": "大工",
    "wartawan": "記者",
    "ustadz/mubaligh": "牧師",
    "guru": "教師",
    "sopir": "運転手",
    "pedagang": "商人",
    "perangkat desa": "役人",
    "kepala desa": "村長",
    "wiraswasta": "自営業",
    "tidak/belum sekolah": "学歴なし",
    "belum tamat sd": "小学校未卒",
    "belum tamat sd/sederajat": "小学校未卒",
    "tamat sd/sederajat": "小学校卒業",
    "sltp/sederajat": "中学校卒業",
    "slta/sederajat": "高校卒業",
    "diploma i/ii": "短大",
    "akademi/diploma iii/sarjana muda": "専門学校",
    "diploma iv/strata i": "大学",
    "strata iii": "博士課程",
    "strata ii": "大学院",
    "kepala keluarga": "家長",
    "suami": "夫",
    "istri": "妻",
    "isteri": "妻",
    "anak": "子",
    "menantu": "義理の子",
    "cucu": "孫",
    "orangtua": "両親",
    "mertua": "義理の親",
    "famili lain": "他の家族",
    "pembantu": "使用人",
    "lainnya": "その他",
    "indonesia":"インドネシア",
    "wn":"インドネシア",
    "wni":"インドネシア",
}



def normalize_text(text):
    # Remove spaces around slashes for consistency (e.g., 'slta / sederajat' to 'slta/sederajat')
    return re.sub(r'\s*/\s*', '/', text.lower())

def translate(text):
    normalized_text = normalize_text(text)

    for key, translation in translation_mapping.items():
        if key in normalized_text:
            return translation  # Return the first matching translation
    
    return text  # If no match, return original

def translate_date_to_japanese(date_str):
    # Parse the date assuming it's in DD-MM-YYYY format
    date_obj = datetime.strptime(date_str, "%d-%m-%Y")
    
    # Format it as 'YYYY年 M月 D日' with tabs between
    return f"{date_obj.year}年 {date_obj.month}月 {date_obj.day}日"