This proposal outlines a modular and extensible Python-based architecture for your CV, cover letter, and now, comprehensive technical proposal generation system. The design prioritizes separation of concerns, testability, and adaptability for future enhancements, including a web-based interface and broader support for different application types (e.g., job applications, consultancy proposals).

### **I. Core Principles:**

* **Modularity:** Each distinct function (data input, LLM interaction, content generation for a specific document type, output formatting) resides in its own module or package.  
* **Separation of Concerns:** Business logic (e.g., prompt engineering, tailoring strategy) is distinct from infrastructure concerns (e.g., API calls, file I/O, database interaction).  
* **Abstraction:** Interfaces are defined for components like the LLM interaction, allowing for different LLM providers or models to be swapped out with minimal changes (model agnosticism).  
* **Configuration-driven:** Key parameters (e.g., file paths, LLM settings, prompt templates, document types) are managed through configuration files or environment variables.  
* **Testability:** Smaller, focused modules are easier to unit test.  
* **Scalability & Extensibility:** Clear separation makes it easier to add new features (e.g., new document types, different output formats, user management) or scale existing ones.

### **II. Current Directory & Module Structure:**

kazi/  
├── app/                          \# For the future web application (e.g., Flask/Django)  
│   ├── static/  
│   ├── templates/  
│   ├── main.py                   \# Web app entry point  
│   ├── routes.py                 \# Web app routes (handling different application types)  
│   ├── forms.py                  \# Web forms (e.g., selecting application type)  
│   └── services.py               \# Services for web app logic, interacting with core  
│  
├── core/                         \# Core business logic and processing  
│   ├── \_\_init\_\_.py  
│   ├── orchestrator.py           \# Main workflow controller, directs appropriate generators  
│   ├── jd\_analyzer.py            \# Handles JD parsing and analysis (Prompt 1 logic)  
│   ├── tor\_analyzer.py           \# Handles Terms of Reference (TOR) parsing for consultancies (Prompt 6\)  
│   │  
│   ├── document\_generators/      \# Package for specific document generation modules  
│   │   ├── \_\_init\_\_.py  
│   │   ├── base\_generator.py     \# (Optional) Abstract base class for generators  
│   │   ├── cv\_generator.py       \# Handles CV tailoring and assembly (Prompts 2, part of 4\)  
│   │   ├── cover\_letter\_generator.py \# Handles cover letter generation (Prompt 5\)  
│   │   ├── technical\_proposal\_generator.py \# Generates sections of technical proposals (Prompts 7, 8, 9, 10, 11, 12, 13\)  
│   │   ├── financial\_proposal\_generator.py \# (Future) For consultancy financial proposals  
│   │   └── work\_plan\_generator.py          \# (Future) For detailed work plan generation within proposals  
│   │  
│   ├── content\_synthesizer.py    \# Generates shared content like professional summary, strategic fit (Prompt 3\)  
│   └── llm\_interface.py          \# Abstract interface for LLM interactions  
│  
├── data\_management/              \# Handles all data input, output, and storage  
│   ├── \_\_init\_\_.py  
│   ├── input\_handler.py          \# PDF, JSON reading (JDs, TORs, master CV)  
│   ├── output\_handler.py         \# Saving text/Markdown/JSON files  
│   ├── cv\_parser.py              \# (Future) Parsing and structuring of master CV data (if not manual JSON)  
│   └── db\_connector.py           \# (Future) For database interactions (CV database, user data)  
│  
├── prompts/                      \# Stores prompt templates, organized by document type  
│   ├── \_\_init\_\_.py  
│   ├── prompt\_loader.py          \# Loads and manages prompt templates  
│   └── templates/  
│       ├── common/  
│       │   └── jd\_analysis\_prompt.txt  
│       │   └── summary\_generation\_prompt.txt  
│       ├── cv/  
│       │   └── cv\_tailoring\_prompt.txt  
│       │   └── cv\_assembly\_prompt.txt  
│       ├── cover\_letter/  
│       │   └── cover\_letter\_generation\_prompt.txt  
│       └── consultancy/  
│           ├── tor\_analysis\_prompt.txt             \# Prompt 6: ToR analysis into JSON  
│           ├── technical\_approach\_framework\_prompt.txt \# Prompt 7: Proposed framework table (Section 6.1)  
│           ├── understanding\_assignment\_prompt.txt   \# Prompt 8: Type & Understanding (Sections 4 & 5\)  
│           ├── technical\_approach\_details\_prompt.txt \# Prompt 9: Detailed tech approach (Sections 6.2-6.10)  
│           ├── work\_plan\_deliverables\_prompt.txt   \# Prompt 10: Work Plan & Deliverables (Section 7\)  
│           ├── general\_management\_sections\_prompt.txt \# Prompt 11: QA, Management, Ethical, Compliance (Sections 10-13)  
│           ├── team\_and\_experience\_sections\_prompt.txt \# Prompt 12: Team & Past Experience (Sections 8 & 9\)  
│           └── executive\_summary\_prompt.txt        \# Prompt 13: Executive Summary (Section 3\)  
│  
├── utils/                        \# General utility functions  
│   ├── \_\_init\_\_.py  
│   ├── text\_utils.py             \# Text processing, JSON extraction  
│   └── static\_content\_builder.py \# Builds static/common Markdown parts (e.g., CV sections)  
│  
├── config/                       \# Configuration files  
│   ├── \_\_init\_\_.py  
│   ├── settings.py               \# App settings, API keys, paths  
│   └── logging\_config.py         \# (Future) Logging configuration  
│  
├── tests/                        \# Unit and integration tests  
│   ├── core/  
│   │   └── document\_generators/  
│   ├── data\_management/  
│   └── utils/  
│  
├── run.py                        \# Main entry point for CLI execution  
├── requirements.txt  
└── .env                          \# Environment variables (API keys, etc.)

