import unittest
from translator import translate
class TestTranslation(unittest.TestCase):
    def test_gender(self):
        self.assertEqual(translate("Pria"), "男性")
        self.assertEqual(translate("LAKI LAKI"), "男性")
        self.assertEqual(translate("wanita"), "女性")
        self.assertEqual(translate("Perempuan"), "女性")

    def test_religion(self):
        self.assertEqual(translate("Islam"), "イスラム教")
        self.assertEqual(translate("kristen"), "キリスト教")
        self.assertEqual(translate("Katolik"), "カトリック")
        self.assertEqual(translate("Hindu"), "ヒンドゥー教")
        self.assertEqual(translate("Buddha"), "仏教")

    def test_marital_status(self):
        self.assertEqual(translate("Belum Kawin"), "未婚")
        self.assertEqual(translate("Kawin"), "既婚")
        self.assertEqual(translate("Cerai Hidup"), "離婚")
        self.assertEqual(translate("Cerai Mati"), "死別")
        self.assertEqual(translate("Kawin Tercatat"), "既婚")

    def test_job(self):
        self.assertEqual(translate("Pegawai Negeri Sipil"), "公務員")
        self.assertEqual(translate("PNS"), "公務員")
        self.assertEqual(translate("TNI"), "軍人")
        self.assertEqual(translate("Petani"), "農家")
        self.assertEqual(translate("Petani/Pekebun"), "農家")
        self.assertEqual(translate("Petani / Pekebun"), "農家")
        self.assertEqual(translate("Petan / Pekebun"), "農家")
        self.assertEqual(translate("Ustadz/Mubaligh"), "牧師")
        self.assertEqual(translate("Ustadz / Mubaligh"), "牧師")
        self.assertEqual(translate("Pelajar"), "学生")
        self.assertEqual(translate("Pelajar/Mahasiswa"), "学生")

    def test_education(self):
        self.assertEqual(translate("BELUM TAMAT SD / SEDERAJAT"), "小学校未卒")
        self.assertEqual(translate("SLTP/Sederajat"), "中学校卒業")
        self.assertEqual(translate("sltp / sederajat"), "中学校卒業")
        self.assertEqual(translate("SLTA/Sederajat"), "高校卒業")
        self.assertEqual(translate("slta / sederajat"), "高校卒業")
        self.assertEqual(translate("Akademi/Diploma III/Sarjana Muda"), "専門学校")
        self.assertEqual(translate("Diploma IV/Strata I"), "大学")
        self.assertEqual(translate("Strata II"), "大学院")
        self.assertEqual(translate("Strata III"), "博士課程")

    def test_family_roles(self):
        self.assertEqual(translate("Kepala Keluarga"), "家長")
        self.assertEqual(translate("Suami"), "夫")
        self.assertEqual(translate("Istri"), "妻")
        self.assertEqual(translate("Anak"), "子")
        self.assertEqual(translate("Menantu"), "義理の子")
        self.assertEqual(translate("Cucu"), "孫")
        self.assertEqual(translate("Orangtua"), "両親")
        self.assertEqual(translate("Mertua"), "義理の親")
        self.assertEqual(translate("Famili Lain"), "他の家族")
        self.assertEqual(translate("Pembantu"), "使用人")
        self.assertEqual(translate("Lainnya"), "その他")

    def test_nationality(self):
        self.assertEqual(translate("Indonesia"), "インドネシア")
        self.assertEqual(translate("WNI"), "インドネシア")
        self.assertEqual(translate("WN"), "インドネシア")


    def test_not_found(self):
        self.assertEqual(translate("Tidak Ada"), "Tidak Ada")
        # self.assertEqual(translate("unknown category"), "unknowsdn category")
        self.assertEqual(translate("RandomText"), "RandomText")

if __name__ == "__main__":
    unittest.main()