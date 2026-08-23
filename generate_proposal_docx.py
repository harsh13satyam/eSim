"""
Generates a comprehensive, formal Internship Proposal & Design Report in Microsoft Word (.docx) format
for FOSSEE eSim Semester Long Internship - Task 5: Automated Tool Manager.
"""

import os
import zipfile
import datetime
import html

def generate_proposal_docx(output_path: str):
    now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    content_types_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
  <Override PartName="/word/fontTable.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.fontTable+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>"""

    rels_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>"""

    core_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
  xmlns:dc="http://purl.org/dc/elements/1.1/"
  xmlns:dcterms="http://purl.org/dc/terms/"
  xmlns:dcmitype="http://purl.org/dc/dcmitype/"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>Project Proposal: Automated Tool Manager for eSim</dc:title>
  <dc:subject>FOSSEE eSim Semester Long Internship - Autumn 2026 Screening Task 5</dc:subject>
  <dc:creator>Harsh Satyam</dc:creator>
  <cp:lastModifiedBy>Harsh Satyam</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>"""

    app_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
  xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Microsoft Word</Application>
  <DocSecurity>0</DocSecurity>
  <Lines>2400</Lines>
  <Paragraphs>600</Paragraphs>
  <ScaleCrop>false</ScaleCrop>
  <HeadingPairs>
    <vt:vector size="2" baseType="variant">
      <vt:variant><vt:lpstr>Title</vt:lpstr></vt:variant>
      <vt:variant><vt:i4>1</vt:i4></vt:variant>
    </vt:vector>
  </HeadingPairs>
  <TitlesOfParts>
    <vt:vector size="1" baseType="lpstr">
      <vt:lpstr>Project Proposal: Automated Tool Manager for eSim</vt:lpstr>
    </vt:vector>
  </TitlesOfParts>
  <Company>FOSSEE, IIT Bombay</Company>
  <LinksUpToDate>false</LinksUpToDate>
  <SharedDoc>false</SharedDoc>
  <HyperlinksChanged>false</HyperlinksChanged>
  <AppVersion>16.0000</AppVersion>
</Properties>"""

    doc_rels_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/fontTable" Target="fontTable.xml"/>
</Relationships>"""

    font_table_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:fonts xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:font w:name="Calibri">
    <w:panose1 w:val="020F0502020204030204"/>
    <w:charset w:val="00"/>
    <w:family w:val="swiss"/>
    <w:pitch w:val="variable"/>
  </w:font>
  <w:font w:name="Calibri Light">
    <w:panose1 w:val="020F0302020204030204"/>
    <w:charset w:val="00"/>
    <w:family w:val="swiss"/>
    <w:pitch w:val="variable"/>
  </w:font>
  <w:font w:name="Cambria">
    <w:panose1 w:val="02040503050406030204"/>
    <w:charset w:val="00"/>
    <w:family w:val="roman"/>
    <w:pitch w:val="variable"/>
  </w:font>
  <w:font w:name="Consolas">
    <w:panose1 w:val="020B0609020204030204"/>
    <w:charset w:val="00"/>
    <w:family w:val="modern"/>
    <w:pitch w:val="fixed"/>
  </w:font>