### **III. Reasoning and Component Breakdown (Current State):**

1. **core/orchestrator.py**: Has become the central control for different application types. It now dynamically selects and executes a sequence of document generation steps based on the \--type argument (e.g., job or consultancy). It orchestrates all the prompt calls and file saving.  
2. **core/tor\_analyzer.py**: Fully implemented. It takes a ToR PDF and processes it using Prompt 6 to extract and structure all key information into a JSON object.  
3. **document\_generators/technical\_proposal\_generator.py**: Fully implemented. This single module now encapsulates the logic for generating *all* the core textual sections of a technical proposal (Sections 3, 4, 5, 6.1, 6.2-6.10, 7, 8, 9, 10, 11, 12, 13\) by calling various dedicated prompts (Prompts 7-13). It also includes the assemble\_technical\_proposal\_markdown function for final document consolidation.  
4. **prompts/templates/consultancy/**: This directory is now fully populated with all the specific prompt templates (Prompts 6-13) tailored for each part of the ToR analysis and proposal generation.  
5. **data\_management/input\_handler.py**: Updated to specifically handle reading ToR PDFs from the tor\_storage directory.  
6. **data\_management/output\_handler.py**: Used across all stages to save the intermediate and final Markdown/JSON outputs.  
7. **config/settings.py**: Updated to define the TOR\_STORAGE\_DIR.  
8. **run.py**: Now accepts a \--type argument (job or consultancy) to switch between the CV/Cover Letter pipeline and the new Technical Proposal pipeline.

### **IV. Progress & Next Steps:**

You have successfully built a robust pipeline for generating a significant portion of a technical proposal. All the logical steps for content generation and consolidation (excluding cover page and annexes which are typically separate files/processes) are now in place.

**Next considerations:**

1. **Refinement of Generated Content:** Now that you have the full proposal in Markdown, you can review the quality of the generated text. This might involve:  
   * Tweaking prompt instructions (e.g., asking for more conciseness, specific phrasing, tone adjustments).  
   * Experimenting with different LLM models or temperatures in settings.py.  
   * Adding post-processing (e.g., a spell checker or grammar checker) if needed.  
2. **Cover Page (Section 1):** While we have a basic placeholder in the assemble\_technical\_proposal\_markdown function, a true Cover Page usually involves more design and specific data (e.g., client logo, custom layouts). This could be a future enhancement if you need it to be fully auto-generated.  
3. **Annexes (Section 14):** Annexes (like detailed CVs, organograms, supporting documents) are typically separate files. The system currently generates a master\_cv\_full.md (via generate\_master\_cv\_markdown if you run generate\_master\_cv\_md.py directly). You might want to consider:  
   * A pipeline step to generate the detailed CVs of *all* team members if your master\_cv.json is expanded.  
   * A plan for *how* these annexes will be bundled or referenced in the final submission.  
4. **PDF Conversion of the Full Proposal:** You have convert\_submissions\_to\_pdf.py which takes a Markdown file and converts it to PDF. You can now use this script on your \_full\_technical\_proposal\_\*.md file to generate a PDF.  
   python kazi-main/submissions/convert\_submissions\_to\_pdf.py "path/to/your\_full\_technical\_proposal\_file.md"

   (You might need to adjust the CSS resume\_markdown\_pdf\_style.css or create a new one for proposals to control fonts, headings, page breaks, etc., more precisely for multi-page documents).

