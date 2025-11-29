import re
import json
from translator import translate, translate_date_to_japanese, translate_citizenship

def filter_after_separator(input_list):
    # Pattern: matches strings like "(4)", "( 4 )", etc.
    pattern = re.compile(r'^\s*\(\s*\d{1,2}\s*\)\s*$')
    
    for i, item in enumerate(input_list):
        if pattern.match(item):
            return input_list[i+1:]
    
    # If no separator found, return original list
    return input_list

def extract_date(s: str) -> str:
    # Match formats like d-m-yyyy, dd-mm-yyyy, d.m.yyyy, dd.mm.yyyy
    match = re.search(r'\b\d{1,2}[-.]\d{1,2}[-.]\d{4}\b', s)
    return match.group(0) if match else ''

def preprocess_string(s, unwanted_chars="/-.,"):
    # 1. Remove unwanted characters dynamically using a character class
    pattern = f"[{re.escape(unwanted_chars)}]"
    s = re.sub(pattern, '', s)
    # 2. Replace multiple spaces with a single space
    s = re.sub(r'\s+', ' ', s)
    # 3. Strip leading and trailing spaces
    s = s.strip()
    return "" if len(s) <= 1 else s
    
def keep_only_numbers(s: str) -> str:
    return re.sub(r'\D', '', s)  # \D = any non-digit character

def keep_only_numbers_and_slash(s: str) -> str:
    return re.sub(r'[^0-9/-]', '', s)  # keep only digits and /

def keep_only_numbers_and_dash(s: str) -> str:
    return re.sub(r'[^0-9-]', '', s)  # keep only digits and -
