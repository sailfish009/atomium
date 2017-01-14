import datetime
from unittest import TestCase
from unittest.mock import patch
from molecupy.pdb.pdbfile import PdbFile
from molecupy.pdb.pdbdatafile import PdbDataFile
from molecupy.converters.pdbfile2pdbdatafile import pdb_data_file_from_pdb_file

class PdbDataFileTest(TestCase):

    def setUp(self):
        self.blank = PdbDataFile()



class PdbDataFileCreationTests(PdbDataFileTest):

    def test_can_create_empty_data_file(self):
        data_file = PdbDataFile()

        self.assertEqual(data_file._classification, None)
        self.assertEqual(data_file._deposition_date, None)
        self.assertEqual(data_file._pdb_code, None)
        self.assertFalse(data_file._is_obsolete)
        self.assertEqual(data_file._obsolete_date, None)
        self.assertEqual(data_file._replacement_code, None)
        self.assertEqual(data_file._title, None)
        self.assertEqual(data_file._split_codes, [])
        self.assertEqual(data_file._caveat, None)
        self.assertEqual(data_file._compounds, [])
        self.assertEqual(data_file._sources, [])
        self.assertEqual(data_file._keywords, [])
        self.assertEqual(data_file._experimental_techniques, [])
        self.assertEqual(data_file._model_count, 1)
        self.assertEqual(data_file._model_annotations, [])
        self.assertEqual(data_file._authors, [])
        self.assertEqual(data_file._revisions, [])
        self.assertEqual(data_file._supercedes, [])
        self.assertEqual(data_file._supercede_date, None)
        self.assertEqual(data_file._journal, None)
        self.assertEqual(data_file._remarks, [])

        self.assertEqual(data_file._dbreferences, [])
        self.assertEqual(data_file._sequence_differences, [])
        self.assertEqual(data_file._residue_sequences, [])
        self.assertEqual(data_file._modified_residues, [])

        self.assertEqual(data_file._hets, [])
        self.assertEqual(data_file._het_names, {})
        self.assertEqual(data_file._het_synonyms, {})
        self.assertEqual(data_file._formulae, {})

        self.assertEqual(data_file._helices, [])
        self.assertEqual(data_file._sheets, [])

        self.assertEqual(data_file._ss_bonds, [])
        self.assertEqual(data_file._links, [])
        self.assertEqual(data_file._cis_peptides, [])

        self.assertEqual(data_file._sites, [])

        self.assertEqual(data_file._crystal, None)
        self.assertEqual(data_file._origix, None)
        self.assertEqual(data_file._scale, None)
        self.assertEqual(data_file._matrix, None)

        self.assertEqual(
         data_file._models,
         [{"model_id": 1, "start_record": -1, "end_record": -1}]
        )
        self.assertEqual(data_file._atoms, [])
        self.assertEqual(data_file._anisou, [])
        self.assertEqual(data_file._termini, [])
        self.assertEqual(data_file._heteroatoms, [])

        self.assertEqual(data_file._connections, [])

        self.assertEqual(data_file._master, None)


    def test_repr(self):
        data_file = PdbDataFile()
        self.assertEqual(str(data_file), "<PdbDataFile (????)>")


    def test_repr_when_there_is_pdb_code(self):
        data_file = PdbDataFile()
        data_file._pdb_code = "ABCD"
        self.assertEqual(str(data_file), "<PdbDataFile (ABCD)>")



