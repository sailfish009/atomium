from datetime import date
from unittest import TestCase
from unittest.mock import Mock, patch, PropertyMock, MagicMock
from atomium.pdb import *

class PdbStringToPdbDictTests(TestCase):

    @patch("atomium.pdb.update_dict")
    def test_can_convert_pdb_string_to_pdb_dict_one_model(self, mock_up):
        ring = "\n".join([
         "HEAD   LINE ", "TITLE  L1     ", "TITLE  L2", ""
         "REMARK 1  X", "REMARK 2  Y", "REMARK 2  Z",
         "ATOM   1", "ATOM   2", "HETATM 1",
         "CONECT 10", "CONECT 20"
        ])
        mock_up.side_effect = lambda d, k, v: d.update({k: v})
        d = pdb_string_to_pdb_dict(ring)
        self.assertEqual(d, {
         "HEAD": "HEAD   LINE", "TITLE": "TITLE  L2",
         "REMARK": {"1": "REMARK 1  X", "2": "REMARK 2  Z"},
         "MODEL": [["ATOM   1", "ATOM   2", "HETATM 1"]],
         "CONECT": "CONECT 20"
        })
        mock_up.assert_any_call(d, "HEAD", "HEAD   LINE")
        mock_up.assert_any_call(d, "TITLE", "TITLE  L1")
        mock_up.assert_any_call(d, "TITLE", "TITLE  L2")
        mock_up.assert_any_call(d["REMARK"], "1", "REMARK 1  X")
        mock_up.assert_any_call(d["REMARK"], "2", "REMARK 2  Y")
        mock_up.assert_any_call(d["REMARK"], "2", "REMARK 2  Z")
        mock_up.assert_any_call(d, "CONECT", "CONECT 10")
        mock_up.assert_any_call(d, "CONECT", "CONECT 20")


    @patch("atomium.pdb.update_dict")
    def test_can_convert_pdb_string_to_pdb_dict_multi_model(self, mock_up):
        ring = "\n".join([
         "HEAD   LINE ", "TITLE  L1     ", "TITLE  L2",
         "MODEL    1", "ATOM   1", "HETATM 1", "ENDMDL",
         "MODEL    2", "ATOM   2", "HETATM 2", "ENDMDL",
         "MODEL    3", "ATOM   3", "HETATM 3", "ENDMDL",
         "CONECT 10", "CONECT 20"
        ])
        mock_up.side_effect = lambda d, k, v: d.update({k: v})
        d = pdb_string_to_pdb_dict(ring)
        self.assertEqual(d, {
         "HEAD": "HEAD   LINE", "TITLE": "TITLE  L2",
         "MODEL": [["ATOM   1", "HETATM 1"], ["ATOM   2", "HETATM 2"], ["ATOM   3", "HETATM 3"]],
         "CONECT": "CONECT 20"
        })
        mock_up.assert_any_call(d, "HEAD", "HEAD   LINE")
        mock_up.assert_any_call(d, "TITLE", "TITLE  L1")
        mock_up.assert_any_call(d, "TITLE", "TITLE  L2")
        mock_up.assert_any_call(d, "CONECT", "CONECT 10")
        mock_up.assert_any_call(d, "CONECT", "CONECT 20")



class DictUpdatingTests(TestCase):

    def test_can_add_to_list(self):
        d = {"a": [1], "b": 2}
        update_dict(d, "a", 5)
        self.assertEqual(d, {"a": [1, 5], "b": 2})


    def test_can_create_list(self):
        d = {"a": [1], "b": 2}
        update_dict(d, "c", 5)
        self.assertEqual(d, {"a": [1], "b": 2, "c": [5]})



class PdbDictToDataDictTests(TestCase):

    @patch("atomium.pdb.update_description_dict")
    @patch("atomium.pdb.update_experiment_dict")
    @patch("atomium.pdb.update_quality_dict")
    @patch("atomium.pdb.update_geometry_dict")
    @patch("atomium.pdb.update_models_list")
    def test_can_convert_pdb_dict_to_data_dict(self, mock_md, mock_gm, mock_ql, mock_ex, mock_ds):
        pdb_dict = {"A": "B"}
        d = pdb_dict_to_data_dict(pdb_dict)
        mock_ds.assert_called_with(pdb_dict, d)
        mock_ex.assert_called_with(pdb_dict, d)
        mock_ql.assert_called_with(pdb_dict, d)
        mock_gm.assert_called_with(pdb_dict, d)
        mock_md.assert_called_with(pdb_dict, d)
        self.assertEqual(d, {
         "description": {
          "code": None, "title": None, "deposition_date": None,
          "classification": None, "keywords": [], "authors": []
         }, "experiment": {
          "technique": None, "source_organism": None, "expression_system": None,
          "missing_residues": []
         }, "quality": {"resolution": None, "rvalue": None, "rfree": None},
         "geometry": {"assemblies": []}, "models": []
        })



