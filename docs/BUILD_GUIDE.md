# EcoSort AI — Build Guide

## 1. Install the basic tools

Install:
- Python 3.13
- Git for Windows
- Visual Studio Code
- IBM Bob

During Python installation on Windows, enable the option to add Python to PATH.

## 2. Open the project

Open the `EcoSortAI` folder in VS Code.

Open a new terminal in VS Code.

## 3. Create the virtual environment

```powershell
py -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks the activation script, run this only for the current terminal session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate again:

```powershell
.\.venv\Scripts\Activate.ps1
```

## 4. Install packages

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Configure watsonx.ai

Copy `.env.example` to `.env`.

Fill in:

```text
WATSONX_APIKEY
WATSONX_URL
WATSONX_PROJECT_ID
```

The model entries can be changed to models available in your watsonx.ai project.

Never commit `.env` to GitHub.

## 6. Test the IBM connection

Run:

```powershell
python tests\test_watsonx.py
```

A successful response should contain a valid model response. The test prompt asks for `WORKING`.

## 7. Test the retrieval layer

Run:

```powershell
python tests\test_rag.py
```

Review the retrieved categories for each sample query.

## 8. Run the application

```powershell
streamlit run app.py
```

Open the local URL shown in the terminal.

## 9. Basic test cases

Try these inputs:

```text
Used AA battery from a TV remote

Empty plastic water bottle

A banana peel from breakfast

An old mobile phone that no longer works

A cardboard delivery box
```

Also test an intentionally vague item such as:

```text
Some old thing I found in a box
```

The vague input should not be forced into a confident category.

## 10. Image testing

Use a clear photo containing one main object. Try a bottle, can, battery, or old phone.

If the selected vision model is unavailable in the current watsonx.ai environment, keep the text-input path working and select a multimodal model that is available in the project.

## 11. IBM Bob usage

Open the project in IBM Bob. Use the prompts in `BOB_PROMPTS.txt`.

Do not provide Bob with API keys or other secrets.

Keep a record of the useful review and debugging steps for project documentation.

## 12. GitHub setup

Initialize the repository:

```powershell
git init
git add .
git commit -m "Initial EcoSort AI prototype"
```

Create a GitHub repository named `EcoSortAI`, connect the local repository to it, and push the project.

Check the repository before sharing it. `.env` must not be present.

## 13. Streamlit deployment

Deploy the repository through Streamlit Community Cloud.

Use the deployment secrets area for:

```toml
WATSONX_APIKEY = "YOUR_API_KEY"
WATSONX_URL = "YOUR_WATSONX_ENDPOINT"
WATSONX_PROJECT_ID = "YOUR_PROJECT_ID"
WATSONX_TEXT_MODEL = "ibm/granite-4-h-small"
WATSONX_VISION_MODEL = "ibm/granite-vision-3-3-2b"
```

Use model identifiers available in your IBM project if these defaults are not available.

## 14. Final local checks

Before presenting the project, confirm:

- Text input works.
- RAG retrieval works.
- The category is displayed.
- The recommendation is displayed.
- The uncertainty path works.
- The image path works when the selected vision model is available.
- No secret appears in the GitHub repository.