class TitleSectionPropertyTests(PdbDataFileTest):

    def test_header_properties(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "HEADER    LYASE                                   06-MAY-02   1LOL"
        ))
        self.assertIs(data_file._classification, data_file.classification())
        self.assertIs(data_file._deposition_date, data_file.deposition_date())
        self.assertIs(data_file._pdb_code, data_file.pdb_code())


    def test_can_modify_header_properties(self):
        self.blank.classification("TEST CLASS")
        self.blank.deposition_date(datetime.datetime(2008, 1, 24).date())
        self.blank.pdb_code("1xxx")
        self.assertEqual(self.blank._classification, "TEST CLASS")
        self.assertEqual(
         self.blank._deposition_date,
         datetime.datetime(2008, 1, 24).date()
        )
        self.assertEqual(self.blank._pdb_code, "1xxx")


    def test_classification_must_be_str(self):
        with self.assertRaises(TypeError):
            self.blank.classification(1000)


    def test_classifcation_must_be_less_than_40_chars(self):
        with self.assertRaises(ValueError):
            self.blank.classification("-" * 41)


    def test_deposition_date_must_be_date(self):
        with self.assertRaises(TypeError):
            self.blank.deposition_date("1-1-91")


    def test_pdb_code_must_be_string(self):
        with self.assertRaises(TypeError):
            self.blank.pdb_code(1000)


    def test_pdb_code_must_be_4_chars(self):
        with self.assertRaises(ValueError):
            self.blank.pdb_code("1xx")
        with self.assertRaises(ValueError):
            self.blank.pdb_code("1xxxx")


    def test_obslte_properties(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "OBSLTE     30-SEP-93 1LOL      1SAM"
        ))
        self.assertIs(data_file._is_obsolete, data_file.is_obsolete())
        self.assertIs(data_file._obsolete_date, data_file.obsolete_date())
        self.assertIs(data_file._replacement_code, data_file.replacement_code())


    def test_can_modify_obslte_properties(self):
        self.blank.is_obsolete(True)
        self.blank.obsolete_date(datetime.datetime(2008, 1, 24).date())
        self.blank.replacement_code("1xxx")
        self.assertTrue(self.blank._is_obsolete)
        self.assertEqual(
         self.blank._obsolete_date,
         datetime.datetime(2008, 1, 24).date()
        )
        self.assertEqual(self.blank._replacement_code, "1xxx")


    def test_is_obsolete_must_be_bool(self):
        with self.assertRaises(TypeError):
            self.blank.is_obsolete("yes")


    def test_obsolete_date_must_be_date(self):
        with self.assertRaises(TypeError):
            self.blank.obsolete_date("1-1-91")


    def test_replacement_code_must_be_string(self):
        with self.assertRaises(TypeError):
            self.blank.replacement_code(1000)


    def test_replacement_code_must_be_4_chars(self):
        with self.assertRaises(ValueError):
            self.blank.replacement_code("1xx")
        with self.assertRaises(ValueError):
            self.blank.replacement_code("1xxxx")


    def test_title_properties(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "TITLE     CRYSTAL STRUCTURE OF OROTIDINE MONOPHOSPHATE DECARBOXYLASE\n"
         "TITLE    2 COMPLEX WITH XMP"
        ))
        self.assertIs(data_file._title, data_file.title())


    def test_can_modify_title_properties(self):
        self.blank.title("123" * 10)
        self.assertEqual(self.blank.title(), "123" * 10)


    def test_title_must_be_str(self):
        with self.assertRaises(TypeError):
            self.blank.title(100)


    def test_split_properties(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "SPLIT      1VOQ 1VOR 1VOS 1VOU 1VOV 1VOW 1VOX 1VOY 1VP0 1VOZ 1VOY 1VP0 1VOZ 1VOZ\n"
         "SPLIT      1VOQ 1VOR 1VOS 1VOU 1VOV 1VOW 1VOX 1VOY 1VP0 1VOZ"
        ))
        self.assertIs(data_file._split_codes, data_file.split_codes())


    def test_caveat_properties(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "TITLE     CRYSTAL STRUCTURE OF OROTIDINE MONOPHOSPHATE DECARBOXYLASE\n"
         "TITLE    2 COMPLEX WITH XMP"
        ))
        self.assertIs(data_file._caveat, data_file.caveat())


    def test_can_modify_caveat_properties(self):
        self.blank.caveat("123" * 10)
        self.assertEqual(self.blank.caveat(), "123" * 10)


    def test_caveat_must_be_str(self):
        with self.assertRaises(TypeError):
            self.blank.caveat(100)


    def test_compnd_properties(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "COMPND    MOL_ID: 1;\n"
         "COMPND   2 MOLECULE: OROTIDINE 5'-MONOPHOSPHATE DECARBOXYLASE;\n"
        ))
        self.assertIs(data_file._compounds, data_file.compounds())


    def test_source_properties(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "SOURCE    MOL_ID: 1;\n"
         "SOURCE   2 ORGANISM_SCIENTIFIC: METHANOTHERMOBACTER\n"
        ))
        self.assertIs(data_file._sources, data_file.sources())


    def test_keyword_properties(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "SOURCE    MOL_ID: 1;\n"
         "SOURCE   2 ORGANISM_SCIENTIFIC: METHANOTHERMOBACTER\n"
        ))
        self.assertIs(data_file._keywords, data_file.keywords())


    def test_expdta_properties(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "SOURCE    MOL_ID: 1;\n"
         "SOURCE   2 ORGANISM_SCIENTIFIC: METHANOTHERMOBACTER\n"
        ))
        self.assertIs(
         data_file._experimental_techniques,
         data_file.experimental_techniques()
        )


    def test_nummdl_properties(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "NUMMDL    2"
        ))
        self.assertIs(data_file._model_count, data_file.model_count())


    def test_can_modify_nummdl_properties(self):
        self.blank.model_count(9)
        self.assertEqual(self.blank.model_count(), 9)


    def test_nummdl_must_be_int(self):
        with self.assertRaises(TypeError):
            self.blank.model_count("1")
        with self.assertRaises(TypeError):
            self.blank.model_count(9.8)


    def test_mdltyp_properties(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "MDLTYP    CA ATOMS ONLY, CHAIN A, B, C, D, E, F, G, H, I, J, K ; P ATOMS ONLY,\n"
         "MDLTYP   2 CHAIN X, Y, Z"
        ))
        self.assertIs(
         data_file._model_annotations,
         data_file.model_annotations()
        )


    def test_author_properties(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "AUTHOR    M.B.BERRY,B.MEADOR,T.BILDERBACK,P.LIANG,M.GLASER,\n"
         "AUTHOR   2 G.N.PHILLIPS JR.,T.L.ST. STEVENS"
        ))
        self.assertIs(data_file._authors, data_file.authors())


    def test_revdat_properties(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "REVDAT   4 1 24-FEB-09 1LOL    1       VERSN  COMPND EXPDTA CAVEAT\n"
         "REVDAT   4 2                   1       SOURCE JRNL\n"
        ))
        self.assertIs(data_file._revisions, data_file.revisions())


    def test_sprsde_properties(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "SPRSDE     27-FEB-95 1GDJ      1LH4 2LH4"
        ))
        self.assertIs(data_file._supercedes, data_file.supercedes())
        self.assertIs(data_file._supercede_date, data_file.supercede_date())


    def test_can_modify_sprsde_properties(self):
        self.blank.supercede_date(datetime.datetime(2008, 1, 24).date())
        self.assertEqual(
         self.blank.supercede_date(),
         datetime.datetime(2008, 1, 24).date()
        )


    def test_supercede_date_must_be_date(self):
        with self.assertRaises(TypeError):
            self.blank.supercede_date("1-1-91")


    def test_jrnl_properties(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "JRNL        REF    J.BIOL.CHEM.                  V. 277 28080 2002"
        ))
        self.assertEqual(data_file._journal, data_file.journal())


    def test_can_modify_jrnl_properties(self):
        self.blank.journal({"authors": ["N.WU", "E.F.PAI"]})
        self.assertEqual(self.blank.journal(), {"authors": ["N.WU", "E.F.PAI"]})


    def test_journal_must_be_dict(self):
        with self.assertRaises(TypeError):
            self.blank.journal("aaa")


    def test_remark_properties(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "REMARK   2\n"
         "REMARK   2 RESOLUTION.    1.90 ANGSTROMS."
        ))
        self.assertEqual(data_file._remarks, data_file.remarks())


    def test_can_get_remark_by_number(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "REMARK   2\n"
         "REMARK 999\n"
         "REMARK   2 RESOLUTION.    1.90 ANGSTROMS."
        ))
        self.assertEqual(
         data_file.get_remark_by_number(2),
         {
          "number": 2,
          "content": "RESOLUTION.    1.90 ANGSTROMS."
         }
        )
        self.assertEqual(data_file.get_remark_by_number(3), None)