class DescriptionDictUpdatingTests(TestCase):

    @patch("atomium.pdb.extract_header")
    @patch("atomium.pdb.extract_title")
    @patch("atomium.pdb.extract_keywords")
    @patch("atomium.pdb.extract_authors")
    def test_can_update_description_dict(self, mock_aut, mock_key, mock_tit, mock_hed):
        d = {"description": "dict"}
        pdb_dict = {"PDB": "DICT"}
        update_description_dict(pdb_dict, d)
        mock_hed.assert_called_with(pdb_dict, "dict")
        mock_tit.assert_called_with(pdb_dict, "dict")
        mock_key.assert_called_with(pdb_dict, "dict")
        mock_aut.assert_called_with(pdb_dict, "dict")



class ExperimentDictUpdatingTests(TestCase):

    @patch("atomium.pdb.extract_technique")
    @patch("atomium.pdb.extract_source")
    @patch("atomium.pdb.extract_missing_residues")
    def test_can_update_experiment_dict(self, mock_miss, mock_src, mock_tech):
        d = {"experiment": "dict"}
        pdb_dict = {"PDB": "DICT"}
        update_experiment_dict(pdb_dict, d)
        mock_src.assert_called_with(pdb_dict, "dict")
        mock_tech.assert_called_with(pdb_dict, "dict")
        mock_miss.assert_called_with(pdb_dict, "dict")



class QualityDictUpdatingTests(TestCase):

    @patch("atomium.pdb.extract_resolution_remark")
    @patch("atomium.pdb.extract_rvalue_remark")
    def test_can_update_quality_dict(self, mock_rfac, mock_res):
        d = {"quality": "dict"}
        pdb_dict = {"PDB": "DICT"}
        update_quality_dict(pdb_dict, d)
        mock_res.assert_called_with(pdb_dict, "dict")
        mock_rfac.assert_called_with(pdb_dict, "dict")



class GeometryDictUpdatingTests(TestCase):

    @patch("atomium.pdb.extract_assembly_remark")
    def test_can_update_geometry_dict(self, mock_ass):
        d = {"geometry": "dict"}
        pdb_dict = {"PDB": "DICT"}
        update_geometry_dict(pdb_dict, d)
        mock_ass.assert_called_with(pdb_dict, "dict")



class ModelsListUpdatingTests(TestCase):

    @patch("atomium.pdb.make_sequences")
    @patch("atomium.pdb.make_aniso")
    @patch("atomium.pdb.get_last_ter_line")
    @patch("atomium.pdb.id_from_line")
    @patch("atomium.pdb.add_atom_to_polymer")
    @patch("atomium.pdb.add_atom_to_non_polymer")
    def test_can_update_one_model(self, mock_np, mock_p, mock_id, mock_tr, mock_an, mock_sq):
        p = {"MODEL": [[
         "ATOM                 A",
         "ATOM                 A",
         "TER",
         "ATOM                 B",
         "ATOM                 B",
         "TER",
         "HETATM               A",
         "HETATM               B"
        ]]}
        d = {"models": []}
        model = {"polymer": {}, "non-polymer": {}, "water": {}}
        mock_tr.return_value = 5
        update_models_list(p, d)
        mock_sq.assert_called_with(p)
        mock_an.assert_called_with(p["MODEL"][0])
        mock_tr.assert_called_with(p["MODEL"][0])
        for n in [0, 1, 3, 4, 6, 7]: mock_id.assert_any_call(p["MODEL"][0][n])
        for n in [0, 1, 3, 4]: mock_p.assert_any_call(
         p["MODEL"][0][n], model, "A" if n < 2 else "B", mock_id.return_value, mock_an.return_value
        )
        for n in [6, 7]: mock_np.assert_any_call(
         p["MODEL"][0][n], model, mock_id.return_value, mock_an.return_value
        )



class HeaderExtractionTests(TestCase):

    def setUp(self):
        self.d = {"code": None, "deposition_date": None, "classification": None}


    def test_can_extract_no_header(self):
        extract_header({"TITLE": ["1"]}, self.d)
        self.assertEqual(self.d, {"code": None, "deposition_date": None, "classification": None})


    def test_can_extract_empty_header(self):
        extract_header({"HEADER": [" " * 74]}, self.d)
        self.assertEqual(self.d, {"code": None, "deposition_date": None, "classification": None})


    def test_can_extract_header(self):
        extract_header({"HEADER": [
         "HEADER    UNKNOWN FUNCTION" + " " * 24 + "21-AUG-17   6AR7" + " " * 14
        ]}, self.d)
        self.assertEqual(self.d, {
         "code": "6AR7", "deposition_date": date(2017, 8, 21), "classification": "UNKNOWN FUNCTION"
        })



