# Multilingual AI Chatbot

A production-ready multilingual AI chatbot with RAG (Retrieval Augmented Generation) architecture. The chatbot supports 100+ languages, uses semantic search to find relevant information, and generates intelligent answers using Google Vertex AI (Gemini 2.5 Flash).

## Features

- **Multilingual Support**: Automatically detects and handles 100+ languages
- **AI-Powered Answers**: Uses Vertex AI (Gemini 2.5 Flash) to generate contextual, intelligent responses
- **Semantic Search**: FAISS vector database for efficient similarity search across 4000+ FAQ pairs
- **RAG Architecture**: Retrieves relevant context and synthesizes answers specific to user questions
- **Modern UI**: Clean, professional Streamlit interface inspired by ChatGPT
- **Free Embeddings**: Uses HuggingFace embeddings by default (no OpenAI credits required)

## Table of Contents

- [Prerequisites](#prerequisites)
- [Google Cloud Setup](#google-cloud-setup)
  - [Step 1: Create a Google Cloud Project](#step-1-create-a-google-cloud-project)
  - [Step 2: Enable Required APIs](#step-2-enable-required-apis)
  - [Step 3: Create a Service Account](#step-3-create-a-service-account)
  - [Step 4: Download Service Account Key](#step-4-download-service-account-key)
  - [Step 5: Set Up Billing (Free Tier)](#step-5-set-up-billing-free-tier)
- [Local Setup](#local-setup)
  - [Step 1: Clone the Repository](#step-1-clone-the-repository)
  - [Step 2: Install Python](#step-2-install-python)
  - [Step 3: Create Virtual Environment](#step-3-create-virtual-environment)
  - [Step 4: Install Dependencies](#step-4-install-dependencies)
  - [Step 5: Configure Environment Variables](#step-5-configure-environment-variables)
  - [Step 6: Initialize Vector Store](#step-6-initialize-vector-store)
  - [Step 7: Test the Setup](#step-7-test-the-setup)
  - [Step 8: Run the Application](#step-8-run-the-application)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Configuration Options](#configuration-options)
- [License](#license)

## Prerequisites

Before you begin, ensure you have:

- **Python 3.10 or higher** installed ([Download Python](https://www.python.org/downloads/))
- **Google Cloud Account** (free tier available)
- **Git** installed (for cloning the repository)
- **Text Editor** or IDE (VS Code, PyCharm, etc.)

## Google Cloud Setup

### Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Sign in with your Google account
3. Click on the project dropdown at the top of the page
4. Click **"New Project"**
5. Enter a project name (e.g., "multilingual-chatbot")
6. Optionally, select an organization
7. Click **"Create"**
8. Wait for the project to be created (usually takes a few seconds)
9. **Important**: Note down your **Project ID** (not the project name). It will look like `multilingual-chatbot-123456`

### Step 2: Enable Required APIs

You need to enable two APIs for this project:

#### Enable Vertex AI API

1. In the Google Cloud Console, go to **"APIs & Services" > "Library"**
2. Search for **"Vertex AI API"**
3. Click on **"Vertex AI API"**
4. Click **"Enable"**
5. Wait for the API to be enabled (may take 1-2 minutes)

#### Enable Cloud Translation API

1. Still in the **"APIs & Services" > "Library"** section
2. Search for **"Cloud Translation API"**
3. Click on **"Cloud Translation API"**
4. Click **"Enable"**
5. Wait for the API to be enabled

**Alternative Method (Faster)**:
- Go to [Enable Vertex AI API](https://console.cloud.google.com/apis/library/aiplatform.googleapis.com)
- Go to [Enable Translation API](https://console.cloud.google.com/apis/library/translate.googleapis.com)

### Step 3: Create a Service Account

A service account allows your local application to authenticate with Google Cloud services.

1. In Google Cloud Console, go to **"IAM & Admin" > "Service Accounts"**
2. Click **"Create Service Account"**
3. Enter a service account name (e.g., "chatbot-service")
4. Enter a description (optional): "Service account for multilingual chatbot"
5. Click **"Create and Continue"**
6. **Grant Roles**:
   - Click **"Select a role"**
   - Add these roles one by one:
     - **"Vertex AI User"** (for Vertex AI API access)
     - **"Cloud Translation API User"** (for Translation API access)
   - Click **"Continue"**
7. Click **"Done"** (you can skip the optional step of granting users access)

### Step 4: Download Service Account Key

1. In the **"Service Accounts"** page, find the service account you just created
2. Click on the service account email
3. Go to the **"Keys"** tab
4. Click **"Add Key" > "Create new key"**
5. Select **"JSON"** as the key type
6. Click **"Create"**
7. A JSON file will be downloaded automatically
8. **Important**: 
   - Rename this file to `gcp-credentials.json`
   - Move it to your project root directory (same folder as `app.py`)
   - **Never commit this file to Git** (it's already in `.gitignore`)

### Step 5: Set Up Billing (Free Tier)

Even though you'll use the free tier, Google Cloud requires a billing account to be linked:

1. Go to **"Billing"** in the Google Cloud Console
2. Click **"Link a billing account"** or **"Manage billing accounts"**
3. If you don't have a billing account:
   - Click **"Create billing account"**
   - Fill in your payment information (credit card required)
   - **Don't worry**: You won't be charged if you stay within free tier limits
4. Link your billing account to your project
5. **Set up billing alerts** (recommended):
   - Go to **"Billing" > "Budgets & alerts"**
   - Create a budget alert for $5-10 to get notified if you exceed free tier

**Free Tier Limits** (per month):
- **Cloud Translation API**: 500,000 characters free
- **Vertex AI**: 15 requests per minute free
- **Cloud Run**: 2 million requests free (if deploying)

## Local Setup

### Step 1: Clone the Repository

```bash
git clone <your-repository-url>
cd Chatbot
```

Or if you're working with a local folder, navigate to your project directory.

### Step 2: Install Python

**Windows**:
1. Download Python from [python.org](https://www.python.org/downloads/)
2. During installation, check **"Add Python to PATH"**
3. Verify installation:
   ```bash
   python --version
   ```
   Should show Python 3.10 or higher

**Linux/Mac**:
```bash
python3 --version
```

If Python is not installed:
- **Ubuntu/Debian**: `sudo apt-get install python3 python3-venv python3-pip`
- **macOS**: `brew install python3`

### Step 3: Create Virtual Environment

**Windows**:
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac**:
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt, indicating the virtual environment is active.

**Alternative**: Use the provided installation scripts:
- **Windows**: Run `install.bat`
- **Linux/Mac**: Run `chmod +x install.sh && ./install.sh`

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages:
- `streamlit` - Web UI framework
- `langchain` - LLM orchestration
- `langchain-google-vertexai` - Vertex AI integration
- `langchain-community` - Community integrations (FAISS, HuggingFace)
- `google-cloud-translate` - Translation API
- `sentence-transformers` - HuggingFace embeddings
- `faiss-cpu` - Vector similarity search
- `python-dotenv` - Environment variable management

### Step 5: Configure Environment Variables

1. Create a `.env` file in the project root directory (same folder as `app.py`)

2. Add the following content to `.env`:

```env
# Google Cloud Configuration
GCP_PROJECT_ID=your-project-id-here
GCP_REGION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=./gcp-credentials.json

# Optional: OpenAI Configuration (only if you want to use OpenAI embeddings)
# OPENAI_API_KEY=your-openai-api-key-here
# USE_OPENAI_EMBEDDINGS=false
```

3. Replace `your-project-id-here` with your actual Google Cloud Project ID (from Step 1)
4. Ensure `gcp-credentials.json` is in the project root directory (from Step 4 of Google Cloud Setup)
5. The `GCP_REGION` can be changed to your preferred region (e.g., `us-east1`, `europe-west1`)

**Important**: 
- The `.env` file is already in `.gitignore` and won't be committed to Git
- Never share your `.env` file or `gcp-credentials.json` publicly

### Step 6: Initialize Vector Store

The vector store needs to be created from your FAQ data:

```bash
python setup.py
```

This will:
1. Load FAQs from `faqs.json`
2. Create embeddings using HuggingFace (free) or OpenAI (if configured)
3. Build and save the FAISS index to `faiss_index/` directory

**First run**: This may take 5-10 minutes as it downloads the HuggingFace model (~90MB) and creates embeddings for all FAQs.

**Subsequent runs**: Much faster as the index is cached.

### Step 7: Test the Setup

Verify all services are working correctly:

```bash
python test_services.py
```

This will test:
- ✅ Translation service (language detection and translation)
- ✅ Vector store service (FAQ search)
- ✅ Vertex AI service (answer generation)

All tests should pass.

### Step 8: Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will:
1. Start a local web server
2. Open your default browser automatically
3. Display the chatbot interface at `http://localhost:8501`

**First run**: You may see a spinner saying "Initializing services... This may take a minute on first run." This is normal as services load. The terminal will show progress messages.

**To stop the application**: Press `Ctrl+C` in the terminal.

## Project Structure

```
Chatbot/
├── app.py                      # Main Streamlit application
├── translation_service.py      # Google Cloud Translation API wrapper
├── vectorstore_service.py      # FAISS vector search service
├── vertexai_service.py         # Vertex AI (Gemini) integration
├── setup.py                    # Initialize vector store script
├── test_services.py            # Test suite for all services
├── faqs.json                   # Knowledge base (4000+ Q&A pairs)
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create this)
├── gcp-credentials.json        # GCP service account key (download from GCP)
├── .gitignore                  # Git ignore rules
├── install.bat                 # Windows installation script
├── install.sh                  # Linux/Mac installation script
└── README.md                   # This file
```

## Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/) - Python web framework
- **Translation**: [Google Cloud Translation API](https://cloud.google.com/translate) - 100+ languages
- **Embeddings**: 
  - [HuggingFace Sentence Transformers](https://www.sbert.net/) (default, free)
  - [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings) (optional, paid)
- **Vector Database**: [FAISS](https://github.com/facebookresearch/faiss) - Facebook AI Similarity Search
- **LLM**: [Google Vertex AI](https://cloud.google.com/vertex-ai) - Gemini 2.5 Flash
- **Framework**: [LangChain](https://www.langchain.com/) - LLM application framework

## Configuration Options

### Using OpenAI Embeddings (Optional)

If you prefer OpenAI embeddings over HuggingFace:

1. Get an OpenAI API key from [platform.openai.com](https://platform.openai.com/)
2. Add to `.env`:
   ```env
   OPENAI_API_KEY=sk-your-key-here
   USE_OPENAI_EMBEDDINGS=true
   ```
3. Rebuild the vector store: `python setup.py`

**Note**: OpenAI embeddings require credits. HuggingFace embeddings are free and work well.

### Changing the Region

Update `GCP_REGION` in `.env`:
- `us-central1` (Iowa) - Default
- `us-east1` (South Carolina)
- `europe-west1` (Belgium)
- `asia-southeast1` (Singapore)

Check [Vertex AI locations](https://cloud.google.com/vertex-ai/docs/general/locations) for available regions.

### Adjusting RAG Parameters

In `app.py`, you can modify:
- `k=5` in `get_relevant_context()` - Number of FAQs to retrieve (default: 5)
- `temperature=0.4` in `vertexai_service.py` - AI creativity (0.0-1.0)
- `max_output_tokens=2048` - Maximum answer length

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues:
1. Review Google Cloud Console for API errors
2. Check that all environment variables are set correctly
3. Verify service account permissions

---

**Built with ❤️ using Google Cloud, LangChain, and Streamlit**
