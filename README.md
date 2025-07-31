# Kazi - AI-Powered CV & Proposal Generator

Kazi is a Python-based system designed to automate the generation of tailored job application materials using AI. It analyzes Job Descriptions (JDs) or Terms of Reference (ToRs) and uses Large Language Models (specifically Google Gemini API) to produce customized CVs, cover letters, and technical proposals.

## 🚀 Features

- **Multi-Pipeline Support**: Job applications, consultancy proposals, and tailored consultancy work
- **AI-Powered Analysis**: Advanced JD/ToR analysis using Google Gemini API
- **Database Integration**: MySQL database for consultant and firm data management
- **Flexible Input**: Supports both PDF and TXT file formats
- **Professional Output**: Generates polished CVs, cover letters, and technical proposals
- **Interactive Team Selection**: Choose consultants and firms for proposals
- **PDF Export**: Convert generated documents to PDF format

## 🏗️ Architecture

The system follows a modular architecture with clear separation between:
- **Core Logic**: JD/ToR analysis, CV generation, proposal creation
- **Data Management**: Database operations, file handling
- **Document Generation**: CV, cover letter, and proposal assembly
- **Utilities**: PDF conversion, text processing, formatting

## 📋 Prerequisites

- Python 3.8+
- MySQL database
- Google Gemini API key
- Required Python packages (see `requirements.txt`)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/kazi.git
   cd kazi
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp env.template .env
   # Edit .env with your actual values
   ```

5. **Set up database**
   - Create a MySQL database
   - Use `database_schema_template.sql` as reference
   - Update database connection settings in `config/settings.py`

6. **Prepare data files**
   - Copy `master_cv_template.json` to `cv_data/master_cv.json`
   - Fill in your personal information
   - Add JD/ToR files to `jd_storage/` or `tor_storage/`

## 🔧 Configuration

### Environment Variables
Create a `.env` file with the following variables:
- `GOOGLE_API_KEY`: Your Google Gemini API key
- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`: Database connection details

### Database Setup
1. Create a MySQL database named `kazi_db`
2. Import the schema from `database_schema_template.sql`
3. Add your consultant and firm data

### File Structure
```
kazi/
├── jd_storage/          # Job Description files
├── tor_storage/         # Terms of Reference files
├── cv_data/            # CV data files
├── output/             # Generated outputs
├── config/             # Configuration files
├── core/               # Core application logic
├── data_management/    # Database and file operations
├── prompts/            # AI prompt templates
└── utils/              # Utility functions
```

## 🚀 Usage

### Job Application Pipeline
Generate tailored CVs and cover letters for job applications:
```bash
python run.py job_description.pdf --type job --consultant-email "your@email.com"
```

### Consultancy Proposal Pipeline
Generate technical proposals for consultancy work:
```bash
python run.py terms_of_reference.pdf --type consultancy-tailored
```

### Output
Generated files are saved in timestamped folders under `output/`:
- `output/job/` - CVs and cover letters
- `output/consultancy-tailored/` - Technical proposals

## 🔒 Security & Privacy

### Important Security Notes
- **Never commit sensitive files**: Personal CV data, API keys, database dumps
- **Use environment variables**: Store API keys and database credentials in `.env`
- **Template files**: Use provided templates as starting points
- **Data sanitization**: Remove personal information before sharing

### Files to Never Commit
- `master_cv.json` - Contains personal information
- `kazi_db.sql` - Database dump with personal data
- `.env` - Environment variables with secrets
- `jd_storage/*.pdf` - Client documents
- `tor_storage/*.pdf` - Client documents
- `output/*` - Generated documents with personal info

### Safe to Commit
- Template files (`*_template.*`)
- Source code
- Configuration templates
- Documentation
- Test files

## 📁 File Structure

```
kazi/
├── core/                           # Core application logic
│   ├── document_generators/       # CV, cover letter, proposal generators
│   ├── jd_analyzer.py            # Job description analysis
│   ├── tor_analyzer.py           # Terms of reference analysis
│   └── orchestrator.py           # Pipeline orchestration
├── data_management/               # Data handling
│   ├── db_handler.py             # Database operations
│   ├── input_handler.py          # File input processing
│   └── output_handler.py         # Output file management
├── prompts/                       # AI prompt templates
│   └── templates/
│       ├── cv/                   # CV generation prompts
│       ├── cover_letter/         # Cover letter prompts
│       └── consultancy/          # Proposal generation prompts
├── utils/                         # Utility functions
│   ├── convert_md_to_pdf.py      # PDF conversion
│   └── static_content_builder.py # Content formatting
├── config/                        # Configuration
│   └── settings.py               # Application settings
├── tests/                         # Unit tests
├── requirements.txt               # Python dependencies
├── run.py                        # Main entry point
└── README.md                     # This file
```

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This tool is designed for educational and professional use. Users are responsible for:
- Ensuring they have permission to use any client documents
- Protecting personal and client information
- Complying with relevant data protection regulations
- Using the generated content appropriately

## 🆘 Support

For issues and questions:
1. Check the documentation
2. Review existing issues
3. Create a new issue with detailed information

## 🔄 Version History

- **v1.0.0**: Initial release with job application pipeline
- **v1.1.0**: Added consultancy proposal pipeline
- **v1.2.0**: Database integration and team selection
- **v1.3.0**: Enhanced formatting and chronological ordering 