class TitleExtractionTests(TestCase):

    def test_missing_title_extraction(self):
        d = {"title": None}
        extract_title({"HEADER": ["1"]}, d)
        self.assertEqual(d, {"title": None})


    @patch("atomium.pdb.merge_lines")
    def test_title_extraction(self, mock_merge):
        d = {"title": None}
        mock_merge.return_value = "TITLE TITLE TITLE"
        extract_title({"TITLE": ["TITLE     L1", "TITLE    2 L2"]}, d)
        mock_merge.assert_called_with(["TITLE     L1", "TITLE    2 L2"], 10)
        self.assertEqual(d["title"], "TITLE TITLE TITLE")



class KeywordExtractionTests(TestCase):

    def test_missing_keyword_extraction(self):
        d = {"keywords": []}
        extract_keywords({"HEADER": ["1"]}, d)
        self.assertEqual(d, {"keywords": []})


    @patch("atomium.pdb.merge_lines")
    def test_keywords_extraction(self, mock_merge):
        d = {"keywords": []}
        mock_merge.return_value = "KEY1, KEY2, KEY3"
        extract_keywords({"KEYWDS": ["KEY     L1", "KEY    2 L2"]}, d)
        mock_merge.assert_called_with(["KEY     L1", "KEY    2 L2"], 10)
        self.assertEqual(d["keywords"], ["KEY1", "KEY2", "KEY3"])



class AuthorExtractionTests(TestCase):

    def test_missing_author_extraction(self):
        d = {"authors": []}
        extract_authors({"HEADER": ["1"]}, d)
        self.assertEqual(d, {"authors": []})


    @patch("atomium.pdb.merge_lines")
    def test_authors_extraction(self, mock_merge):
        d = {"authors": []}
        mock_merge.return_value = "AT1, AT2, AT3"
        extract_authors({"AUTHOR": ["AT     L1", "AT    2 L2"]}, d)
        mock_merge.assert_called_with(["AT     L1", "AT    2 L2"], 10)
        self.assertEqual(d["authors"], ["AT1", "AT2", "AT3"])



class TechniqueExtractionTests(TestCase):

    def test_missing_technique_extraction(self):
        d = {"technique": None}
        extract_technique({"HEADER": ["1"]}, d)
        self.assertEqual(d, {"technique": None})


    def test_empty_technique_extraction(self):
        d = {"technique": None}
        extract_technique({"EXPDTA": ["     "]}, d)
        self.assertEqual(d, {"technique": None})


    def test_technique_extraction(self):
        d = {"technique": None}
        extract_technique({"EXPDTA": ["EXPDTA    X-RAY DIFFRACTION       "]}, d)
        self.assertEqual(d, {"technique": "X-RAY DIFFRACTION"})



class SourceExtractionTests(TestCase):

    def test_missing_source_extraction(self):
        d = {"source_organism": None, "expression_system": None}
        extract_source({"HEADER": ["1"]}, d)
        self.assertEqual(d, {"source_organism": None, "expression_system": None})


    @patch("atomium.pdb.merge_lines")
    def test_empty_source_extraction(self, mock_merge):
        mock_merge.return_value = "JYVGBHUBBGYBHKJNHBK"
        d = {"source_organism": None, "expression_system": None}
        extract_source({"SOURCE": ["1", "2"]}, d)
        self.assertEqual(d, {"source_organism": None, "expression_system": None})
        mock_merge.assert_called_with(["1", "2"], 10)


    @patch("atomium.pdb.merge_lines")
    def test_empty_source_extraction(self, mock_merge):
        mock_merge.return_value = (
         "MOL_ID: 1;"
         " ORGANISM_SCIENTIFIC: METHANOTHERMOBACTER"
         " THERMAUTOTROPHICUS STR. DELTA H;"
         " ORGANISM_TAXID: 187420;"
         " STRAIN: DELTA H;"
         " EXPRESSION_SYSTEM: ESCHERICHIA COLI;"
         " EXPRESSION_SYSTEM_TAXID: 562;"
         " EXPRESSION_SYSTEM_PLASMID: PET15B"
        )
        d = {"source_organism": None, "expression_system": None}
        extract_source({"SOURCE": ["1", "2"]}, d)
        self.assertEqual(d, {
         "source_organism": "METHANOTHERMOBACTER THERMAUTOTROPHICUS STR. DELTA H",
         "expression_system": "ESCHERICHIA COLI"
        })
        mock_merge.assert_called_with(["1", "2"], 10)



