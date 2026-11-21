EXPECTED_YES = ('fill pdf form', 'fills pdf form', 'filling pdf form', 'fill pdf forms', 'fills pdf forms', 'filling pdf forms', 'fill in pdf form', 'fills in pdf form', 'filling in pdf form', 'fill in pdf forms', 'fills in pdf forms', 'filling in pdf forms', 'fill pdf form field', 'fills pdf form field', 'filling pdf form field', 'fill pdf form fields', 'fills pdf form fields', 'filling pdf form fields', 'fill out pdf form', 'fills out pdf form', 'filling out pdf form', 'fill out pdf forms', 'fills out pdf forms', 'filling out pdf forms', 'complete pdf form', 'completes pdf form', 'completing pdf form', 'complete pdf forms', 'completes pdf forms', 'completing pdf forms', 'enter data into pdf form', 'enters data into pdf form', 'entering data into pdf form', 'enter data into pdf forms', 'enters data into pdf forms', 'entering data into pdf forms', 'fill acroform', 'fills acroform', 'filling acroform', 'fill pdf form with data', 'fills pdf form with data', 'filling pdf form with data', 'pdf form filler', 'pdf form filling', 'fillable pdf form', 'fillable pdf forms', 'populate pdf form', 'populates pdf form', 'populating pdf form', 'autofill pdf form')
EXPECTED_NO = ('no pdf form filling', 'does not fill pdf form', 'does not fill pdf forms', 'does not fill in pdf form', 'does not fill in pdf forms', 'does not fill pdf form field', 'does not fill pdf form fields', 'does not fill out pdf form', 'does not fill out pdf forms', 'does not complete pdf form', 'does not complete pdf forms', 'does not enter data into pdf form', 'does not enter data into pdf forms', 'does not fill acroform', 'does not fill pdf form with data', 'no pdf form filler', 'does not support pdf form filling', 'without pdf form filling', 'pdf form filling not supported', 'no pdf form filling support', 'does not populate pdf form', 'does not autofill pdf form', 'pdf form filling not available', 'no fillable pdf form')
EXPECTED_NAMES = ('fill_pdf_form', 'fill_pdf_forms', 'fill_pdf_form_field', 'fill_pdf_form_fields', 'fill_in_pdf_form', 'fill_out_pdf_form', 'complete_pdf_form', 'fill_acroform', 'fill_pdf_form_with_data', 'populate_pdf_form', 'autofill_pdf_form', 'pdf_form_filler', 'pdf_form_filling', 'fill_pdf', 'fill_form', 'fill_form_fields', 'fill_form_field', 'update_pdf_form_field', 'update_pdf_form_fields', 'set_pdf_form_field', 'set_pdf_form_value', 'fill_pdf_field', 'fill_pdf_fields', 'fill_pdf_acroform')
import contextlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from pdf_form_filling_claim_audit.audit import audit, evidence
from pdf_form_filling_claim_audit.phrases import PDFORMFILLING, NOPDFORMFILLING, GENERIC_NAMES
from pdf_form_filling_claim_audit.__main__ import main