class PrimaryStructureSectionPropertyTests(PdbDataFileTest):

    def test_dbref_properties(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "DBREF1 1LOL C   61   322  GB                   AE017221\n"
         "DBREF2 1LOL C     46197919                      1534489     1537377"
        ))
        self.assertEqual(data_file._dbreferences, data_file.dbreferences())


    def test_seqadv_properties(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "SEQADV 1LOL GLU A  229  UNP  O26232              INSERTION\n"
         "SEQADV 1LOL GLU B 1229  UNP  O26232              INSERTION"
        ))
        self.assertEqual(
         data_file._sequence_differences,
         data_file.sequence_differences()
        )


    def test_seqres_properties(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "SEQRES   1 A    8  LEU ARG SER ARG ARG VAL ASP VAL MET ASP VAL MET ASN\n"
         "SEQRES   2 A    8  ARG LEU ILE\n"
        ))
        self.assertEqual(
         data_file._residue_sequences,
         data_file.residue_sequences()
        )



    def test_modres_properties(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "MODRES 1LOL ASP A   10  ASP  GLYCOSYLATION SITE"
        ))
        self.assertEqual(
         data_file._modified_residues,
         data_file.modified_residues()
        )



class HeterogenSectionPropertyTests(PdbDataFileTest):

    def test_het_properties(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "HET    BU2  A5001       6\n"
         "HET    BU2  B5002       6\n"
         "HET    XMP  A2001      24\n"
         "HET    XMP  B2002      24"
        ))
        self.assertEqual(data_file._hets, data_file.hets())


    def test_hetnam_properties(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "HETNAM     BU2 1,3-BUTANEDIOL\n"
         "HETNAM     XMP XANTHOSINE-5'-MONOPHOSPHATE"
        ))
        self.assertEqual(data_file._het_names, data_file.het_names())


    def test_hetsyn_properties(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "HETSYN     BU2 BOOM BOOM BOMB; WYRDSTUFF\n"
         "HETSYN     XMP 5-MONOPHOSPHATE-9-BETA-D-RIBOFURANOSYL XANTHINE"
        ))
        self.assertEqual(data_file._het_synonyms, data_file.het_synonyms())


    def test_formul_properties(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "FORMUL   3  BU2    2(C4 H10 O2)\n"
        ))
        self.assertEqual(data_file._formulae, data_file.formulae())



class SecondaryStructurePropertyTests(PdbDataFileTest):

    def test_helix_properties(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "HELIX    1   1 VAL A   11  ASN A   13  5                                   3\n"
         "HELIX    2   2 ASN A   23  ARG A   35  1                                  13"
        ))
        self.assertEqual(data_file._helices, data_file.helices())


    def test_sheet_properties(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "SHEET    1   A 2 LEU A  15  MET A  19  0\n"
         "SHEET    2   A 2 THR A  40  GLY A  44  1  O  LYS A  42   N  LEU A  17"
        ))
        self.assertEqual(data_file._sheets, data_file.sheets())



class ConnectivityAnnotationPropertyTests(PdbDataFileTest):

    def test_ssbond_properties(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "SSBOND   1 CYS A  123    CYS A  155                          1555   1555  2.04"
        ))
        self.assertEqual(data_file._ss_bonds, data_file.ss_bonds())


    def test_link_properties(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "LINK         O   TYR A 146                 K     K A 501     1555   1555  2.75"
        ))
        self.assertEqual(data_file._links, data_file.links())


    def test_cispep_properties(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "CISPEP     ASP B 1188    PRO B 1189          0         0.35"
        ))
        self.assertEqual(data_file._cis_peptides, data_file.cis_peptides())



class MiscellaneousSectionPropertyTests(PdbDataFileTest):

    def test_site_properties(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "SITE     1 AC1  6 ASP A  70  LYS A  72  LEU A 123  VAL A 155"
        ))
        self.assertEqual(data_file._sites, data_file.sites())


