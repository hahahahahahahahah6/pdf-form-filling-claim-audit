# Documentation claim auditor

This offline static auditor compares documentation of the checked capability with Python source patterns. It scans the root README and Markdown under docs. Fenced code is excluded; inline code counts. Source is parsed without execution. Tests are reported separately; fixtures, examples, documentation and symlinks are excluded from production evidence.

```sh
pdf-form-filling-claim-audit audit . --json --fail-on medium --ignore vendor/
python3 -m pdf_form_filling_claim_audit --version
```

Exit 0 means PASS, 2 means a finding meets the threshold, and 1 means a usage or I/O error. The default threshold is high. Ignore prefixes can be repeated.

```
documented-pdf-form-filling-claim-false
documented-no-pdf-form-filling-claim-false
```

## Differentiation

The checked operation is distinct from document extraction, generation, merging, splitting, encryption and rotation. It is also distinct from spreadsheet, word processing and presentation reading and generation. Table extraction, specialized document extraction, invoice separation, multiple receipt detection, document cropping, image operations, electronic signatures, payment processing and OCR are outside the phrase lists.

## Limitations

- A matching phrase may describe a tool that only lists fields.
- A matching phrase may describe a form rendered as an image inside a document.
- A matching phrase may describe a wrapper that never performs the checked operation.
- A matching phrase may describe a template the tool only generates.
- A matching phrase may describe completion by hand in a browser.
- A matching phrase may describe sample data in a demo.
- A matching phrase may describe only creating new fields.
- A writer construction and an unrelated update call in one module count together.
- A wrapper construction and an unrelated fill call in one module count together.
- An opener and an unrelated field value assignment in one module count together.
- An assignment counts without a subsequent widget update.
- A wrapper and fill call count even when the dictionary matches no widgets.
- A writer and update call count even with an empty values dictionary.
- A library write call counts even with an empty data dictionary.
- An assignment counts even when the value is an empty string.
- A writer construction alone is not detected.
- A reader construction paired with an update call is not detected.
- An update call alone is not detected without a matching writer construction.
- A fill call alone is not detected without a matching wrapper construction.
- A field value assignment alone is not detected without a matching opener.
- Reading a field value is not detected.
- A widget update alone is not detected.
- A wrapper construction alone is not detected.
- A writer construction and write call alone are not detected.
- A writer construction and field-reading call alone are not detected.
- A field listing call alone is not detected.
- A flattening call alone is not detected.
- A text box placement call alone is not detected.
- A radio button placement call alone is not detected.
- A dropdown placement call alone is not detected.
- A writer and append call alone are not detected.
- A writer and merge call alone are not detected.
- A writer and single-page addition call alone are not detected.
- A writer and encryption call alone are not detected.
- A reader or writer and rotation call alone are not detected.
- An opener and page rotation call alone are not detected.
- A signing call alone is not detected.
- A reader call alone is not detected.
- Whole-pages extend alone is not detected.
- Single-page append alone is not detected.
- Plural page addition alone is not detected.
- An insert_pdf call alone is not detected.
- Document generation alone is not detected.
- Document merging alone is not detected.
- Document splitting alone is not detected.
- Document encryption alone is not detected.
- Document rotation alone is not detected.
- Document extraction alone is not detected.
- Electronic signing alone is not detected.
- External command subprocess calls are not detected.
- Mindee parsing with any product is not detected.
- Azure document analysis with any model ID is not detected.
- Veryfi calls of any kind are not detected.
- Google Document AI processing with any processor is not detected.
- Eden AI universal calls with any model ID are not detected.
- Textract calls of any kind are not detected.
- LlamaParse calls are not detected.
- Nanonets calls are not detected.
- Docsumo calls are not detected.
- ABBYY Vantage calls are not detected.
- Rossum calls are not detected.
- Klippa calls are not detected.
- Parseur calls are not detected.
- Extend calls are not detected.
- Hand-written dictionary editing without a listed call is not detected.
- Detection cannot establish whether values are correct or complete.
- Static matching cannot judge semantics.
- Dead code counts.
- Alias chains beyond the tracer are missed.
- Only exact phrases count.
- Denial handling depends on the listed phrases.
- Each paired route must occur in a single module.
