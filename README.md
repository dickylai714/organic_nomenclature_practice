```markdown
# 🧪 Organic Nomenclature Practice for HKDSE Chemistry

An interactive web application designed to help secondary school students, particularly those preparing for the HKDSE Chemistry exam, master the art of IUPAC nomenclature for organic compounds. This tool provides a dynamic and engaging way to practice naming a wide range of molecules.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-name.streamlit.app/)
*(Replace the link above with your actual Streamlit Community Cloud URL)*

![App Screenshot](https://i.imgur.com/your-screenshot.png)
*(Suggestion: Add a screenshot of your app here)*

## ✨ Features

This application is built to provide a robust and user-friendly practice experience:

* **Comprehensive Question Bank**: Covers a wide array of compound families relevant to the HKDSE curriculum, including:
    * Straight-chain and Branched Alkanes
    * Alkenes (including dienes)
    * Alkanols (Alcohols)
    * Haloalkanes
    * Carboxylic Acids
    * Compounds with Mixed Functional Groups
* **Customizable Quizzes**: Tailor your practice sessions by selecting specific compound categories and difficulty levels (Easy, Medium, Hard).
* **Multiple Structure Views**: Visualize molecules in different ways to build familiarity:
    * **Skeletal Formula**: The standard for quick representation.
    * **Full Structural Formula**: Shows all atoms (including Carbon and Hydrogen) and bonds.
    * **Condensed Formula**: A text-based representation.
* **Instant Feedback**: Check your answers immediately to reinforce learning. The app accepts preferred IUPAC names as well as common valid alternatives.
* **AI-Powered Explanations**: For incorrect answers, the app leverages the Google Gemini AI to provide step-by-step explanations, helping you understand the logic behind the correct name.

## 🚀 How to Run the App

You can run this application locally on your own machine or deploy it easily.

### Prerequisites

* Python 3.8+
* `pip` package installer

### 1. Clone the Repository

First, get a copy of the project on your local machine:
```bash
git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
cd your-repository-name
```

### 2. Install Dependencies

The project requires several Python packages and some system-level libraries for image generation.

**System Libraries (For Debian/Ubuntu-based systems):**
These are needed by the RDKit library to draw the molecule images correctly.
```bash
sudo apt-get update && sudo apt-get install -y libxrender1 libcairo2 libpng16-16 libfreetype6 libfontconfig1
```
*(These packages are listed in `packages.txt` and are installed automatically if you use the provided Dev Container.)*

**Python Packages:**
Install all the required Python packages using the `requirements.txt` file.
```bash
pip install -r requirements.txt
```
This will install `streamlit`, `rdkit-pypi`, `google-genai`, and other necessary libraries.

### 3. Set Up Your API Key

The AI explanation feature requires a Google Generative AI API key.

1.  Create a folder named `.streamlit` in the root of your project directory.
2.  Inside this folder, create a file named `secrets.toml`.
3.  Add your API key to this file as shown below:
    ```toml
    GENAI_API_KEY = "YOUR_API_KEY_HERE"
    ```
This method keeps your API key secure and is the recommended approach for Streamlit apps.

### 4. Run the Streamlit App

Once the setup is complete, you can run the application with a single command:
```bash
streamlit run streamlit_app.py
```
Your web browser should open a new tab with the running application.

## ☁️ Development and Deployment

### Using GitHub Codespaces

This project is configured to work out-of-the-box with GitHub Codespaces. The `.devcontainer/devcontainer.json` file sets up a complete development environment in the cloud, automatically installing all dependencies and running the app. Simply open this repository in a Codespace, and the application will be ready to use and edit.

### Deploying on Streamlit Community Cloud

This app is ideal for deployment on the Streamlit Community Cloud, allowing you to share it with students and colleagues for free.

1.  Push your project to a GitHub repository.
2.  Sign up for Streamlit Community Cloud and connect your GitHub account.
3.  Deploy your app and remember to add your `GENAI_API_KEY` in the advanced settings under "Secrets".

```