'''
class CrystalRecordTests(PdbDataFileTest):

    def test_missing_crystal_processing(self):
        self.assertEqual(self.empty._crystal_a, None)
        self.assertEqual(self.empty._crystal_b, None)
        self.assertEqual(self.empty._crystal_c, None)
        self.assertEqual(self.empty._crystal_alpha, None)
        self.assertEqual(self.empty._crystal_beta, None)
        self.assertEqual(self.empty._crystal_gamma, None)
        self.assertEqual(self.empty._crystal_s_group, None)
        self.assertEqual(self.empty._crystal_z, None)
        self.assertEqual(self.blank._crystal_a, None)
        self.assertEqual(self.blank._crystal_b, None)
        self.assertEqual(self.blank._crystal_c, None)
        self.assertEqual(self.blank._crystal_alpha, None)
        self.assertEqual(self.blank._crystal_beta, None)
        self.assertEqual(self.blank._crystal_gamma, None)
        self.assertEqual(self.blank._crystal_s_group, None)
        self.assertEqual(self.blank._crystal_z, None)


    def test_crystal_record_processing(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "CRYST1   57.570   55.482   66.129  90.00  94.28  90.00 P 1 21 1      4"
        ))
        self.assertEqual(data_file._crystal_a, 57.57)
        self.assertEqual(data_file._crystal_b, 55.482)
        self.assertEqual(data_file._crystal_c, 66.129)
        self.assertEqual(data_file._crystal_alpha, 90.0)
        self.assertEqual(data_file._crystal_beta, 94.28)
        self.assertEqual(data_file._crystal_gamma, 90.0)
        self.assertEqual(data_file._crystal_s_group, "P 1 21 1")
        self.assertEqual(data_file._crystal_z, 4)


    def test_crystal_properties(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "CRYST1   57.570   55.482   66.129  90.00  94.28  90.00 P 1 21 1      4"
        ))
        self.assertEqual(data_file._crystal_a, data_file.crystal_a())
        self.assertEqual(data_file._crystal_b, data_file.crystal_b())
        self.assertEqual(data_file._crystal_c, data_file.crystal_c())
        self.assertEqual(data_file._crystal_beta, data_file.crystal_beta())
        self.assertEqual(data_file._crystal_alpha, data_file.crystal_alpha())
        self.assertEqual(data_file._crystal_gamma, data_file.crystal_gamma())
        self.assertEqual(data_file._crystal_s_group, data_file.crystal_s_group())
        self.assertEqual(data_file._crystal_z, data_file.crystal_z())


    def test_can_modify_crystal_properties(self):
        self.blank.crystal_a(57.57)
        self.blank.crystal_b(55.482)
        self.blank.crystal_c(66.129)
        self.blank.crystal_alpha(90.0)
        self.blank.crystal_beta(94.28)
        self.blank.crystal_gamma(90.0)
        self.blank.crystal_s_group("P 1 21 1")
        self.blank.crystal_z(4)
        self.assertEqual(self.blank._crystal_a, 57.57)
        self.assertEqual(self.blank._crystal_b, 55.482)
        self.assertEqual(self.blank._crystal_c, 66.129)
        self.assertEqual(self.blank._crystal_alpha, 90.0)
        self.assertEqual(self.blank._crystal_beta, 94.28)
        self.assertEqual(self.blank._crystal_gamma, 90.0)
        self.assertEqual(self.blank._crystal_s_group, "P 1 21 1")
        self.assertEqual(self.blank._crystal_z, 4)


    def test_crystal_a_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.crystal_a("aaa")


    def test_crystal_b_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.crystal_b("aaa")


    def test_crystal_c_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.crystal_c("aaa")


    def test_crystal_alpha_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.crystal_alpha("aaa")


    def test_crystal_beta_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.crystal_beta("aaa")


    def test_crystal_gamma_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.crystal_gamma("aaa")


    def test_crystal_s_group_must_be_str(self):
        with self.assertRaises(TypeError):
            self.blank.crystal_s_group(1.5)


    def test_crystal_z_must_be_int(self):
        with self.assertRaises(TypeError):
            self.blank.crystal_z(1.5)



class OrigxRecordTests(PdbDataFileTest):

    def test_missing_origx_processing(self):
        self.assertEqual(self.empty._origx_o11, None)
        self.assertEqual(self.empty._origx_o12, None)
        self.assertEqual(self.empty._origx_o13, None)
        self.assertEqual(self.empty._origx_t1, None)
        self.assertEqual(self.empty._origx_o21, None)
        self.assertEqual(self.empty._origx_o22, None)
        self.assertEqual(self.empty._origx_o23, None)
        self.assertEqual(self.empty._origx_t2, None)
        self.assertEqual(self.empty._origx_o31, None)
        self.assertEqual(self.empty._origx_o32, None)
        self.assertEqual(self.empty._origx_o33, None)
        self.assertEqual(self.empty._origx_t3, None)
        self.assertEqual(self.blank._origx_o11, None)
        self.assertEqual(self.blank._origx_o12, None)
        self.assertEqual(self.blank._origx_o13, None)
        self.assertEqual(self.blank._origx_t1, None)
        self.assertEqual(self.blank._origx_o21, None)
        self.assertEqual(self.blank._origx_o22, None)
        self.assertEqual(self.blank._origx_o23, None)
        self.assertEqual(self.blank._origx_t2, None)
        self.assertEqual(self.blank._origx_o31, None)
        self.assertEqual(self.blank._origx_o32, None)
        self.assertEqual(self.blank._origx_o33, None)
        self.assertEqual(self.blank._origx_t3, None)


    def test_origx_record_processing(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "ORIGX1      0.963457  0.136613  0.230424       16.61000\n"
         "ORIGX2     -0.158977  0.983924  0.081383       13.72000\n"
         "ORIGX3     -0.215598 -0.115048  0.969683       37.65000"
        ))
        self.assertEqual(data_file._origx_o11, 0.963457)
        self.assertEqual(data_file._origx_o12, 0.136613)
        self.assertEqual(data_file._origx_o13, 0.230424)
        self.assertEqual(data_file._origx_t1, 16.61)
        self.assertEqual(data_file._origx_o21, -0.158977)
        self.assertEqual(data_file._origx_o22, 0.983924)
        self.assertEqual(data_file._origx_o23, 0.081383)
        self.assertEqual(data_file._origx_t2, 13.72)
        self.assertEqual(data_file._origx_o31, -0.215598)
        self.assertEqual(data_file._origx_o32, -0.115048)
        self.assertEqual(data_file._origx_o33, 0.969683)
        self.assertEqual(data_file._origx_t3, 37.65)


    def test_origx_properties(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "ORIGX1      0.963457  0.136613  0.230424       16.61000\n"
         "ORIGX2     -0.158977  0.983924  0.081383       13.72000\n"
         "ORIGX3     -0.215598 -0.115048  0.969683       37.65000"
        ))
        self.assertEqual(data_file._origx_o11, data_file.origx_o11())
        self.assertEqual(data_file._origx_o12, data_file.origx_o12())
        self.assertEqual(data_file._origx_o13, data_file.origx_o13())
        self.assertEqual(data_file._origx_t1, data_file.origx_t1())
        self.assertEqual(data_file._origx_o21, data_file.origx_o21())
        self.assertEqual(data_file._origx_o22, data_file.origx_o22())
        self.assertEqual(data_file._origx_o23, data_file.origx_o23())
        self.assertEqual(data_file._origx_t2, data_file.origx_t2())
        self.assertEqual(data_file._origx_o31, data_file.origx_o31())
        self.assertEqual(data_file._origx_o32, data_file.origx_o32())
        self.assertEqual(data_file._origx_o33, data_file.origx_o33())
        self.assertEqual(data_file._origx_t3, data_file.origx_t3())


    def test_can_modify_origx_properties(self):
        self.blank.origx_o11(0.963457)
        self.blank.origx_o12(0.136613)
        self.blank.origx_o13(0.230424)
        self.blank.origx_t1(16.61)
        self.blank.origx_o21(-0.158977)
        self.blank.origx_o22(0.983924)
        self.blank.origx_o23(0.081383)
        self.blank.origx_t2(13.72)
        self.blank.origx_o31(-0.215598)
        self.blank.origx_o32(-0.115048)
        self.blank.origx_o33(0.969683)
        self.blank.origx_t3(37.65)
        self.assertEqual(self.blank._origx_o11, 0.963457)
        self.assertEqual(self.blank._origx_o12, 0.136613)
        self.assertEqual(self.blank._origx_o13, 0.230424)
        self.assertEqual(self.blank._origx_t1, 16.61)
        self.assertEqual(self.blank._origx_o21, -0.158977)
        self.assertEqual(self.blank._origx_o22, 0.983924)
        self.assertEqual(self.blank._origx_o23, 0.081383)
        self.assertEqual(self.blank._origx_t2, 13.72)
        self.assertEqual(self.blank._origx_o31, -0.215598)
        self.assertEqual(self.blank._origx_o32, -0.115048)
        self.assertEqual(self.blank._origx_o33, 0.969683)
        self.assertEqual(self.blank._origx_t3, 37.65)


    def test_origx_o11_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.origx_o11("...")


    def test_origx_o12_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.origx_o12("...")


    def test_origx_o13_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.origx_o13("...")


    def test_origx_t1_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.origx_t1("...")


    def test_origx_o21_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.origx_o21("...")


    def test_origx_o22_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.origx_o22("...")


    def test_origx_o23_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.origx_o23("...")


    def test_origx_t2_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.origx_t2("...")


    def test_origx_o31_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.origx_o31("...")


    def test_origx_o32_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.origx_o32("...")


    def test_origx_o33_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.origx_o33("...")


    def test_origx_t3_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.origx_t3("...")



class ScaleRecordTests(PdbDataFileTest):

    def test_missing_scale_processing(self):
        self.assertEqual(self.empty._scale_s11, None)
        self.assertEqual(self.empty._scale_s12, None)
        self.assertEqual(self.empty._scale_s13, None)
        self.assertEqual(self.empty._scale_u1, None)
        self.assertEqual(self.empty._scale_s21, None)
        self.assertEqual(self.empty._scale_s22, None)
        self.assertEqual(self.empty._scale_s23, None)
        self.assertEqual(self.empty._scale_u2, None)
        self.assertEqual(self.empty._scale_s31, None)
        self.assertEqual(self.empty._scale_s32, None)
        self.assertEqual(self.empty._scale_s33, None)
        self.assertEqual(self.empty._scale_u3, None)
        self.assertEqual(self.blank._scale_s11, None)
        self.assertEqual(self.blank._scale_s12, None)
        self.assertEqual(self.blank._scale_s13, None)
        self.assertEqual(self.blank._scale_u1, None)
        self.assertEqual(self.blank._scale_s21, None)
        self.assertEqual(self.blank._scale_s22, None)
        self.assertEqual(self.blank._scale_s23, None)
        self.assertEqual(self.blank._scale_u2, None)
        self.assertEqual(self.blank._scale_s31, None)
        self.assertEqual(self.blank._scale_s32, None)
        self.assertEqual(self.blank._scale_s33, None)
        self.assertEqual(self.blank._scale_u3, None)


    def test_scale_record_processing(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "SCALE1      0.963457  0.136613  0.230424       16.61000\n"
         "SCALE2     -0.158977  0.983924  0.081383       13.72000\n"
         "SCALE3     -0.215598 -0.115048  0.969683       37.65000"
        ))
        self.assertEqual(data_file._scale_s11, 0.963457)
        self.assertEqual(data_file._scale_s12, 0.136613)
        self.assertEqual(data_file._scale_s13, 0.230424)
        self.assertEqual(data_file._scale_u1, 16.61)
        self.assertEqual(data_file._scale_s21, -0.158977)
        self.assertEqual(data_file._scale_s22, 0.983924)
        self.assertEqual(data_file._scale_s23, 0.081383)
        self.assertEqual(data_file._scale_u2, 13.72)
        self.assertEqual(data_file._scale_s31, -0.215598)
        self.assertEqual(data_file._scale_s32, -0.115048)
        self.assertEqual(data_file._scale_s33, 0.969683)
        self.assertEqual(data_file._scale_u3, 37.65)


    def test_scale_properties(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "SCALE1      0.963457  0.136613  0.230424       16.61000\n"
         "SCALE2     -0.158977  0.983924  0.081383       13.72000\n"
         "SCALE3     -0.215598 -0.115048  0.969683       37.65000"
        ))
        self.assertEqual(data_file._scale_s11, data_file.scale_s11())
        self.assertEqual(data_file._scale_s12, data_file.scale_s12())
        self.assertEqual(data_file._scale_s13, data_file.scale_s13())
        self.assertEqual(data_file._scale_u1, data_file.scale_u1())
        self.assertEqual(data_file._scale_s21, data_file.scale_s21())
        self.assertEqual(data_file._scale_s22, data_file.scale_s22())
        self.assertEqual(data_file._scale_s23, data_file.scale_s23())
        self.assertEqual(data_file._scale_u2, data_file.scale_u2())
        self.assertEqual(data_file._scale_s31, data_file.scale_s31())
        self.assertEqual(data_file._scale_s32, data_file.scale_s32())
        self.assertEqual(data_file._scale_s33, data_file.scale_s33())
        self.assertEqual(data_file._scale_u3, data_file.scale_u3())


    def test_can_modify_scale_properties(self):
        self.blank.scale_s11(0.963457)
        self.blank.scale_s12(0.136613)
        self.blank.scale_s13(0.230424)
        self.blank.scale_u1(16.61)
        self.blank.scale_s21(-0.158977)
        self.blank.scale_s22(0.983924)
        self.blank.scale_s23(0.081383)
        self.blank.scale_u2(13.72)
        self.blank.scale_s31(-0.215598)
        self.blank.scale_s32(-0.115048)
        self.blank.scale_s33(0.969683)
        self.blank.scale_u3(37.65)
        self.assertEqual(self.blank._scale_s11, 0.963457)
        self.assertEqual(self.blank._scale_s12, 0.136613)
        self.assertEqual(self.blank._scale_s13, 0.230424)
        self.assertEqual(self.blank._scale_u1, 16.61)
        self.assertEqual(self.blank._scale_s21, -0.158977)
        self.assertEqual(self.blank._scale_s22, 0.983924)
        self.assertEqual(self.blank._scale_s23, 0.081383)
        self.assertEqual(self.blank._scale_u2, 13.72)
        self.assertEqual(self.blank._scale_s31, -0.215598)
        self.assertEqual(self.blank._scale_s32, -0.115048)
        self.assertEqual(self.blank._scale_s33, 0.969683)
        self.assertEqual(self.blank._scale_u3, 37.65)


    def test_scale_s11_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.scale_s11("...")


    def test_scale_s12_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.scale_s12("...")


    def test_scale_s13_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.scale_s13("...")


    def test_scale_u1_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.scale_u1("...")


    def test_scale_s21_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.scale_s21("...")


    def test_scale_s22_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.scale_s22("...")


    def test_scale_s23_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.scale_s23("...")


    def test_scale_u2_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.scale_u2("...")


    def test_scale_s31_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.scale_s31("...")


    def test_scale_s32_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.scale_s32("...")


    def test_scale_s33_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.scale_s33("...")


    def test_scale_u3_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.scale_u3("...")



class MtrixRecordTests(PdbDataFileTest):

    def test_missing_matrix_processing(self):
        self.assertEqual(self.empty._matrix_serial_1, None)
        self.assertEqual(self.empty._matrix_m11, None)
        self.assertEqual(self.empty._matrix_m12, None)
        self.assertEqual(self.empty._matrix_m13, None)
        self.assertEqual(self.empty._matrix_v1, None)
        self.assertEqual(self.empty._matrix_i_given_1, None)
        self.assertEqual(self.empty._matrix_serial_2, None)
        self.assertEqual(self.empty._matrix_m21, None)
        self.assertEqual(self.empty._matrix_m22, None)
        self.assertEqual(self.empty._matrix_m23, None)
        self.assertEqual(self.empty._matrix_v2, None)
        self.assertEqual(self.empty._matrix_i_given_2, None)
        self.assertEqual(self.empty._matrix_serial_3, None)
        self.assertEqual(self.empty._matrix_m31, None)
        self.assertEqual(self.empty._matrix_m32, None)
        self.assertEqual(self.empty._matrix_m33, None)
        self.assertEqual(self.empty._matrix_v3, None)
        self.assertEqual(self.empty._matrix_i_given_3, None)
        self.assertEqual(self.empty._matrix_serial_1, None)
        self.assertEqual(self.blank._matrix_m11, None)
        self.assertEqual(self.blank._matrix_m12, None)
        self.assertEqual(self.blank._matrix_m13, None)
        self.assertEqual(self.blank._matrix_v1, None)
        self.assertEqual(self.empty._matrix_i_given_1, None)
        self.assertEqual(self.empty._matrix_serial_2, None)
        self.assertEqual(self.blank._matrix_m21, None)
        self.assertEqual(self.blank._matrix_m22, None)
        self.assertEqual(self.blank._matrix_m23, None)
        self.assertEqual(self.blank._matrix_v2, None)
        self.assertEqual(self.empty._matrix_i_given_2, None)
        self.assertEqual(self.empty._matrix_serial_3, None)
        self.assertEqual(self.blank._matrix_m31, None)
        self.assertEqual(self.blank._matrix_m32, None)
        self.assertEqual(self.blank._matrix_m33, None)
        self.assertEqual(self.blank._matrix_v3, None)
        self.assertEqual(self.empty._matrix_i_given_1, None)


    def test_mtrix_record_processing(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "MTRIX1   1 -1.000000  0.000000  0.000000        0.00000    1\n"
         "MTRIX2   1  0.000000  1.000000  0.000000        0.00000    1\n"
         "MTRIX3   1  0.000000  0.000000 -1.000000        0.00000    1"
        ))
        self.assertEqual(data_file._matrix_serial_1, 1)
        self.assertEqual(data_file._matrix_m11, -1.0)
        self.assertEqual(data_file._matrix_m12, 0.0)
        self.assertEqual(data_file._matrix_m13, 0.0)
        self.assertEqual(data_file._matrix_v1, 0.0)
        self.assertIs(data_file._matrix_i_given_1, True)
        self.assertEqual(data_file._matrix_serial_2, 1)
        self.assertEqual(data_file._matrix_m21, 0.0)
        self.assertEqual(data_file._matrix_m22, 1.0)
        self.assertEqual(data_file._matrix_m23, 0.0)
        self.assertEqual(data_file._matrix_v2, 0.0)
        self.assertIs(data_file._matrix_i_given_2, True)
        self.assertEqual(data_file._matrix_serial_3, 1)
        self.assertEqual(data_file._matrix_m31, 0.0)
        self.assertEqual(data_file._matrix_m32, 0.0)
        self.assertEqual(data_file._matrix_m33, -1.0)
        self.assertEqual(data_file._matrix_v3, 0.0)
        self.assertIs(data_file._matrix_i_given_3, True)


    def test_mtrix_properties(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "MTRIX1   1 -1.000000  0.000000  0.000000        0.00000    1\n"
         "MTRIX2   1  0.000000  1.000000  0.000000        0.00000    1\n"
         "MTRIX3   1  0.000000  0.000000 -1.000000        0.00000    1"
        ))
        self.assertEqual(data_file._matrix_serial_1, data_file.matrix_serial_1())
        self.assertEqual(data_file._matrix_m11, data_file.matrix_m11())
        self.assertEqual(data_file._matrix_m12, data_file.matrix_m12())
        self.assertEqual(data_file._matrix_m13, data_file.matrix_m13())
        self.assertEqual(data_file._matrix_v1, data_file.matrix_v1())
        self.assertEqual(data_file._matrix_i_given_1, data_file.matrix_i_given_1())
        self.assertEqual(data_file._matrix_serial_2, data_file.matrix_serial_2())
        self.assertEqual(data_file._matrix_m21, data_file.matrix_m21())
        self.assertEqual(data_file._matrix_m22, data_file.matrix_m22())
        self.assertEqual(data_file._matrix_m23, data_file.matrix_m23())
        self.assertEqual(data_file._matrix_v2, data_file.matrix_v2())
        self.assertEqual(data_file._matrix_i_given_2, data_file.matrix_i_given_2())
        self.assertEqual(data_file._matrix_serial_3, data_file.matrix_serial_3())
        self.assertEqual(data_file._matrix_m31, data_file.matrix_m31())
        self.assertEqual(data_file._matrix_m32, data_file.matrix_m32())
        self.assertEqual(data_file._matrix_m33, data_file.matrix_m33())
        self.assertEqual(data_file._matrix_v3, data_file.matrix_v3())
        self.assertEqual(data_file._matrix_i_given_3, data_file.matrix_i_given_3())


    def test_can_modify_mtrx_properties(self):
        self.blank.matrix_serial_1(1)
        self.blank.matrix_m11(-1.0)
        self.blank.matrix_m12(0.0)
        self.blank.matrix_m13(0.0)
        self.blank.matrix_v1(0.0)
        self.blank.matrix_i_given_1(True)
        self.blank.matrix_serial_2(1)
        self.blank.matrix_m21(0.0)
        self.blank.matrix_m22(1.0)
        self.blank.matrix_m23(0.0)
        self.blank.matrix_v2(0.0)
        self.blank.matrix_i_given_2(True)
        self.blank.matrix_serial_3(1)
        self.blank.matrix_m31(0.0)
        self.blank.matrix_m32(0.0)
        self.blank.matrix_m33(-1.0)
        self.blank.matrix_v3(0.0)
        self.blank.matrix_i_given_3(True)
        self.assertEqual(self.blank._matrix_serial_1, 1)
        self.assertEqual(self.blank._matrix_m11, -1.0)
        self.assertEqual(self.blank._matrix_m12, 0.0)
        self.assertEqual(self.blank._matrix_m13, 0.0)
        self.assertEqual(self.blank._matrix_v1, 0.0)
        self.assertEqual(self.blank._matrix_i_given_1, True)
        self.assertEqual(self.blank._matrix_serial_2, 1)
        self.assertEqual(self.blank._matrix_m21, 0.0)
        self.assertEqual(self.blank._matrix_m22, 1.0)
        self.assertEqual(self.blank._matrix_m23, 0.0)
        self.assertEqual(self.blank._matrix_v2, 0.0)
        self.assertEqual(self.blank._matrix_i_given_2, True)
        self.assertEqual(self.blank._matrix_serial_3, 1)
        self.assertEqual(self.blank._matrix_m31, 0.0)
        self.assertEqual(self.blank._matrix_m32, 0.0)
        self.assertEqual(self.blank._matrix_m33, -1.0)
        self.assertEqual(self.blank._matrix_v3, 0.0)
        self.assertEqual(self.blank._matrix_i_given_3, True)


    def test_matrix_serial_1_must_be_int(self):
        with self.assertRaises(TypeError):
            self.blank.matrix_serial_1("...")


    def test_matrix_m11_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.matrix_m11("...")


    def test_matrix_m12_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.matrix_m12("...")


    def test_matrix_m13_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.matrix_m13("...")


    def test_matrix_v1_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.matrix_v1("...")


    def test_matrix_i_given_1_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.matrix_i_given_1("...")


    def test_matrix_serial_2_must_be_bool(self):
        with self.assertRaises(TypeError):
            self.blank.matrix_serial_2("...")


    def test_matrix_m21_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.matrix_m21("...")


    def test_matrix_m22_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.matrix_m22("...")


    def test_matrix_m23_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.matrix_m23("...")


    def test_matrix_v2_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.matrix_v2("...")


    def test_matrix_i_given_2_must_be_bool(self):
        with self.assertRaises(TypeError):
            self.blank.matrix_i_given_2("...")


    def test_matrix_serial_3_must_be_int(self):
        with self.assertRaises(TypeError):
            self.blank.matrix_serial_3("...")


    def test_matrix_m31_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.matrix_m31("...")


    def test_matrix_m32_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.matrix_m32("...")


    def test_matrix_m33_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.matrix_m33("...")


    def test_matrix_v3_must_be_float(self):
        with self.assertRaises(TypeError):
            self.blank.matrix_v3("...")


    def test_matrix_i_given_3_must_be_bool(self):
        with self.assertRaises(TypeError):
            self.blank.matrix_i_given_3("...")





class ModelRecordTests(PdbDataFileTest):

    def test_missing_model_processing(self):
        self.assertEqual(
         self.empty._models,
         [
          {
           "model_id": 1,
           "start_record": -1,
           "end_record": -1
          }
         ]
        )
        self.assertEqual(
         self.blank._models,
         [
          {
           "model_id": 1,
           "start_record": -1,
           "end_record": -1
          }
         ]
        )


    def test_model_processing(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "MODEL        1\n"
         "ATOM    107  N   GLY A  13      12.681  37.302 -25.211 1.000 15.56           N\n"
         "ENDMDL\n"
         "MODEL        2\n"
         "ATOM    107  N   GLY A  13      12.681  37.302 -25.211 1.000 15.56           N\n"
         "ENDMDL"
        ))
        self.assertEqual(
         data_file._models,
         [
          {
           "model_id": 1,
           "start_record": 1,
           "end_record": 3
          }, {
           "model_id": 2,
           "start_record": 4,
           "end_record": 6
          }
         ]
        )


    def test_model_properties(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "MODEL        1\n"
         "ATOM    107  N   GLY A  13      12.681  37.302 -25.211 1.000 15.56           N\n"
         "ENDMDL\n"
        ))
        self.assertEqual(data_file._models, data_file.models())



class AtomRecordTests(PdbDataFileTest):

    def test_missing_atom_processing(self):
        self.assertEqual(self.empty._atoms, [])
        self.assertEqual(self.blank._atoms, [])


    def test_atom_processing(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "ATOM    107  N   GLY A  13      12.681  37.302 -25.211 1.000 15.56           N\n"
         "ATOM    108  CA  GLY A  13      11.982  37.996 -26.241 1.000 16.92           C"
        ))
        self.assertEqual(
         data_file._atoms,
         [
          {
           "atom_id": 107,
           "atom_name": "N",
           "alt_loc": None,
           "residue_name": "GLY",
           "chain_id": "A",
           "residue_id": 13,
           "insert_code": "",
           "x": 12.681,
           "y": 37.302,
           "z": -25.211,
           "occupancy": 1.0,
           "temperature_factor": 15.56,
           "element": "N",
           "charge": None,
           "model_id": 1
          }, {
           "atom_id": 108,
           "atom_name": "CA",
           "alt_loc": None,
           "residue_name": "GLY",
           "chain_id": "A",
           "residue_id": 13,
           "insert_code": "",
           "x": 11.982,
           "y": 37.996,
           "z": -26.241,
           "occupancy": 1.0,
           "temperature_factor": 16.92,
           "element": "C",
           "charge": None,
           "model_id": 1
          }
         ]
        )


    def test_atom_properties(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "ATOM    107  N   GLY A  13      12.681  37.302 -25.211 1.000 15.56           N\n"
         "ATOM    108  CA  GLY A  13      11.982  37.996 -26.241 1.000 16.92           C"
        ))
        self.assertEqual(data_file._atoms, data_file.atoms())



class AnisouRecordTests(PdbDataFileTest):

    def test_missing_anisou_processing(self):
        self.assertEqual(self.empty._anisou, [])
        self.assertEqual(self.blank._anisou, [])


    def test_anisou_processing(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "ANISOU  107  N   GLY A  13     2406   1892   1614    198    519   -328       N\n"
         "ANISOU  108  CA  GLY A  13     2748   2004   1679    -21    155   -419       C"
        ))
        self.assertEqual(
         data_file._anisou,
         [
          {
           "atom_id": 107,
           "atom_name": "N",
           "alt_loc": None,
           "residue_name": "GLY",
           "chain_id": "A",
           "residue_id": 13,
           "insert_code": "",
           "u11": 2406,
           "u22": 1892,
           "u33": 1614,
           "u12": 198,
           "u13": 519,
           "u23": -328,
           "element": "N",
           "charge": None,
           "model_id": 1
          }, {
           "atom_id": 108,
           "atom_name": "CA",
           "alt_loc": None,
           "residue_name": "GLY",
           "chain_id": "A",
           "residue_id": 13,
           "insert_code": "",
           "u11": 2748,
           "u22": 2004,
           "u33": 1679,
           "u12": -21,
           "u13": 155,
           "u23": -419,
           "element": "C",
           "charge": None,
           "model_id": 1
          }
         ]
        )


    def test_anisou_properties(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "ANISOU  107  N   GLY A  13     2406   1892   1614    198    519   -328       N\n"
         "ANISOU  108  CA  GLY A  13     2748   2004   1679    -21    155   -419       C"
        ))
        self.assertEqual(data_file._anisou, data_file.anisou())



class TerRecordTests(PdbDataFileTest):

    def test_missing_ter_processing(self):
        self.assertEqual(self.empty._termini, [])
        self.assertEqual(self.blank._termini, [])


    def test_ter_processing(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "TER     109      GLY A  13"
        ))
        self.assertEqual(
         data_file._termini,
         [
          {
           "atom_id": 109,
           "residue_name": "GLY",
           "chain_id": "A",
           "residue_id": 13,
           "insert_code": "",
           "model_id": 1
          }
         ]
        )


    def test_ter_properties(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "TER     109      GLY A  13"
        ))
        self.assertEqual(data_file._termini, data_file.termini())



class HetatmRecordTests(PdbDataFileTest):

    def test_missing_hetatm_processing(self):
        self.assertEqual(self.empty._heteroatoms, [])
        self.assertEqual(self.blank._heteroatoms, [])


    def test_hetatm_processing(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "HETATM 8237 MG    MG A1001      13.872  -2.555 -29.045  1.00 27.36          MG"
        ))
        self.assertEqual(
         data_file._heteroatoms,
         [
          {
           "atom_id": 8237,
           "atom_name": "MG",
           "alt_loc": None,
           "residue_name": "MG",
           "chain_id": "A",
           "residue_id": 1001,
           "insert_code": "",
           "x": 13.872,
           "y": -2.555,
           "z": -29.045,
           "occupancy": 1.0,
           "temperature_factor": 27.36,
           "element": "MG",
           "charge": None,
           "model_id": 1
          }
         ]
        )


    def test_het_names_always_interpreted_as_string(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "HETATM 8237 MG   123 A1001      13.872  -2.555 -29.045  1.00 27.36          MG"
        ))
        self.assertEqual(
         data_file._heteroatoms,
         [
          {
           "atom_id": 8237,
           "atom_name": "MG",
           "alt_loc": None,
           "residue_name": "123",
           "chain_id": "A",
           "residue_id": 1001,
           "insert_code": "",
           "x": 13.872,
           "y": -2.555,
           "z": -29.045,
           "occupancy": 1.0,
           "temperature_factor": 27.36,
           "element": "MG",
           "charge": None,
           "model_id": 1
          }
         ]
        )


    def test_hetatm_properties(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "HETATM 8237 MG    MG A1001      13.872  -2.555 -29.045  1.00 27.36          MG"
        ))
        self.assertEqual(data_file._heteroatoms, data_file.heteroatoms())



class ConectRecordTests(PdbDataFileTest):

    def test_missing_conect_processing(self):
        self.assertEqual(self.empty._connections, [])
        self.assertEqual(self.blank._connections, [])


    def test_conect_processing(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "CONECT 1179  746 1184 1195 1203\n"
         "CONECT 1179 1211 1222"
        ))
        self.assertEqual(
         data_file._connections,
         [
          {
           "atom_id": 1179,
           "bonded_atoms": [746, 1184, 1195, 1203, 1211, 1222]
          }
         ]
        )


    def test_can_handle_conect_records_smushed_together(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "CONECT11056107961105711063"
        ))
        self.assertEqual(
         data_file._connections,
         [
          {
           "atom_id": 11056,
           "bonded_atoms": [10796, 11057, 11063]
          }
         ]
        )


    def test_conect_properties(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "CONECT 1179  746 1184 1195 1203\n"
         "CONECT 1179 1211 1222"
        ))
        self.assertEqual(data_file._connections, data_file.connections())



class MasterRecordTests(PdbDataFileTest):

    def test_missing_master_processing(self):
        self.assertEqual(self.empty._master, None)
        self.assertEqual(self.blank._master, None)


    def test_master_processing(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "MASTER       40    0    0    0    0    0    0    6 2930    2    0   29"
        ))
        self.assertEqual(
         data_file._master,
         {
          "remark_num": 40,
          "het_num": 0,
          "helix_num": 0,
          "sheet_num": 0,
          "site_num": 0,
          "crystal_num": 6,
          "coordinate_num": 2930,
          "ter_num": 2,
          "conect_num": 0,
          "seqres_num": 29
         }
        )


    def test_master_properties(self):
        data_file = pdb_data_file_from_pdb_file(PdbFile(
         "MASTER       40    0    0    0    0    0    0    6 2930    2    0   29"
        ))
        self.assertEqual(data_file._master, data_file.master())


    def test_can_modify_master_properties(self):
        self.blank.master({
         "remark_num": 40,
         "het_num": 0,
         "helix_num": 0,
         "sheet_num": 0,
         "site_num": 0,
         "crystal_num": 6,
         "coordinate_num": 2930,
         "ter_num": 2,
         "conect_num": 0,
         "seqres_num": 29
        })
        self.assertEqual(self.blank.master(), {
         "remark_num": 40,
         "het_num": 0,
         "helix_num": 0,
         "sheet_num": 0,
         "site_num": 0,
         "crystal_num": 6,
         "coordinate_num": 2930,
         "ter_num": 2,
         "conect_num": 0,
         "seqres_num": 29
        })


    def test_master_must_be_dict(self):
        with self.assertRaises(TypeError):
            self.blank.master("aaa")'''
