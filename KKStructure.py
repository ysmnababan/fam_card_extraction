from dataclasses import dataclass, field, asdict
import json
import TableScanner as ts 
import ImageProcessor as ip

FULL_NAME_COLUMN_IMAGE_FILE_NAME = "column_1.png"
NIK_COLUMN_IMAGE_FILE_NAME = "column_2.png"
SEXES_COLUMN_IMAGE_FILE_NAME = "column_3.png"
BIRTHPLACE_COLUMN_IMAGE_FILE_NAME = "column_4.png"
BIRTHDATE_COLUMN_IMAGE_FILE_NAME =  "column_5.png"
RELIGION_COLUMN_IMAGE_FILE_NAME = "column_6.png"
EDUCATION_COLUMN_IMAGE_FILE_NAME = "column_7.png"
PROFESION_COLUMN_IMAGE_FILE_NAME ="column_8.png"

MARRIAGE_STAT_COLUMN_IMAGE_FILE_NAME = "column_1.png"
MARRIAGE_DATE_COLUMN_IMAGE_FILE_NAME = "column_2.png"
MARRIAGE_REL_COLUMN_IMAGE_FILE_NAME = "column_3.png"
CITIZEN_COLUMN_IMAGE_FILE_NAME = "column_4.png"
PASPOR_NO_COLUMN_IMAGE_FILE_NAME = "column_5.png"
KITAS_NO_COLUMN_IMAGE_FILE_NAME = "column_6.png"
FATHER_COLUMN_IMAGE_FILE_NAME = "column_7.png"
MOTHER_COLUMN_IMAGE_FILE_NAME = "column_8.png"

MARRIAGE_REL_COLUMN_IMAGE_FILE_NAME_2018V = "column_2.png"
CITIZEN_COLUMN_IMAGE_FILE_NAME_2018V = "column_3.png"
PASPOR_NO_COLUMN_IMAGE_FILE_NAME_2018V = "column_4.png"
KITAS_NO_COLUMN_IMAGE_FILE_NAME_2018V = "column_5.png"
FATHER_COLUMN_IMAGE_FILE_NAME_2018V = "column_6.png"
MOTHER_COLUMN_IMAGE_FILE_NAME_2018V = "column_7.png"

LOWER_TABLE_DIR = "./output/sliced_lower_table/"
UPPER_TABLE_DIR = "./output/sliced_upper_table/"

@dataclass
class KKStructure:
    version : str = ""
    names: list[str] = field(default_factory=list)
    niks: list[str] = field(default_factory=list)
    sexes: list[str] = field(default_factory=list)
    birthplaces :list[str] = field(default_factory=list)
    birthdates: list[str] = field(default_factory=list)
    religions: list[str] = field(default_factory=list)
    educations: list[str] = field(default_factory=list)
    profession: list[str] = field(default_factory=list)
    marriage_stats: list[str] = field(default_factory=list)
    marriage_dates: list[str] = field(default_factory=list)
    marriage_rels: list[str] = field(default_factory=list)
    citizenships: list[str] = field(default_factory=list)
    paspor_no: list[str] = field(default_factory=list)
    kitas_no: list[str] = field(default_factory=list)
    father_names: list[str] = field(default_factory=list)
    mother_names: list[str] = field(default_factory=list)

    def __init__(self, version):
        self.version = version
    
    def add_names(self,):
        table_scanner = ts.TableScanner()
        self.names = table_scanner.detect_single_image(UPPER_TABLE_DIR+FULL_NAME_COLUMN_IMAGE_FILE_NAME)
        print("NAMES: ",self.names)
        print("scanning names completed\n\n")
    
    def add_niks(self,):
        table_scanner = ts.TableScanner()
        self.niks = table_scanner.detect_single_image(UPPER_TABLE_DIR+NIK_COLUMN_IMAGE_FILE_NAME)
        print("NIK: ", self.niks)
        print("scanning niks completed\n\n")

    def add_sexes(self,):
        table_scanner = ts.TableScanner()
        self.sexes = table_scanner.detect_single_image(UPPER_TABLE_DIR+SEXES_COLUMN_IMAGE_FILE_NAME)
        print("SEX: ",self.sexes)
        print("scanning sexes completed\n\n")

    def add_birthplaces(self,):
        table_scanner = ts.TableScanner()
        self.birthplaces = table_scanner.detect_single_image(UPPER_TABLE_DIR+BIRTHPLACE_COLUMN_IMAGE_FILE_NAME )
        print("BIRTHPLACE: ",self.birthplaces)
        print("scanning birthplaces completed\n\n")
    
    def add_birthdates(self,):
        table_scanner = ts.TableScanner()
        self.birthdates = table_scanner.detect_single_image(UPPER_TABLE_DIR+BIRTHDATE_COLUMN_IMAGE_FILE_NAME)
        print("BIRTHDATES: ",self.birthdates)
        print("scanning birthdates completed\n\n")

    def add_religions(self,):
        table_scanner = ts.TableScanner()
        self.religions = table_scanner.detect_single_image(UPPER_TABLE_DIR+RELIGION_COLUMN_IMAGE_FILE_NAME)
        print("RELIGIONS: ",self.religions)
        print("scanning religions completed\n\n")

    def add_educations(self,):
        table_scanner = ts.TableScanner()
        self.educations = table_scanner.detect_single_image(UPPER_TABLE_DIR+EDUCATION_COLUMN_IMAGE_FILE_NAME)
        print("EDUCATIONS: ",self.educations)
        print("scanning educations completed\n\n")

    def add_profession(self,):
        table_scanner = ts.TableScanner()
        self.profession = table_scanner.detect_single_image(UPPER_TABLE_DIR+PROFESION_COLUMN_IMAGE_FILE_NAME)
        print("PROFESSION: ", self.profession)
        print("scanning professions completed\n\n")