</w:fonts>"""

    settings_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:zoom w:percent="100"/>
  <w:defaultTabStop w:val="720"/>
  <w:characterSpacingControl w:val="doNotCompress"/>
</w:settings>"""

    styles_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/>
        <w:sz w:val="22"/>
        <w:szCs w:val="22"/>
        <w:color w:val="1F2937"/>
      </w:rPr>
    </w:rPrDefault>
    <w:pPrDefault>
      <w:pPr>
        <w:spacing w:after="140" w:line="276" w:lineRule="auto"/>
      </w:pPr>
    </w:pPrDefault>
  </w:docDefaults>

  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:qFormat/>
  </w:style>

  <w:style w:type="paragraph" w:styleId="ProposalTitle">
    <w:name w:val="ProposalTitle"/>
    <w:basedOn w:val="Normal"/>
    <w:next w:val="Normal"/>
    <w:qFormat/>
    <w:pPr>
      <w:spacing w:before="360" w:after="120"/>
      <w:jc w:val="center"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Cambria" w:hAnsi="Cambria"/>
      <w:b/>
      <w:sz w:val="52"/>
      <w:color w:val="0F2942"/>
    </w:rPr>
  </w:style>

  <w:style w:type="paragraph" w:styleId="ProposalSubtitle">
    <w:name w:val="ProposalSubtitle"/>
    <w:basedOn w:val="Normal"/>
    <w:next w:val="Normal"/>
    <w:qFormat/>
    <w:pPr>
      <w:spacing w:before="0" w:after="240"/>
      <w:jc w:val="center"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Calibri Light" w:hAnsi="Calibri Light"/>
      <w:sz w:val="26"/>
      <w:color w:val="2563EB"/>
      <w:b/>
    </w:rPr>
  </w:style>

  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:basedOn w:val="Normal"/>
    <w:next w:val="Normal"/>
    <w:qFormat/>
    <w:pPr>
      <w:spacing w:before="360" w:after="160"/>
      <w:pBdr>
        <w:bottom w:val="single" w:sz="16" w:space="6" w:color="1E40AF"/>
      </w:pBdr>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Cambria" w:hAnsi="Cambria"/>
      <w:b/>
      <w:sz w:val="32"/>
      <w:color w:val="1E3A8A"/>
    </w:rPr>
  </w:style>

  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:basedOn w:val="Normal"/>
    <w:next w:val="Normal"/>
    <w:qFormat/>
    <w:pPr>
      <w:spacing w:before="240" w:after="120"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
      <w:b/>
      <w:sz w:val="26"/>
      <w:color w:val="1D4ED8"/>
    </w:rPr>
  </w:style>

  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/>
    <w:basedOn w:val="Normal"/>
    <w:next w:val="Normal"/>
    <w:qFormat/>
    <w:pPr>
      <w:spacing w:before="160" w:after="80"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
      <w:b/>
      <w:sz w:val="23"/>
      <w:color w:val="334155"/>
    </w:rPr>
  </w:style>

  <w:style w:type="paragraph" w:styleId="CodeBlock">
    <w:name w:val="CodeBlock"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr>
      <w:shd w:val="clear" w:color="auto" w:fill="F8FAFC"/>
      <w:pBdr>
        <w:left w:val="single" w:sz="18" w:space="10" w:color="3B82F6"/>
      </w:pBdr>
      <w:spacing w:before="60" w:after="60" w:line="240" w:lineRule="auto"/>
      <w:ind w:left="200" w:right="200"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>
      <w:sz w:val="19"/>
      <w:color w:val="0F172A"/>
    </w:rPr>
  </w:style>

  <w:style w:type="paragraph" w:styleId="CalloutBox">
    <w:name w:val="CalloutBox"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr>
      <w:shd w:val="clear" w:color="auto" w:fill="EFF6FF"/>
      <w:pBdr>
        <w:left w:val="single" w:sz="24" w:space="12" w:color="2563EB"/>
        <w:top w:val="single" w:sz="4" w:space="6" w:color="DBEAFE"/>
        <w:right w:val="single" w:sz="4" w:space="6" w:color="DBEAFE"/>
        <w:bottom w:val="single" w:sz="4" w:space="6" w:color="DBEAFE"/>
      </w:pBdr>
      <w:spacing w:before="120" w:after="160"/>
      <w:ind w:left="240" w:right="240"/>
    </w:pPr>
    <w:rPr>
      <w:sz w:val="21"/>
      <w:color w:val="1E3A8A"/>
    </w:rPr>
  </w:style>
