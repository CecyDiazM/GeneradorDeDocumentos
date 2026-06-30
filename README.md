📄 Automated Document Generator (Generador de Documentos)
A lightweight, efficient automation tool designed to streamline bulk document creation by merging tabular raw data with structured document templates. Built with an intuitive web interface, this application allows teams to upload data sources and document matrices, generating customized, ready-to-sign files in a matter of seconds.

🚀 Key Features
Multi-Format Upload Panel (Carga de Archivos): Supports bulk data parsing from Microsoft Excel spreadsheets (.xlsx, .xls) alongside template layouts in Microsoft Word (.docx).

Automated Data Merging: Instantly cross-references data arrays (such as employee or client parameters) and systematically binds them to variables inside a structured master template.

One-Click Batch Processing (Generar Documentos): Processes and renders multi-file iterations concurrently, bypassing the latency of manual typing or copy-pasting.

Zip Extraction Package: Compresses all individually generated documents into a single download payload (contratos_generados.zip) for convenient, clean local extraction.

🧠 Problems It Solves
Tedious Manual Workflows: Creating high-volume recurring templates—such as employment contracts ("Contrato_Cecilia_Diaz"), payroll receipts, or report cards—is typically prone to manual oversight and fatigue. This tool automates the process flawlessly.

Data Typo and Inconsistency Risks: By pulling row records directly from a spreadsheet, the app eliminates common data-entry typos when mapping personal information like names, ages, salaries, and deduction data ("REPORTE DE DATOS").

Cumbersome Document Merging Systems: Instead of navigating complex mail-merge features inside native office suites, this implementation provides a simple, direct user interface accessible from any browser without complex setup requirements.

🛠️ Built With
Streamlit / Web Frontend: Providing a clean, intuitive dark-themed UI with upload progression states and dynamic success feedback bars.
![Streamlit](https://img.shields.io/badge/Streamlit-%23FE4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)

Python: Powering the document compilation engines and matrix mapping backend logic.
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