class FamilyData:
    def __init__(self, data: dict):
        # Dynamically set attributes for each key in the data
        for key, value in data.items():
            setattr(self, key, value)

    @classmethod
    def from_json_file(cls, filepath: str) -> 'FamilyData':
        """Load data from a JSON file and return a FamilyData instance"""
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return cls(data)

    def to_dict(self):
        return self.__dict__

    def save_to_json(self, filename: str):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=4, ensure_ascii=False)

    def print_all(self):
        """Print all attributes (excluding methods and built-ins)"""
        for key in self.__dict__:
            print(f"{key}: {getattr(self, key)}")

    def preprocess_no_kk(self):
        self.no = keep_only_numbers(self.no)
    
    def preprocess_kepala_keluarga(self):
        self.keluarga = preprocess_string(self.keluarga, "!/-,1234567890")
        self.kep_keluarga = self.keluarga
    
    def preprocess_alamat(self):
        self.alamat = preprocess_string(self.alamat, "!/-,1234567890")

    def preprocess_rw(self):
        self.rw = keep_only_numbers_and_slash(self.rw)

    def preprocess_pos(self):
        self.pos = keep_only_numbers(self.pos)

    def preprocess_kelurahan(self):
        self.kelurahan = preprocess_string(self.kelurahan, "!/-,1234567890")

    def preprocess_kecamatan(self):
        self.kecamatan= preprocess_string(self.kecamatan, "!/-,1234567890")
    
    def preprocess_kota(self):
        self.kota = preprocess_string(self.kota, "!/-,1234567890")

    def preprocess_provinsi(self):
        self.provinsi = preprocess_string(self.provinsi, "!/-,1234567890")
    
    def preprocess_names(self):
        self.names = filter_after_separator(self.names)
        self.names = [preprocess_string(name, "!/-,1234567890") for name in self.names]
    
    def preprocess_nik(self):
        self.niks = filter_after_separator(self.niks)
        self.niks = [keep_only_numbers(nik) for nik in self.niks]

    def preprocess_sexes(self):
        self.sexes = filter_after_separator(self.sexes)
        self.sexes = [preprocess_string(sex, "!/-,1234567890") for sex in self.sexes]
        self.sexes = [translate(item) for item in self.sexes]

    def preprocess_birthplaces(self):
        self.birthplaces = filter_after_separator(self.birthplaces)
        self.birthplaces = [preprocess_string(birthplace, "!/-,1234567890") for birthplace in self.birthplaces]

    def preprocess_birthdates(self):
        self.birthdates = filter_after_separator(self.birthdates) 
        self.birthdates = [extract_date(birthdate) for birthdate in self.birthdates]

    def preprocess_religions(self):
        self.religions = filter_after_separator(self.religions)
        self.religions = [preprocess_string(religion, "!/-,1234567890") for religion in self.religions]
        self.religions = [translate(item) for item in self.religions]

    def preprocess_educations(self):
        self.educations = filter_after_separator(self.educations)
        self.educations = [preprocess_string(education, "!-,1234567890") for education in self.educations]
        self.educations = [translate(item) for item in self.educations]

    def preprocess_profession(self):
        self.profession = filter_after_separator(self.profession)
        self.profession = [preprocess_string(p, "!-,1234567890") for p in self.profession]
        self.profession = [translate(item) for item in self.profession]

    def preprocess_marriage_stats(self):
        self.marriage_stats = filter_after_separator(self.marriage_stats)
        self.marriage_stats = [preprocess_string(item, "!/-,1234567890") for item in self.marriage_stats]
        self.marriage_stats = [translate(item) for item in self.marriage_stats]

    def preprocess_marriage_dates(self):
        self.marriage_dates = filter_after_separator(self.marriage_dates)
        self.marriage_dates = [extract_date(item) for item in self.marriage_dates]
        self.marriage_dates = [translate_date_to_japanese(item) for item in self.marriage_dates]
        
    def preprocess_marriage_rels(self):
        self.marriage_rels = filter_after_separator(self.marriage_rels)
        self.marriage_rels = [preprocess_string(item, "!/-,1234567890") for item in self.marriage_rels]
        self.marriage_rels = [translate(item) for item in self.marriage_rels]

    def preprocess_citizenships(self):
        self.citizenships = filter_after_separator(self.citizenships)
        self.citizenships = [preprocess_string(item, "!/-,1234567890") for item in self.citizenships]
        self.citizenships = [translate_citizenship(item) for item in self.citizenships]

    def preprocess_paspor_no(self):
        self.paspor_no = filter_after_separator(self.paspor_no)
        self.paspor_no = [preprocess_string(item, "!/-,") for item in self.paspor_no]

    def preprocess_kitas_no(self):
        self.kitas_no = filter_after_separator(self.kitas_no)
        self.kitas_no = [preprocess_string(item, "!/-,") for item in self.kitas_no]

    def preprocess_father_names(self):
        self.father_names = filter_after_separator(self.father_names)
        self.father_names = [preprocess_string(item, "!/-,1234567890") for item in self.father_names]
    
    def preprocess_mother_names(self):
        self.mother_names = filter_after_separator(self.mother_names)
        self.mother_names = [preprocess_string(item, "!/-,1234567890") for item in self.mother_names]

    def preprocess_tanggal(self):
        self.tanggal = extract_date(self.tanggal)

    def preprocess_nip(self):
        self.nip = keep_only_numbers(self.nip)

    def preprocess_officer_name(self):
        self.officer_name = preprocess_string(self.officer_name, "/-1234567890")

    def preprocess(self, output_path):
        self.preprocess_no_kk()
        self.preprocess_kepala_keluarga()
        self.preprocess_alamat()
        self.preprocess_rw()
        self.preprocess_pos()
        self.preprocess_kelurahan()
        self.preprocess_kecamatan()
        self.preprocess_kota()
        self.preprocess_provinsi()
        self.preprocess_names()
        self.preprocess_nik()
        self.preprocess_sexes()
        self.preprocess_birthplaces()
        self.preprocess_birthdates()
        self.preprocess_religions()
        self.preprocess_educations()
        self.preprocess_profession()
        self.preprocess_marriage_stats()
        self.preprocess_marriage_dates()
        self.preprocess_marriage_rels()
        self.preprocess_citizenships()
        self.preprocess_paspor_no()
        self.preprocess_kitas_no()
        self.preprocess_father_names()
        self.preprocess_mother_names()
        self.preprocess_tanggal()
        self.preprocess_nip()
        self.preprocess_officer_name()
        self.save_to_json(output_path)
        self.print_all()