class MissingResiduesExtractionTests(TestCase):

    def setUp(self):
        self.remark_lines = {
         "1": ["", "BLAH BLAH"],
         "465": ["", "REMARK 465 MISSING RESIDUES", "REMARK 465     LEU A     1",
         "REMARK 465     VAL A     6A", "REMARK 465     LEU B  1001"],
         "466": ["", "BLAH BLAH"]
        }


    def test_missing_remarks_extraction(self):
        d = {"missing_residues": []}
        del self.remark_lines["465"]
        extract_missing_residues({"REMARK": self.remark_lines}, d)
        self.assertEqual(d, {"missing_residues": []})
        extract_missing_residues({"ABC": []}, d)
        self.assertEqual(d, {"missing_residues": []})


    def test_missing_residues_extraction(self):
        d = {"missing_residues": []}
        extract_missing_residues({"REMARK": self.remark_lines}, d)
        self.assertEqual(d, {"missing_residues": [
         {"name": "LEU", "id": "A.1"}, {"name": "VAL", "id": "A.6A"}, {"name": "LEU", "id": "B.1001"}
        ]})



class ResolutionExtractionTests(TestCase):

    def setUp(self):
        self.remark_lines = {
         "1": ["", "BLAH BLAH"],
         "2": ["", "REMARK 2   RESOLUTION.    1.90 ANGSTROMS."],
         "24": ["", "BLAH BLAH"]
        }


    def test_missing_remarks_extraction(self):
        d = {"resolution": None}
        del self.remark_lines["2"]
        extract_resolution_remark({"REMARK": self.remark_lines}, d)
        self.assertEqual(d, {"resolution": None})
        extract_resolution_remark({"ABC": []}, d)
        self.assertEqual(d, {"resolution": None})


    def test_empty_resolution_extraction(self):
        d = {"resolution": None}
        self.remark_lines["2"][1] = "REMARK 2   RESOLUTION. NOT APPLICABLE."
        extract_resolution_remark({"REMARK": self.remark_lines}, d)
        self.assertEqual(d, {"resolution": None})


    def test_resolution_extraction(self):
        d = {"resolution": None}
        extract_resolution_remark({"REMARK": self.remark_lines}, d)
        self.assertEqual(d, {"resolution": 1.9})



class RvalueExtractionTests(TestCase):

    def setUp(self):
        self.remark_lines = {
         "1": ["", "BLAH BLAH"],
         "3": [
          "REMARK 3     CROSS-VALIDATION METHOD          : THROUGHOUT",
          "REMARK 3     FREE R VALUE TEST SET SELECTION  : RANDOM",
          "REMARK 3     R VALUE            (WORKING SET) : 0.193",
          "REMARK 3     FREE R VALUE                     : 0.229",
          "REMARK 3     FREE R VALUE TEST SET SIZE   (%) : 4.900",
          "REMARK 3     FREE R VALUE TEST SET COUNT      : 1583",
          "REMARK 3     BIN R VALUE           (WORKING SET) : 0.2340 "
         ],
         "24": ["", "BLAH BLAH"]
        }


    def test_missing_rvalue_extraction(self):
        d = {"rvalue": None, "rfree": None}
        del self.remark_lines["3"]
        extract_resolution_remark({"REMARK": self.remark_lines}, d)
        self.assertEqual(d, {"rvalue": None, "rfree": None})
        extract_rvalue_remark({"ABC": []}, d)
        self.assertEqual(d, {"rvalue": None, "rfree": None})


    def test_empty_rvalue_extraction(self):
        d = {"rvalue": None, "rfree": None}
        self.remark_lines["3"][2] = self.remark_lines["3"][2][:-7]
        self.remark_lines["3"][3] = self.remark_lines["3"][3][:-7]
        self.remark_lines["3"].pop()
        extract_rvalue_remark({"REMARK": self.remark_lines}, d)
        self.assertEqual(d, {"rvalue": None, "rfree": None})


    def test_rvalue_extraction(self):
        d = {"rvalue": None, "rfree": None}
        extract_rvalue_remark({"REMARK": self.remark_lines}, d)
        self.assertEqual(d, {"rvalue": 0.193, "rfree": 0.229})