class AuditTests(unittest.TestCase):
    def test_phrase_oracle(self):
        self.assertEqual(PDFORMFILLING, EXPECTED_YES)
        self.assertEqual(NOPDFORMFILLING, EXPECTED_NO)
        self.assertEqual(GENERIC_NAMES, EXPECTED_NAMES)

    def test_routes(self):
        cases = []
        for mod in ('pypdf', 'PyPDF2'):
            cases += [f'from {mod} import PdfWriter as W\nW(); x.update_page_form_field_values()', f'import {mod} as m\nm.PdfWriter(); x.update_page_form_field_values()']
        cases += ['from PyPDF2 import PdfWriter as W\nW(); x.updatePageFormFieldValues()', 'from fillpdf.fillpdfs import write_fillable_pdf as f\nf()', 'from fillpdf import write_fillable_pdf as f\nf()', 'from fillpdf import fillpdfs as f\nf.write_fillable_pdf()', 'import fillpdf as f\nf.fillpdfs.write_fillable_pdf()', 'from PyPDFForm import PdfWrapper as W\nW(); x.fill()', 'import PyPDFForm as f\nf.PdfWrapper(); x.fill()']
        for mod in ('fitz','pymupdf'):
            for method in ('open','Document'):
                cases += [f'import {mod} as m\nm.{method}(); widget.field_value = ""', f'from {mod} import {method} as op\nop(); widget.field_value: str = "a"']
        cases += ['x.'+name+'()' for name in EXPECTED_NAMES]
        cases += ['from other import fill_pdf_form as f\nf()']
        # Assigned-variable forms (canonical real-world usage; the method
        # call sits on a local variable bound to the construction).
        cases += ['from pypdf import PdfWriter\nw = PdfWriter()\nw.update_page_form_field_values(p, {})',
                  'from PyPDF2 import PdfWriter\nw = PdfWriter()\nw.updatePageFormFieldValues(p, {})',
                  'from PyPDFForm import PdfWrapper\nw = PdfWrapper("in.pdf")\nw.fill({})',
                  'import fitz\ndoc = fitz.open(x)\nwidget = doc[0].widgets()\nwidget.field_value = "a"',
                  'import fitz\nfor widget in fitz.open(x)[0].widgets():\n    widget.field_value = "a"']
        for source in cases:
            with self.subTest(source=source): self.assertTrue(evidence(source))

    def test_not_evidence(self):
        cases = ['import '+x for x in ('pypdf','PyPDF2','fillpdf','PyPDFForm','fitz','pymupdf')]
        cases += ['import pypdf\npypdf.PdfWriter()', 'import PyPDF2\nPyPDF2.PdfWriter()', 'import pypdf\npypdf.PdfReader(); x.update_page_form_field_values()', 'x.update_page_form_field_values()', 'x.updatePageFormFieldValues()', 'import pypdf\npypdf.PdfWriter(); x.updatePageFormFieldValues()', 'import pypdf\npypdf.PdfWriter().write(x)', 'import pypdf\npypdf.PdfWriter().get_fields()']
        cases += ['from fillpdf import fillpdfs\nfillpdfs.'+name+'()' for name in ('get_form_fields','flatten_pdf','place_text_box','place_radiobutton','place_dropdown')]
        cases += ['import PyPDFForm\nPyPDFForm.PdfWrapper()', 'x.fill()', 'import PyPDFForm\nPyPDFForm.PdfWrapper().write()', 'import PyPDFForm\nPyPDFForm.PdfWrapper().save()', 'import PyPDFForm\nPyPDFForm.FormWrapper(); x.fill()', 'import fitz\nfitz.open()', 'widget.field_value = 1', 'import fitz\nfitz.open(); v = widget.field_value', 'import fitz\nfitz.open(); widget.update()', 'import fitz\nfitz.open().save(x)']
        cases += ['import pypdf\npypdf.PdfWriter().'+x+'(y)' for x in ('append','add_page','encrypt')]
        cases += ['import PyPDF2\nPyPDF2.PdfWriter().merge(x)', 'import fitz\nfitz.open().insert_pdf(x)', 'import pypdf\npypdf.PdfReader().rotate(90)', 'import fitz\nfitz.open(); x.set_rotation(90)', 'pyhanko.sign_pdf()', 'endesive.pdf.cms.sign()', 'docusign.create_envelope()', 'dropbox.signature_request_send()', 'pypdf.PdfReader()', 'pdfplumber.open()', 'pdfminer.extract_text()', 'reportlab.Canvas().save()', 'fpdf.output()', 'weasyprint.write_pdf()', 'x.pages.extend(y)', 'x.addpages(y)', 'x.addpage(y)', '"pdf fill form"', 'x.fill_pdf_form', 'fill_pdf_form()', 'def fill_pdf_form(): pass\nx.fill_pdf_form()', 'import pypdf\npypdf = 1\npypdf.PdfWriter(); x.update_page_form_field_values()', 'from pypdf import PdfWriter\nwith x as PdfWriter: pass\nPdfWriter(); x.update_page_form_field_values()', 'def broken(']
        cases += ['import subprocess\nsubprocess.run(["'+x+'"] )' for x in ('qpdf','pdftk','gs')]
        cases += [x+'(x)' for x in ('mindee.parse','azure.begin_analyze_document','veryfi.Client','documentai.process_document','textract.analyze_document','eden.universal_ai','llamaparse.parse','nanonets.ocr','docsumo.upload','abbyy.process','rossum.process','klippa.parse','parseur.parse','extend.parse')]
        for source in cases:
            with self.subTest(source=source): self.assertFalse(evidence(source))

    def test_audit_scenarios(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); readme=p/'README.md'; src=p/'app.py'
            readme.write_text('fill pdf form'); r=audit(d); self.assertEqual(r['findings'][0]['rule'],'documented-pdf-form-filling-claim-false'); self.assertEqual(r['findings'][0]['severity'],'HIGH'); self.assertEqual(r['verdict'],'FAIL')
            src.write_text('x.fill_pdf_form()'); self.assertEqual(audit(d)['verdict'],'PASS')
            readme.write_text('does not fill pdf form'); r=audit(d); self.assertEqual(r['findings'][0]['rule'],'documented-no-pdf-form-filling-claim-false'); self.assertEqual(r['claims'],[])
            src.unlink(); self.assertEqual(audit(d)['verdict'],'PASS')
            readme.write_text('```\nfill pdf form\n```'); self.assertEqual(audit(d)['verdict'],'PASS')
            readme.write_text('`fill pdf form`'); self.assertEqual(audit(d)['verdict'],'FAIL')
            (p/'tests').mkdir(); (p/'tests/test_app.py').write_text('x.fill_pdf_form()')
            self.assertEqual(audit(d)['findings'][0]['severity'],'MEDIUM'); self.assertEqual(audit(d)['verdict'],'PASS'); self.assertEqual(audit(d,fail_on='medium')['verdict'],'FAIL')
            src.write_text('import fitz\nfitz.open()'); (p/'other.py').write_text('widget.field_value = 1'); self.assertEqual(audit(d)['findings'][0]['severity'],'MEDIUM')
            readme.write_text('Nothing claimed'); self.assertEqual(audit(d)['verdict'],'PASS')

    def test_exclusions(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); (p/'README.md').write_text('fill pdf form')
            for name in ('fixtures','examples','docs'):
                (p/name).mkdir(); (p/name/'code.py').write_text('x.fill_pdf_form()')
            (p/'test_file.py').write_text('x.fill_pdf_form()'); (p/'app_test.py').write_text('x.fill_pdf_form()')
            (p/'link.py').symlink_to(p/'test_file.py'); (p/'linked').symlink_to(p/'fixtures',target_is_directory=True)
            r=audit(d); self.assertFalse(r['production_evidence']); self.assertEqual(len(r['test_evidence']),2)
            self.assertEqual(audit(d,ignore=('test_','app_'))['findings'][0]['severity'],'HIGH')

    def test_cli(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); (p/'README.md').write_text('fill pdf form')
            cmd=[sys.executable,'-m','pdf_form_filling_claim_audit']
            r=subprocess.run(cmd+['audit',d,'--json'],capture_output=True,text=True); self.assertEqual(r.returncode,2)
            data=json.loads(r.stdout); self.assertEqual(data['verdict'],'FAIL'); self.assertTrue(data['findings'][0]['message'])
            self.assertEqual(subprocess.run(cmd+['--version'],capture_output=True,text=True).stdout.strip(),'0.1.0')
            self.assertEqual(subprocess.run(cmd+['audit',d,'--fail-on','HIGH'],capture_output=True).returncode,1)
            self.assertEqual(subprocess.run(cmd+['audit',d+'/missing'],capture_output=True).returncode,1)
            with contextlib.redirect_stdout(io.StringIO()): self.assertEqual(main(['audit',d]),2)
            (p/'README.md').write_text('does not fill pdf form'); (p/'app.py').write_text('x.fill_pdf_form()')
            with contextlib.redirect_stdout(io.StringIO()): self.assertEqual(main(['audit',d]),2)
            (p/'app.py').unlink(); (p/'README.md').write_text('fill pdf form'); (p/'test_app.py').write_text('x.fill_pdf_form()')
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main(['audit',d]),0); self.assertEqual(main(['audit',d,'--fail-on','medium']),2)