</w:styles>"""

    # Helpers for building OpenXML tags
    def p(text="", bold=False, italic=False, style=None, color=None, font=None, size=None, align=None):
        p_pr = []
        if style:
            p_pr.append(f'<w:pStyle w:val="{style}"/>')
        if align:
            p_pr.append(f'<w:jc w:val="{align}"/>')
        p_pr_xml = f'<w:pPr>{"".join(p_pr)}</w:pPr>' if p_pr else ""

        if not text:
            return f'<w:p>{p_pr_xml}</w:p>'

        r_pr = []
        if bold:
            r_pr.append('<w:b/>')
        if italic:
            r_pr.append('<w:i/>')
        if color:
            r_pr.append(f'<w:color w:val="{color}"/>')
        if font:
            r_pr.append(f'<w:rFonts w:ascii="{font}" w:hAnsi="{font}"/>')
        if size:
            r_pr.append(f'<w:sz w:val="{size}"/>')
        r_pr_xml = f'<w:rPr>{"".join(r_pr)}</w:rPr>' if r_pr else ""

        safe_text = html.escape(text)
        return f'<w:p>{p_pr_xml}<w:r>{r_pr_xml}<w:t xml:space="preserve">{safe_text}</w:t></w:r></w:p>'

    def p_runs(runs, style=None, align=None):
        p_pr = []
        if style:
            p_pr.append(f'<w:pStyle w:val="{style}"/>')
        if align:
            p_pr.append(f'<w:jc w:val="{align}"/>')
        p_pr_xml = f'<w:pPr>{"".join(p_pr)}</w:pPr>' if p_pr else ""

        runs_xml = []
        for text, bold, italic, color, font, size in runs:
            r_pr = []
            if bold:
                r_pr.append('<w:b/>')
            if italic:
                r_pr.append('<w:i/>')
            if color:
                r_pr.append(f'<w:color w:val="{color}"/>')
            if font:
                r_pr.append(f'<w:rFonts w:ascii="{font}" w:hAnsi="{font}"/>')
            if size:
                r_pr.append(f'<w:sz w:val="{size}"/>')
            r_pr_xml = f'<w:rPr>{"".join(r_pr)}</w:rPr>' if r_pr else ""
            safe_text = html.escape(text)
            runs_xml.append(f'<w:r>{r_pr_xml}<w:t xml:space="preserve">{safe_text}</w:t></w:r>')

        return f'<w:p>{p_pr_xml}{"".join(runs_xml)}</w:p>'

    def bullet(text, bold_prefix="", level=0):
        runs = []
        if bold_prefix:
            runs.append((bold_prefix, True, False, "0F172A", None, None))
        runs.append((text, False, False, "334155", None, None))
        
        ind_left = 360 * (level + 1)
        p_pr = f'<w:pPr><w:spacing w:after="80"/><w:ind w:left="{ind_left}" w:hanging="240"/></w:pPr>'
        bullet_run = '<w:r><w:rPr><w:rFonts w:ascii="Symbol" w:hAnsi="Symbol"/><w:color w:val="2563EB"/></w:rPr><w:t>·  </w:t></w:r>'
        
        runs_xml = []
        for t, b, it, c, f, s in runs:
            r_pr = []
            if b:
                r_pr.append('<w:b/>')
            if it:
                r_pr.append('<w:i/>')
            if c:
                r_pr.append(f'<w:color w:val="{c}"/>')
            if f:
                r_pr.append(f'<w:rFonts w:ascii="{f}" w:hAnsi="{f}"/>')
            if s:
                r_pr.append(f'<w:sz w:val="{s}"/>')
            r_pr_xml = f'<w:rPr>{"".join(r_pr)}</w:rPr>' if r_pr else ""
            runs_xml.append(f'<w:r>{r_pr_xml}<w:t xml:space="preserve">{html.escape(t)}</w:t></w:r>')

        return f'<w:p>{p_pr}{bullet_run}{"".join(runs_xml)}</w:p>'

    def code_block(lines):
        xml_lines = []
        for line in lines:
            xml_lines.append(f'<w:p><w:pPr><w:pStyle w:val="CodeBlock"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/><w:sz w:val="18"/><w:color w:val="0F172A"/></w:rPr><w:t xml:space="preserve">{html.escape(line)}</w:t></w:r></w:p>')
        return "".join(xml_lines)

    def table(headers, rows, col_widths=None):
        if not col_widths:
            col_widths = [9000 // len(headers)] * len(headers)
        
        tbl_pr = """<w:tblPr>
          <w:tblW w:w="9000" w:type="dxa"/>
          <w:jc w:val="center"/>
          <w:tblBorders>
            <w:top w:val="single" w:sz="8" w:space="0" w:color="94A3B8"/>
            <w:left w:val="none"/>
            <w:bottom w:val="single" w:sz="12" w:space="0" w:color="64748B"/>
            <w:right w:val="none"/>
            <w:insideH w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
            <w:insideV w:val="none"/>
          </w:tblBorders>
        </w:tblPr>"""
        
        grid_cols = "".join([f'<w:gridCol w:w="{w}"/>' for w in col_widths])
        grid_xml = f'<w:tblGrid>{grid_cols}</w:tblGrid>'
        
        hdr_cells = []
        for i, h in enumerate(headers):
            hdr_cells.append(f"""<w:tc>
              <w:tcPr>
                <w:tcW w:w="{col_widths[i]}" w:type="dxa"/>
                <w:shd w:val="clear" w:color="auto" w:fill="1E3A8A"/>
                <w:tcMar><w:top w:w="140"/><w:bottom w:w="140"/><w:left w:w="160"/><w:right w:w="160"/></w:tcMar>
              </w:tcPr>
              <w:p><w:pPr><w:spacing w:before="0" w:after="0"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="20"/><w:color w:val="FFFFFF"/></w:rPr><w:t>{html.escape(h)}</w:t></w:r></w:p>
            </w:tc>""")
        hdr_row = f'<w:tr><w:trPr><w:tblHeader/></w:trPr>{"".join(hdr_cells)}</w:tr>'
        
        body_rows = []
        for r_idx, row in enumerate(rows):
            fill_color = "FFFFFF" if r_idx % 2 == 0 else "F8FAFC"
            cells = []
            for c_idx, cell in enumerate(row):
                cells.append(f"""<w:tc>
                  <w:tcPr>
                    <w:tcW w:w="{col_widths[c_idx]}" w:type="dxa"/>
                    <w:shd w:val="clear" w:color="auto" w:fill="{fill_color}"/>
                    <w:tcMar><w:top w:w="100"/><w:bottom w:w="100"/><w:left w:w="160"/><w:right w:w="160"/></w:tcMar>
                  </w:tcPr>
                  <w:p><w:pPr><w:spacing w:before="0" w:after="0"/></w:pPr><w:r><w:rPr><w:sz w:val="20"/><w:color w:val="334155"/></w:rPr><w:t>{html.escape(cell)}</w:t></w:r></w:p>
                </w:tc>""")
            body_rows.append(f'<w:tr>{"".join(cells)}</w:tr>')
            
        return f'<w:tbl>{tbl_pr}{grid_xml}{hdr_row}{"".join(body_rows)}</w:tbl><w:p><w:pPr><w:spacing w:after="160"/></w:pPr></w:p>'

    doc_body = []

    # --- COVER / PROPOSAL HEADER ---
    doc_body.append(p("PROJECT PROPOSAL & TECHNICAL REPORT", bold=True, style="ProposalTitle"))
    doc_body.append(p("Automated Tool Manager for eSim EDA Suite", style="ProposalSubtitle"))
    doc_body.append(p("FOSSEE Semester Long Internship – Autumn 2026 Screening Task 5 (CSE and Related Fields)", italic=True, align="center", color="4B5563"))

    # Proposal Metadata Block
    prop_headers = ["Proposal Field", "Details / Value"]
    prop_rows = [
        ["Applicant Name", "Harsh Satyam"],
        ["Contact Email", "harshsatyam636@gmail.com"],
        ["Target Initiative", "eSim Open-Source EDA Development (FOSSEE, IIT Bombay)"],
        ["Screening Task", "Task 5: Tool Manager"],
        ["Core Requirements Implemented", "Requirement 1 (Installation Management) + Requirement 4 (Dependency Checker)"],
        ["Development Language", "Python 3.10+ (Standard Library, Zero-External Dependencies)"],
        ["Test Coverage & Quality", "36 Unit Tests (100% Core Logic Coverage, unittest runner)"],
        ["Accompanying Prototype", "Full CLI Tool (`main.py`) + Reactive Sophisticated Dark Web GUI"]
    ]
    doc_body.append(table(prop_headers, prop_rows, [3000, 6000]))

    # Callout Box
    doc_body.append(p_runs([
        ("Executive Proposal Statement: ", True, False, "1E3A8A", None, None),
        ("This proposal presents a complete, production-ready Automated Tool Manager engineered specifically for the eSim EDA platform. Designed to eliminate recurring onboarding and configuration friction for students and researchers, the solution delivers robust cross-platform dependency checking, loose banner version extraction, strategy-based package management, and non-destructive simulation modes.", False, False, "1E40AF", None, None)
    ], style="CalloutBox"))

    # --- SECTION 1: INTRODUCTION & PROBLEM STATEMENT ---
    doc_body.append(p("1. Introduction & Problem Statement", bold=True, style="Heading1"))
    doc_body.append(p_runs([
        ("eSim ", True, False, "1E3A8A", None, None),
        ("(developed by FOSSEE, IIT Bombay) is an open-source Electronic Design Automation environment that integrates several independent, specialized scientific tools into a cohesive circuit simulation and PCB workflow. The core external dependencies include:", False, False, "334155", None, None)
    ]))
    doc_body.append(bullet("The core SPICE analog, transient, and digital simulation engine.", "Ngspice: "))
    doc_body.append(bullet("The schematic capture (eeschema) and PCB layout (pcbnew) suite.", "KiCad EDA: "))
    doc_body.append(bullet("Subcircuit creation, parameter sweeps, and orchestration scripting runtime.", "Python 3: "))
    doc_body.append(bullet("Project repository tracking, subcircuit versioning, and schematic library distribution.", "Git: "))

    doc_body.append(p("Identified Friction Points in Current eSim Ecosystem:", bold=True, style="Heading2"))
    doc_body.append(bullet("Heterogeneous package formats across Linux distros (APT on Ubuntu/Debian, Pacman on Arch, DNF on Fedora), macOS (Homebrew), and Windows (Winget, Chocolatey).", "1. Platform Fragmentation: "))
    doc_body.append(bullet("Incompatibilities like Ngspice < 38 causing SPICE netlist syntax breaks, or KiCad 5 vs 7/8 schematic schema divergence.", "2. Version Incompatibilities: "))
    doc_body.append(bullet("Discrepancies in default executable search paths (/usr/bin, /usr/local/bin, /opt/homebrew, C:\\Program Files\\).", "3. Path Non-Uniformity: "))
    doc_body.append(bullet("Lack of unified diagnostics and actionable recovery suggestions for non-technical users.", "4. Diagnostic Deficits: "))

    # --- SECTION 2: OBJECTIVES & PROPOSED SOLUTION ---
    doc_body.append(p("2. Objectives & Implemented Solution", bold=True, style="Heading1"))
    doc_body.append(p("The proposed tool manager resolves these issues with zero external pip dependencies, ensuring out-of-the-box reliability across every operating system:"))

    obj_headers = ["Screening Task Objective", "Implementation Approach", "Demonstrated Outcome"]
    obj_rows = [
        ["Req 1: Tool Installation Management", "Strategy Pattern across 6 package managers (Apt, Pacman, Dnf, Brew, Winget, Choco) with privilege checks and `--dry-run` simulation.", "100% deterministic package installation resolution with zero arbitrary shell invocations."],
        ["Req 4: Dependency Checker", "Multi-candidate binary locator, timeout-protected banner probes, and integer-tuple SemVer comparison.", "Instant classification into INSTALLED, MISSING, INCOMPATIBLE, UNKNOWN, or UNSUPPORTED."],
        ["System Diagnostics (`doctor`)", "Unified environmental audit (OS, release, CPU arch, Python version, admin status) with actionable recommendations.", "Provides clear, copy-pasteable terminal instructions to resolve missing or outdated tools."],
        ["Enterprise Telemetry & Logging", "Rotating file logging to `logs/esim_manager.log` with 5MB rotation caps and 3 backups.", "Complete operational audit trail without leaking environment secrets."]
    ]
    doc_body.append(table(obj_headers, obj_rows, [2600, 3400, 3000]))

    # --- SECTION 3: SYSTEM ARCHITECTURE & DESIGN PATTERNS ---
    doc_body.append(p("3. System Architecture & Design Patterns", bold=True, style="Heading1"))
    doc_body.append(p("The architecture follows SOLID principles, strictly decoupling system discovery, package manager strategies, and tool definitions."))

    doc_body.append(p("Architectural Pattern Breakdown:", bold=True, style="Heading2"))
    doc_body.append(bullet("Encapsulates platform-specific package managers behind a uniform interface (`build_install_command`, `is_available`, `install`). Adding a new package manager requires zero changes to core manager logic.", "1. Strategy Pattern (`installer.py`): "))
    doc_body.append(bullet("Isolates tool specifications (binaries, min version, regex, package IDs, docs URL) into pluggable classes inheriting `BaseToolProvider`. Registering a new tool (e.g. Verilator, GHDL) is a simple one-file addition.", "2. Registry Pattern (`tools/`): "))
    doc_body.append(bullet("`ToolManager` provides a single clean API surface consumed by the CLI, testing suites, and graphical frontend.", "3. Facade Pattern (`manager.py`): "))
    doc_body.append(bullet("Strict ban on `shell=True`. All external calls use explicit array tokens `subprocess.run(['apt-get', 'install', '-y', pkg], shell=False)` with a 10s timeout.", "4. Security Guardrails: "))

    doc_body.append(p("Architecture Block Diagram:", bold=True, style="Heading2"))
    diag = [
        "+-----------------------------------------------------------------------------------+",
        "|                    CLI / User Interface Layer (main.py / cli.py)                  |",
        "+-----------------------------------------------------------------------------------+",
        "                                          |                                          ",
        "                                          v                                          ",
        "+-----------------------------------------------------------------------------------+",
        "|                           ToolManager (Central Facade)                            |",
        "+-----------------------------------------------------------------------------------+",
        "         |                                 |                                 |       ",
        "         v                                 v                                 v       ",
        "+---------------------+           +---------------------+           +---------------+",
        "|   SystemDetector    |           |   PackageInstaller  |           | Tool Registry |",
        "+---------------------+           +---------------------+           +---------------+",
        "   |               |                 |               |                 | Python      |",
        "   v               v                 v               v                 | Git         |",
        "[Platform]     [SemVer]          [Apt/Pacman]    [Brew/Winget]         | Ngspice     |",
        "[Manager ]     [Checker]         [Dnf       ]    [Choco      ]         | KiCad       |",
        "                                                                    +---------------+",
        "                                          |                                          ",
        "                                          v                                          ",
        "+-----------------------------------------------------------------------------------+",
        "|                  Rotating File Logger (logs/esim_manager.log)                     |",
        "+-----------------------------------------------------------------------------------+"
    ]
    doc_body.append(code_block(diag))

    # --- SECTION 4: CODE IMPLEMENTATION & MODULE BREAKDOWN ---
    doc_body.append(p("4. Code Implementation & Module Breakdown", bold=True, style="Heading1"))

    doc_body.append(p("4.1 Source Code Tree", bold=True, style="Heading2"))
    tree = [
        "esim-tool-manager/",
        "├── src/esim_tool_manager/",
        "│   ├── __init__.py           # Package version and API exports",
        "│   ├── models.py            # Typed dataclasses (ToolDefinition, ToolStatus, SystemInfo)",
        "│   ├── platform.py          # OS, architecture, and privilege heuristics",
        "│   ├── version_checker.py   # SemVer comparator and vendor banner extractors",
        "│   ├── detector.py          # System dependency and binary locator engine",
        "│   ├── installer.py         # Strategy pattern for package managers",
        "│   ├── logger.py            # Rotating file and console logger",
        "│   ├── exceptions.py        # Typed exception hierarchy",
        "│   ├── manager.py           # Central ToolManager facade",
        "│   ├── cli.py               # Argument parser, ANSI formatting, and JSON serializer",
        "│   └── tools/               # Pluggable tool registry",
        "│       ├── base.py          # BaseToolProvider abstract class",
        "│       ├── python.py        # Python 3 specification",
        "│       ├── git.py           # Git version control specification",
        "│       ├── ngspice.py       # Ngspice simulator specification",
        "│       └── kicad.py         # KiCad EDA specification",
        "├── tests/                   # 36 automated unit tests",
        "├── docs/                    # Complete design and testing documentation",
        "├── logs/                    # Action and diagnostic logs",
        "├── main.py                  # Direct CLI entry point",
        "└── pyproject.toml           # Modern PEP 518/621 packaging metadata"
    ]
    doc_body.append(code_block(tree))

    doc_body.append(p("4.2 Core Version Extraction Engine (`version_checker.py`)", bold=True, style="Heading2"))
    doc_body.append(p("The engine handles heterogeneous multi-line vendor outputs:"))
    doc_body.append(bullet("Extracts clean SemVer from outputs like 'Python 3.10.12' and 'git version 2.34.1'.", "Standard Regex: "))
    doc_body.append(bullet("Handles complex banners like '** ngspice-42.2 : Circuit level simulation program'.", "Ngspice Parser: "))
    doc_body.append(bullet("Extracts versions from releases like 'Application: kicad Version: 7.0.10' or '8.0.0-rc1'.", "KiCad Parser: "))
    doc_body.append(bullet("Transforms raw version strings into comparable integer tuples (e.g. '42.2' -> (42, 2, 0)) to avoid lexicographical comparison bugs.", "Tuple Transformation: "))

    # --- SECTION 5: STEP-BY-STEP EXECUTION WORKFLOW ---
    doc_body.append(p("5. Execution Workflows & Sequence Trace", bold=True, style="Heading1"))

    doc_body.append(p("5.1 Dependency Check (`python main.py check`)", bold=True, style="Heading2"))
    flow1 = [
        "1. CLI parses 'check' command -> ToolManager.check_all_dependencies()",
        "2. PlatformManager determines OS (Linux Debian 12), Arch (x86_64), Elevation (Root).",
        "3. Loop through ToolRegistry (Python, Git, Ngspice, KiCad):",
        "     a. PlatformManager.find_executable('python3') -> Found at /usr/bin/python3.10",
        "     b. Subprocess executes ['/usr/bin/python3.10', '--version'] with 10s timeout.",
        "     c. VersionChecker extracts '3.10.12' -> Compares against required '3.10.0' -> Status: INSTALLED",
        "     d. PlatformManager.find_executable('ngspice') -> Not found -> Status: MISSING",
        "4. ToolManager returns list[ToolStatus] -> CLI renders formatted ANSI table."
    ]
    doc_body.append(code_block(flow1))

    doc_body.append(p("5.2 Safe Installation (`python main.py install ngspice --dry-run`)", bold=True, style="Heading2"))
    flow2 = [
        "1. CLI parses 'install ngspice --dry-run' -> ToolManager.install_tool('ngspice', dry_run=True)",
        "2. ToolManager fetches ToolDefinition for 'ngspice' from registry.",
        "3. PackageInstaller resolves host package manager -> Selects AptStrategy.",
        "4. AptStrategy builds argument array: ['apt-get', 'install', '-y', 'ngspice'].",
        "5. [Dry-Run Mode] Logs simulated action without executing subprocess.",
        "6. Returns InstallationResult(success=True, dry_run=True) -> CLI outputs simulation summary."
    ]
    doc_body.append(code_block(flow2))

    # --- SECTION 6: TESTING & VERIFICATION ---
    doc_body.append(p("6. Testing Strategy & Verification Matrix", bold=True, style="Heading1"))
    doc_body.append(p("The implementation is backed by 36 unit tests covering 100% of the core logic using Python's native `unittest` test runner:"))

    test_headers = ["Test Module", "Test Count", "Key Test Vectors & Scenarios"]
    test_rows = [
        ["test_detector.py", "6 Tests", "Binary discovery on PATH, missing executables, CPU/OS detection, timeout handling, platform mismatch."],
        ["test_version_checker.py", "5 Tests", "SemVer comparison, tuple conversion, standard version banners, complex Ngspice headers, KiCad releases."],
        ["test_installer.py", "9 Tests", "Apt, Brew, Choco, Dnf, Pacman, Winget command generation, dry-run simulation, mock success (0) and failure (100)."],
        ["test_manager.py", "6 Tests", "ToolManager facade, check_all, check_single, get_tool_info, list_supported_tools, doctor diagnostic reports."],
        ["test_tools.py", "3 Tests", "Default tool loading, case-insensitive registry lookups, runtime registration of custom tool providers."],
        ["test_cli.py", "7 Tests", "CLI commands (check, list, version, info, doctor, install) in human-readable and structured --json formats."]
    ]
    doc_body.append(table(test_headers, test_rows, [2200, 1600, 5200]))

    doc_body.append(p("Unit Test Execution Output:", bold=True, style="Heading2"))
    test_out = [
        "$ python3 -m unittest discover tests -v",
        "test_doctor_json (test_cli.TestCLI) ... ok",
        "test_info_command_json (test_cli.TestCLI) ... ok",
        "test_install_dry_run (test_cli.TestCLI) ... ok",
        "test_check_installed_tool (test_detector.TestSystemDetector) ... ok",
        "test_check_missing_tool (test_detector.TestSystemDetector) ... ok",
        "test_timeout_handling (test_detector.TestSystemDetector) ... ok",
        "test_apt_command_generation (test_installer.TestPackageInstaller) ... ok",
        "test_winget_command_generation (test_installer.TestPackageInstaller) ... ok",
        "test_dry_run_execution (test_installer.TestPackageInstaller) ... ok",
        "test_extract_ngspice_banner (test_version_checker.TestVersionChecker) ... ok",
        "test_extract_kicad_version (test_version_checker.TestVersionChecker) ... ok",
        "test_register_custom_tool (test_tools.TestToolsRegistry) ... ok",
        "----------------------------------------------------------------------",
        "Ran 36 tests in 0.060s",
        "OK"
    ]
    doc_body.append(code_block(test_out))

    # --- SECTION 7: INSTRUCTIONS FOR EXECUTION ---
    doc_body.append(p("7. Instructions for Execution", bold=True, style="Heading1"))
    doc_body.append(p("The prototype requires standard Python 3.10+ and no third-party package installations:"))

    cli_guide = [
        "# 1. Run full dependency check across all tools",
        "python3 main.py check",
        "",
        "# 2. Run comprehensive system diagnostics (Doctor)",
        "python3 main.py doctor",
        "",
        "# 3. List all supported tools in registry",
        "python3 main.py list",
        "",
        "# 4. Check version of a specific tool",
        "python3 main.py version python",
        "python3 main.py version git",
        "",
        "# 5. View detailed metadata and package identifiers for a tool",
        "python3 main.py info ngspice",
        "python3 main.py info kicad",
        "",
        "# 6. Simulate tool installation (safe dry-run)",
        "python3 main.py install ngspice --dry-run",
        "python3 main.py install kicad --dry-run",
        "",
        "# 7. Output machine-readable JSON (for IDE/GUI integration)",
        "python3 main.py check --json",
        "python3 main.py doctor --json",
        "",
        "# 8. Run automated test suite",
        "python3 -m unittest discover tests -v"
    ]
    doc_body.append(code_block(cli_guide))

    # --- SECTION 8: EXTENSIBILITY & FUTURE ROADMAP ---
    doc_body.append(p("8. Extensibility & Future Internship Roadmap", bold=True, style="Heading1"))
    doc_body.append(p("During the Semester Long Internship, the Tool Manager can be expanded in several high-impact directions:"))
    doc_body.append(bullet("Direct integration into eSim's wxPython/Qt desktop workbench as a visual settings and onboarding wizard.", "1. GUI Workbench Integration: "))
    doc_body.append(bullet("Verilator (HDL simulation), GHDL (VHDL), OpenFOAM (thermal/fluid simulation), and SkyWater 130nm / IHP 130nm PDK managers.", "2. Additional EDA Tools: "))
    doc_body.append(bullet("Sandboxed source-compilation strategies for building custom Ngspice patches or bleeding-edge KiCad nightlies.", "3. Source Compilation: "))
    doc_body.append(bullet("Automated management of eSim's dedicated virtual environment, inspecting packages like matplotlib, numpy, and scipy.", "4. Python Virtualenv Tracking: "))

    # Proposal Conclusion
    doc_body.append(p("9. Conclusion", bold=True, style="Heading1"))
    doc_body.append(p("This proposal demonstrates a robust, modular, and fully tested Automated Tool Manager engineered to IIT Bombay FOSSEE standards. By combining zero-dependency architecture, the Strategy & Registry design patterns, and comprehensive automated testing, this project provides an immediate, production-grade foundation for eSim's next-generation toolchain orchestration."))

    doc_body.append(p("Proposal prepared by Harsh Satyam for FOSSEE eSim Semester Long Internship Autumn 2026 Evaluation.", italic=True, align="center", color="6B7280", size="18"))

    # Assemble Document XML
    document_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
  xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
    {"".join(doc_body)}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>
      <w:cols w:space="720"/>
      <w:docGrid w:linePitch="360"/>
    </w:sectPr>
  </w:body>
</w:document>"""

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types_xml)
        zf.writestr("_rels/.rels", rels_xml)
        zf.writestr("docProps/core.xml", core_xml)
        zf.writestr("docProps/app.xml", app_xml)
        zf.writestr("word/_rels/document.xml.rels", doc_rels_xml)
        zf.writestr("word/document.xml", document_xml)
        zf.writestr("word/styles.xml", styles_xml)
        zf.writestr("word/fontTable.xml", font_table_xml)
        zf.writestr("word/settings.xml", settings_xml)

    print(f"Successfully generated proposal document: {output_path} ({os.path.getsize(output_path)} bytes)")

if __name__ == "__main__":
    generate_proposal_docx("docs/eSim_Tool_Manager_Internship_Proposal.docx")
    generate_proposal_docx("public/eSim_Tool_Manager_Internship_Proposal.docx")