class BiomoleculeExtractionTests(TestCase):

    def setUp(self):
        self.remark_lines = {
         "1": ["BLAH BLAH"],
         "350": [
          "REMARK 350 ",
          "REMARK 350  BIOMOLECULE: 1",
          "REMARK 350  SOFTWARE DETERMINED QUATERNARY STRUCTURE: DIMERIC",
          "REMARK 350  SOFTWARE USED: PISA",
          "REMARK 350  TOTAL BURIED SURFACE AREA: 1650 ANGSTROM**2",
          "REMARK 350  SURFACE AREA OF THE COMPLEX: 4240 ANGSTROM**2",
          "REMARK 350  APPLY THE FOLLOWING TO CHAINS: G, H",
          "REMARK 350    BIOMT1   1  1.000000  0.000000  0.000000        0.00000",
          "REMARK 350    BIOMT2   1  0.000000  1.000000  0.000000        2.00000",
          "REMARK 350    BIOMT3   1  0.000000  0.000000  1.000000        -6.00000",
          "REMARK 350 ",
          "REMARK 350  BIOMOLECULE: 5",
          "REMARK 350  SOFTWARE DETERMINED QUATERNARY STRUCTURE: DODECAMERIC",
          "REMARK 350  SOFTWARE USED: PISA",
          "REMARK 350  TOTAL BURIED SURFACE AREA: 21680 ANGSTROM**2",
          "REMARK 350  SURFACE AREA OF THE COMPLEX: 12240 ANGSTROM**2",
          "REMARK 350  CHANGE IN SOLVENT FREE ENERGY: -332.0 KCAL/MOL",
          "REMARK 350  APPLY THE FOLLOWING TO CHAINS: E, F, G, H,",
          "REMARK 350                     AND CHAINS: J, K, L",
          "REMARK 350    BIOMT1   1  1.000000  0.000000  0.000000        0.00000",
          "REMARK 350    BIOMT2   1  0.000000  1.000000  0.000000        0.00000",
          "REMARK 350    BIOMT3   1  0.000000  0.000000  1.000000        0.00000",
          "REMARK 350    BIOMT1   2 -0.500000 -0.866025  0.000000        0.00000",
          "REMARK 350    BIOMT2   2  0.866025 -0.500000  0.000000        0.00000",
          "REMARK 350    BIOMT3   2  0.000000  0.000000  1.000000        0.00000",
         ],
         "24": ["", "BLAH BLAH"]
        }


    def test_missing_biomolecules_extraction(self):
        d = {"assemblies": []}
        del self.remark_lines["350"]
        extract_assembly_remark({"REMARK": self.remark_lines}, d)
        self.assertEqual(d, {"assemblies": []})


    @patch("atomium.pdb.assembly_lines_to_assembly_dict")
    def test_biomolecules_extraction(self, mock_dict):
        mock_dict.side_effect = "AB"
        d = {"assemblies": []}
        extract_assembly_remark({"REMARK": self.remark_lines}, d)
        self.assertEqual(d, {"assemblies": ["A", "B"]})
        mock_dict.assert_any_call(self.remark_lines["350"][1:11])
        mock_dict.assert_any_call(self.remark_lines["350"][11:])



class AssemblyLinesToAssemblyDictTests(TestCase):

    def test_can_parse_simple_assembly(self):
        d = assembly_lines_to_assembly_dict([
         "REMARK 350  BIOMOLECULE: 1",
         "REMARK 350  SOFTWARE DETERMINED QUATERNARY STRUCTURE: DIMERIC",
         "REMARK 350  SOFTWARE USED: PISA",
         "REMARK 350  TOTAL BURIED SURFACE AREA: 1650 ANGSTROM**2",
         "REMARK 350  SURFACE AREA OF THE COMPLEX: 4240 ANGSTROM**2",
         "REMARK 350  CHANGE IN SOLVENT FREE ENERGY: -7.0 KCAL/MOL",
         "REMARK 350  APPLY THE FOLLOWING TO CHAINS: G, H",
         "REMARK 350    BIOMT1   1  1.000000  0.000000  0.000000        0.00000",
         "REMARK 350    BIOMT2   1  0.000000  1.000000  0.000000        2.00000",
         "REMARK 350    BIOMT3   1  0.000000  0.000000  1.000000        -6.00000",
         "REMARK 350 "
        ])
        self.assertEqual(d, {
         "id": 1, "software": "PISA", "delta_energy": -7.0,
         "buried_surface_area": 1650.0, "surface_area": 4240.0,
         "transformations": [{
          "chains": ["G", "H"],
          "matrix": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
          "vector": [0.0, 2.0, -6.0]
         }]
        })


    def test_can_parse_complex_assembly(self):
        d = assembly_lines_to_assembly_dict([
         "REMARK 350  BIOMOLECULE: 5",
         "REMARK 350  SOFTWARE DETERMINED QUATERNARY STRUCTURE: DODECAMERIC",
         "REMARK 350  SOFTWARE USED: PISA",
         "REMARK 350  TOTAL BURIED SURFACE AREA: 21680 ANGSTROM**2",
         "REMARK 350  SURFACE AREA OF THE COMPLEX: 12240 ANGSTROM**2",
         "REMARK 350  CHANGE IN SOLVENT FREE ENERGY: -332.0 KCAL/MOL",
         "REMARK 350  APPLY THE FOLLOWING TO CHAINS: E, F, G, H,",
         "REMARK 350                     AND CHAINS: J, K, L",
         "REMARK 350    BIOMT1   1  1.000000  0.000000  0.000000        0.00000",
         "REMARK 350    BIOMT2   1  0.000000  1.000000  0.000000        0.00000",
         "REMARK 350    BIOMT3   1  0.000000  0.000000  1.000000        0.00000",
         "REMARK 350    BIOMT1   2 -0.500000 -0.866025  0.000000        0.00000",
         "REMARK 350    BIOMT2   2  0.866025 -0.500000  0.000000        0.00000",
         "REMARK 350    BIOMT3   2  0.000000  0.000000  1.000000        0.00000",
        ])
        self.assertEqual(d, {
         "id": 5, "software": "PISA", "delta_energy": -332.0,
         "buried_surface_area": 21680.0, "surface_area": 12240.0,
         "transformations": [{
          "chains": ["E", "F", "G", "H", "J", "K", "L"],
          "matrix": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
          "vector": [0.0, 0.0, 0.0]
         }, {
          "chains": ["E", "F", "G", "H", "J", "K", "L"],
          "matrix": [[-0.5, -0.866025, 0.0], [0.866025, -0.5, 0.0], [0, 0, 1]],
          "vector": [0.0, 0.0, 0.0]
         }]
        })


    def test_can_parse_sparse_assembly(self):
        d = assembly_lines_to_assembly_dict([
         "REMARK 350  BIOMOLECULE: 1",
         "REMARK 350  APPLY THE FOLLOWING TO CHAINS: G, H",
         "REMARK 350    BIOMT1   1  1.000000  0.000000  0.000000        0.00000",
         "REMARK 350    BIOMT2   1  0.000000  1.000000  0.000000        2.00000",
         "REMARK 350    BIOMT3   1  0.000000  0.000000  1.000000        -6.00000",
         "REMARK 350 "
        ])
        self.assertEqual(d, {
         "id": 1, "software": None, "delta_energy": None,
         "buried_surface_area": None, "surface_area": None,
         "transformations": [{
          "chains": ["G", "H"],
          "matrix": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
          "vector": [0.0, 2.0, -6.0]
         }]
        })