# +++++++++++++++++++++++++
    def add_marriage_stats(self,):
        table_scanner = ts.TableScanner()
        self.marriage_stats = table_scanner.detect_single_image(LOWER_TABLE_DIR+MARRIAGE_STAT_COLUMN_IMAGE_FILE_NAME)
        print("MARRIAGE STATUS :",self.marriage_stats)
        print("scanning marriage stats completed\n\n")
    
    def add_marriage_dates(self,):
        if self.version == ip.BEFORE_2018V:
            self.marriage_dates = []
            return
        table_scanner = ts.TableScanner()
        self.marriage_dates = table_scanner.detect_single_image(LOWER_TABLE_DIR+MARRIAGE_DATE_COLUMN_IMAGE_FILE_NAME)
        print("MARRIAGE DATES: ",self.marriage_dates)
        print("scanning marriage dates completed\n\n")
    
    def add_marriage_rels(self,):
        table_scanner = ts.TableScanner()
        if self.version == ip.BEFORE_2018V:
            self.marriage_rels = table_scanner.detect_single_image(LOWER_TABLE_DIR+MARRIAGE_REL_COLUMN_IMAGE_FILE_NAME_2018V)
        else :
            self.marriage_rels = table_scanner.detect_single_image(LOWER_TABLE_DIR+MARRIAGE_REL_COLUMN_IMAGE_FILE_NAME)
        print("MARRIAGE_RELATIONSHIP: ",self.marriage_rels)
        print("scanning marriage rels completed\n\n")

    def add_citizenship(self,):
        table_scanner = ts.TableScanner()
        if self.version == ip.BEFORE_2018V:
            self.citizenships = table_scanner.detect_single_image(LOWER_TABLE_DIR+CITIZEN_COLUMN_IMAGE_FILE_NAME_2018V)
        else :
            self.citizenships = table_scanner.detect_single_image(LOWER_TABLE_DIR+CITIZEN_COLUMN_IMAGE_FILE_NAME)
        print("CITIZENSHIPS: ",self.citizenships)
        print("scanning citizenship completed\n\n")

    def add_paspor_no(self,):
        table_scanner = ts.TableScanner()
        if self.version == ip.BEFORE_2018V:
            self.paspor_no = table_scanner.detect_single_image(LOWER_TABLE_DIR+PASPOR_NO_COLUMN_IMAGE_FILE_NAME_2018V)
        else :
            self.paspor_no = table_scanner.detect_single_image(LOWER_TABLE_DIR+PASPOR_NO_COLUMN_IMAGE_FILE_NAME)
        print("PASPOR NO: ", self.paspor_no)
        print("scanning paspor numbers completed\n\n")

    def add_kitas_no(self,):
        table_scanner = ts.TableScanner()
        if self.version == ip.BEFORE_2018V:
            self.kitas_no = table_scanner.detect_single_image(LOWER_TABLE_DIR+KITAS_NO_COLUMN_IMAGE_FILE_NAME_2018V)
        else:
            self.kitas_no = table_scanner.detect_single_image(LOWER_TABLE_DIR+KITAS_NO_COLUMN_IMAGE_FILE_NAME)
        print("KITAS NO: ",self.kitas_no)
        print("scanning kitas numbers completed\n\n")
    
    def add_father_names(self,):
        table_scanner = ts.TableScanner()
        if self.version == ip.BEFORE_2018V:
            self.father_names = table_scanner.detect_single_image(LOWER_TABLE_DIR+FATHER_COLUMN_IMAGE_FILE_NAME_2018V)
        else :
            self.father_names = table_scanner.detect_single_image(LOWER_TABLE_DIR+FATHER_COLUMN_IMAGE_FILE_NAME)
        print("FATHER NAMES: ",self.father_names)
        print("scanning father names completed\n\n")

    def add_mother_names(self,):
        table_scanner = ts.TableScanner()
        if self.version == ip.BEFORE_2018V:
            self.mother_names = table_scanner.detect_single_image(LOWER_TABLE_DIR+MOTHER_COLUMN_IMAGE_FILE_NAME_2018V)
        else : 
            self.mother_names = table_scanner.detect_single_image(LOWER_TABLE_DIR+MOTHER_COLUMN_IMAGE_FILE_NAME)
        print("MOTHER NAMES: ", self.mother_names)
        print("scanning mother names completed\n\n")

    def generate_json(self, filename, template_filename):
        # Load the existing template JSON
        with open(template_filename, "r") as f:
            data = json.load(f)

        # Update the fields in the template with current dataclass values
        for key, value in asdict(self).items():
            # if key in data:
            data[key] = value  # overwrite only if key exists in template

        # Save back to the same file (or you can specify a different output filename)
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"JSON file '{filename}' updated based on template.")

    def execute(self, filename, template_filename):
        self.add_names()
        self.add_niks()
        self.add_sexes()
        self.add_birthplaces()
        self.add_birthdates()
        self.add_religions()
        self.add_educations()
        self.add_profession()
        self.add_marriage_stats()
        self.add_marriage_dates()
        self.add_marriage_rels()
        self.add_citizenship()
        self.add_paspor_no()
        self.add_kitas_no()
        self.add_father_names()
        self.add_mother_names()
        self.generate_json(filename=filename,template_filename=template_filename)