class SequenceMakingTests(TestCase):

    def test_can_make_no_sequences(self):
        self.assertEqual(make_sequences({}), {})


    def test_can_make_sequences(self):
        self.assertEqual(make_sequences({"SEQRES": [
         "SEQRES   1 C  271  VAL TRP XYZ",
         "SEQRES   1 C  271  HIS",
         "SEQRES   1 D  271  DT DA"
        ]}), {"C": "VWXH", "D": "TA"})



class AnisoMakingTests(TestCase):

    def test_can_make_no_aniso(self):
        self.assertEqual(make_aniso([]), {})


    def test_can_make_aniso(self):
        self.assertEqual(make_aniso([
         "ANISOU  107  N   GLY A  13     2406   1892   1614    198    519   -328",
         "ANISOU  110  O   GLY A  13     3837   2505   1611    164   -121    189"
        ]), {
         107: [0.2406, 0.1892, 0.1614, 0.0198, 0.0519, -0.0328],
         110: [0.3837, 0.2505, 0.1611, 0.0164, -0.0121, 0.0189]
        })



class LastTerLineTests(TestCase):

    def test_can_get_no_ter_line(self):
        self.assertEqual(get_last_ter_line(["ATOM", "HETATM"]), 0)


    def test_can_get_last_ter_line(self):
        self.assertEqual(get_last_ter_line(["AT", "TER", "HET", "TER", "4"]), 3)



class IdFromLineTests(TestCase):

    def test_can_get_id_no_insert(self):
        self.assertEqual(id_from_line("ATOM    219  CZ  TYR A  37 "), "A.37")


    def test_can_get_id_with_insert(self):
        self.assertEqual(id_from_line("ATOM    219  CZ  TYR A  37B"), "A.37B")



class AtomToPolymerTests(TestCase):

    @patch("atomium.pdb.atom_line_to_dict")
    def test_can_add_atom_to_residue(self, mock_at):
        model = {"polymer": {"A": {"residues": {"A.10": {"atoms": {}}}}}}
        line = "ATOM    10   "
        add_atom_to_polymer(line, model, "A", "A.10", {1: 2})
        mock_at.assert_called_with(line, {1: 2})
        self.assertEqual(
         model, {"polymer": {"A": {"residues": {"A.10": {"atoms": {10: mock_at.return_value}}}}}}
        )


    @patch("atomium.pdb.atom_line_to_dict")
    def test_can_add_atom_to_chain(self, mock_at):
        model = {"polymer": {"A": {"residues": {}}}}
        line = "ATOM    10       RES"
        add_atom_to_polymer(line, model, "A", "A.10", {1: 2})
        mock_at.assert_called_with(line, {1: 2})
        self.assertEqual(model,
         {"polymer": {"A": {"residues": {"A.10": {"name": "RES", "number": 1, "atoms": {10: mock_at.return_value}}}}}}
        )


    @patch("atomium.pdb.atom_line_to_dict")
    def test_can_add_atom_to_model(self, mock_at):
        model = {"polymer": {}}
        line = "ATOM    10       RES"
        add_atom_to_polymer(line, model, "A", "A.10", {1: 2})
        mock_at.assert_called_with(line, {1: 2})
        self.assertEqual(model,
         {"polymer": {"A": {"internal_id": "A", "residues": {"A.10": {
          "name": "RES", "number": 1, "atoms": {10: mock_at.return_value}
         }}}}}
        )



class AtomToNonPolymerTests(TestCase):

    @patch("atomium.pdb.atom_line_to_dict")
    def test_can_add_atom_to_molecule(self, mock_at):
        model = {"non-polymer": {"A.10": {"atoms": {}}}}
        line = "ATOM    10   "
        add_atom_to_non_polymer(line, model, "A.10", {1: 2})
        mock_at.assert_called_with(line, {1: 2})
        self.assertEqual(
         model, {"non-polymer": {"A.10": {"atoms": {10: mock_at.return_value}}}}
        )


    @patch("atomium.pdb.atom_line_to_dict")
    def test_can_add_atom_to_model(self, mock_at):
        model = {"non-polymer": {}}
        line = "ATOM    10       MOL A"
        add_atom_to_non_polymer(line, model, "A.10", {1: 2})
        mock_at.assert_called_with(line, {1: 2})
        self.assertEqual(
         model, {"non-polymer": {"A.10": {
          "internal_id": "A", "polymer": "A", "name": "MOL", "atoms": {10: mock_at.return_value}
         }}}
        )


    @patch("atomium.pdb.atom_line_to_dict")
    def test_can_add_atom_to_water(self, mock_at):
        model = {"water": {"A.10": {"atoms": {}}}}
        line = "ATOM    10       HOH A"
        add_atom_to_non_polymer(line, model, "A.10", {1: 2})
        mock_at.assert_called_with(line, {1: 2})
        self.assertEqual(
         model, {"water": {"A.10": {"atoms": {10: mock_at.return_value}}}}
        )



class AtomLineToDictTests(TestCase):

    def test_can_convert_full_line_to_atom(self):
        atom = atom_line_to_dict(
         "ATOM    107  N1 AGLY B  13C     " +
         "12.681  37.302 -25.211 0.70  15.56           N2-", {1: 100, 107: 200}
        )
        self.assertEqual(atom, {
         "name": "N1", "alt_loc": "A", "x": 12.681, "y": 37.302, "z": -25.211,
         "occupancy": 0.7, "bvalue": 15.56, "anisotropy": 200,
         "element": "N", "charge": -2,
        })


    def test_can_handle_weird_charge(self):
        atom = atom_line_to_dict(
         "ATOM    107  N1  GLY B  13      " +
         "12.681  37.302 -25.211 0.70  15.56           N-2", {}
        )
        self.assertEqual(atom, {
         "name": "N1", "alt_loc": None, "x": 12.681, "y": 37.302, "z": -25.211,
         "occupancy": 0.7, "bvalue": 15.56, "anisotropy": [0] * 6,
         "element": "N", "charge": -2,
        })



class LineMergingTests(TestCase):

    def setUp(self):
        self.lines = ["0123456789 ", "abcdefghij ", "0123456789 "]
        self.punc_lines = ["0123, 456789 ", "abcd  efghij ", "0123; 456789 "]


    def test_can_merge_lines(self):
        self.assertEqual(
         merge_lines(self.lines, 5),
         "56789 fghij 56789"
        )
        self.assertEqual(
         merge_lines(self.lines, 8),
         "89 ij 89"
        )


    def test_can_vary_join(self):
        self.assertEqual(
         merge_lines(self.lines, 5, join=""),
         "56789fghij56789"
        )
        self.assertEqual(
         merge_lines(self.lines, 8, join="."),
         "89.ij.89"
        )



class StructureToPdbStringTests(TestCase):

    def setUp(self):
        self.patch1 = patch("atomium.pdb.pack_sequences")
        self.patch2 = patch("atomium.pdb.atom_to_atom_line")
        self.mock_pk = self.patch1.start()
        self.mock_at = self.patch2.start()
        self.mock_at.side_effect = lambda a, l: l.append(str(a.id))


    def tearDown(self):
        self.patch1.stop()
        self.patch2.stop()


    def test_can_convert_structure_with_one_chain_to_lines(self):
        structure = Mock()
        structure.atoms.return_value = [
         Mock(id=1, structure=Mock(Residue), chain=1), Mock(id=2, structure=Mock(Residue), chain=1)
        ]
        s = structure_to_pdb_string(structure)
        self.assertEqual(self.mock_pk.call_args_list[0][0][0], structure)
        self.assertEqual(s, "1\n2\nTER")



    def test_can_convert_structure_with_two_chains_to_lines(self):
        structure = Mock()
        structure.atoms.return_value = [
         Mock(id=1, structure=Mock(Residue), chain=1), Mock(id=2, structure=Mock(Residue), chain=1),
         Mock(id=3, structure=Mock(Residue), chain=2), Mock(id=4, structure=Mock(Residue), chain=2)
        ]
        s = structure_to_pdb_string(structure)
        self.assertEqual(self.mock_pk.call_args_list[0][0][0], structure)
        self.assertEqual(s, "1\n2\nTER\n3\n4\nTER")


    def test_can_convert_structure_with_one_chain_and_ligands_to_lines(self):
        structure = Mock()
        structure.atoms.return_value = [
         Mock(id=1, structure=Mock(Residue), chain=1), Mock(id=2, structure=Mock(Residue), chain=1),
         Mock(id=3, structure=Mock(Ligand), chain=1), Mock(id=4, structure=Mock(Ligand), chain=1)
        ]
        s = structure_to_pdb_string(structure)
        self.assertEqual(self.mock_pk.call_args_list[0][0][0], structure)
        self.assertEqual(s, "1\n2\nTER\n3\n4")


    def test_can_convert_structure_with_two_chains_and_ligands_to_lines(self):
        structure = Mock()
        structure.atoms.return_value = [
         Mock(id=1, structure=Mock(Residue), chain=1), Mock(id=2, structure=Mock(Residue), chain=1),
         Mock(id=3, structure=Mock(Residue), chain=2), Mock(id=4, structure=Mock(Residue), chain=2),
         Mock(id=5, structure=Mock(Ligand), chain=1), Mock(id=6, structure=Mock(Ligand), chain=1)
        ]
        s = structure_to_pdb_string(structure)
        self.assertEqual(self.mock_pk.call_args_list[0][0][0], structure)
        self.assertEqual(s, "1\n2\nTER\n3\n4\nTER\n5\n6")



class SequencePackingTests(TestCase):

    def test_can_pack_sequence(self):
        structure = Mock()
        structure.chains.return_value = [Mock(sequence="ABC" * 10, id=2), Mock(sequence="GA", id=1)]
        lines = []
        pack_sequences(structure, lines)
        self.assertEqual(lines, [
         "SEQRES   1 1    2  DG DA",
         "SEQRES   1 2   30  ALA XXX CYS ALA XXX CYS ALA XXX CYS ALA XXX CYS ALA",
         "SEQRES   2 2   30  XXX CYS ALA XXX CYS ALA XXX CYS ALA XXX CYS ALA XXX",
         "SEQRES   3 2   30  CYS ALA XXX CYS"
        ])


    def test_can_handle_no_chains(self):
        structure = Mock()
        structure.chains.side_effect = AttributeError
        lines = []
        pack_sequences(structure, lines)
        self.assertEqual(lines, [])



class AtomToAtomLineTests(TestCase):

    @patch("atomium.pdb.atom_to_anisou_line")
    def test_can_convert_atom_to_line_residue(self, mock_an):
        atom = Mock(structure=Mock(Residue, id="A100B", _name="RES"),
         chain=Mock(id="A"), _name="CD", id=100, x=1.2, y=2.7, z=-9, bvalue=12.1,
          charge=-2, element="C")
        lines = []
        atom_to_atom_line(atom, lines)
        self.assertEqual(lines[0], "ATOM    100  CD  RES A 100B      1.200   2.700  -9.000  1.00  12.1           C2-")
        self.assertEqual(lines[1], mock_an.return_value)
        mock_an.assert_called_with(atom, " CD", "RES", "A", 100, "B")


    @patch("atomium.pdb.atom_to_anisou_line")
    def test_can_convert_atom_to_line_ligand(self, mock_an):
        atom = Mock(structure=Mock(Ligand, id="A100B", _name="RES"),
         chain=Mock(id="A"), _name="CD", id=100, x=1.2, y=2.7, z=-9, bvalue=12.1,
          charge=-2, element="C", anisotropy=[0, 0, 0, 0, 0, 0])
        lines = []
        atom_to_atom_line(atom, lines)
        self.assertEqual(lines[0], "HETATM  100  CD  RES A 100B      1.200   2.700  -9.000  1.00  12.1           C2-")
        self.assertFalse(mock_an.called)


    @patch("atomium.pdb.atom_to_anisou_line")
    def test_can_convert_atom_to_line_bare(self, mock_an):
        atom = Mock(_name="CD", id=100, x=1.2, y=2.7, z=-9, bvalue=12.1,
          charge=-2, element="C", anisotropy=[0, 0, 0, 0, 0, 0], structure=None)
        lines = []
        atom_to_atom_line(atom, lines)
        self.assertEqual(lines[0], "ATOM    100  CD                  1.200   2.700  -9.000  1.00  12.1           C2-")
        self.assertFalse(mock_an.called)



class AtomToAnisouLinetests(TestCase):

    def test_can_convert_atom_to_anisou_line(self):
        atom = Mock(id=4, anisotropy=[0.12, 0.24, 0.36, 0.48, 0.512, 0.1], charge=-1, element="P")
        line = atom_to_anisou_line(atom, "A", "RES", "C", "101", "D")
        self.assertEqual(line, "ANISOU    4 A    RES C101 D    1200   2400   3600   4800   5120   1000       P1-")
