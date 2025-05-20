# Step 1: Import necessary libraries
import streamlit as st
import base64 # Still used by original format_condensed_formula_html if needed, but not for st.image
from io import BytesIO # Same as above
import random
import re
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem.AllChem import Compute2DCoords
from rdkit.Chem.Draw import rdMolDraw2D # For MolDrawOptions

# For Google GenAI
from google import genai

# --- Configuration & Initialization ---

# IMPORTANT: For Streamlit, it's better to manage API keys using st.secrets
# Create a .streamlit/secrets.toml file with:
# GENAI_API_KEY = "YOUR_API_KEY"

st.set_page_config(page_title="Chemistry Quiz", layout="wide", initial_sidebar_state="collapsed")

try:
    api_key_to_use = st.secrets.get("GENAI_API_KEY")
    gemini_model_name = st.secrets.get("GENAI_MODEL_NAME", "gemini-2.0-flash") # Allow model override via secrets

    if not api_key_to_use:
        # Fallback to your provided key if not in secrets - use with caution
        api_key_to_use = "" # YOUR PROVIDED KEY
        st.warning(
            "⚠️ Using a hardcoded API key from the original script. "
            "For security and best practice, please set `GENAI_API_KEY` in Streamlit Secrets. "
            "The current key may be exposed or invalid."
        )
    
    # User's original Colab script used "gemini-2.0-flash".
    # The GENAI_MODEL_NAME secret allows overriding this if needed.
    # If not set in secrets, it defaults to "gemini-1.5-flash-latest" for broader compatibility.
    # If user's specific "gemini-2.0-flash" is desired and works, they can set it in secrets.
    # For this conversion, I will use the model name from secrets or the default.
    # Let's ensure `gemini_model_name` is used:
    
    genai_model = genai.Client(api_key=api_key_to_use)
    genai_service_available = True
    # Small test to see if model listing works (less intrusive than generating content on startup)
    # list(genai.list_models())
except Exception as e:
    st.error(f"🚨 Failed to initialize Google GenAI service: {e}. \n"
             f"AI features may not work. Ensure API key is valid and model name ('{gemini_model_name}') is correct. \n"
             "You can set `GENAI_API_KEY` and optionally `GENAI_MODEL_NAME` in Streamlit Secrets.")
    genai_model = None
    genai_service_available = False


# @title Question Bank (Keep as is)
practice_problems = [
    # === Straight-chain Alkane ===
    {"smiles": "C", "name": "methane", "condensed": "CH4", "category": "Straight-chain Alkane", "difficulty": "Easy"},
    {"smiles": "CC", "name": "ethane", "condensed": "CH3CH3", "category": "Straight-chain Alkane", "difficulty": "Easy"},
    {"smiles": "CCC", "name": "propane", "condensed": "CH3CH2CH3", "category": "Straight-chain Alkane", "difficulty": "Easy"},
    {"smiles": "CCCC", "name": "butane", "condensed": "CH3CH2CH2CH3", "category": "Straight-chain Alkane", "difficulty": "Medium"},
    {"smiles": "CCCCC", "name": "pentane", "condensed": "CH3(CH2)3CH3", "category": "Straight-chain Alkane", "difficulty": "Medium"},
    {"smiles": "CCCCCC", "name": "hexane", "condensed": "CH3(CH2)4CH3", "category": "Straight-chain Alkane", "difficulty": "Medium"},
    {"smiles": "CCCCCCC", "name": "heptane", "condensed": "CH3(CH2)5CH3", "category": "Straight-chain Alkane", "difficulty": "Difficult"},
    {"smiles": "CCCCCCCC", "name": "octane", "condensed": "CH3(CH2)6CH3", "category": "Straight-chain Alkane", "difficulty": "Difficult"},

    # === Branched Alkane ===
    {"smiles": "CC(C)C", "name": "2-methylpropane", "condensed": "CH3CH(CH3)CH3", "category": "Branched Alkane", "difficulty": "Easy"},
    {"smiles": "CC(C)CC", "name": "2-methylbutane", "condensed": "CH3CH(CH3)CH2CH3", "category": "Branched Alkane", "difficulty": "Medium"},
    {"smiles": "CCC(C)CC", "name": "3-methylpentane", "condensed": "CH3CH2CH(CH3)CH2CH3", "category": "Branched Alkane", "difficulty": "Medium"},
    {"smiles": "CC(C)(C)C", "name": "2,2-dimethylpropane", "condensed": "C(CH3)4", "category": "Branched Alkane", "difficulty": "Medium"},
    {"smiles": "CC(C)CCC", "name": "2-methylpentane", "condensed": "CH3CH(CH3)CH2CH2CH3", "category": "Branched Alkane", "difficulty": "Medium"},
    {"smiles": "CC(C)C(C)C", "name": "2,3-dimethylbutane", "condensed": "CH3CH(CH3)CH(CH3)CH3", "category": "Branched Alkane", "difficulty": "Hard"},
    {"smiles": "CCC(C)(C)CC", "name": "3,3-dimethylpentane", "condensed": "CH3CH2C(CH3)2CH2CH3", "category": "Branched Alkane", "difficulty": "Hard"},
    {"smiles": "CC(C)CC(C)C", "name": "2,4-dimethylpentane", "condensed": "CH3CH(CH3)CH2CH(CH3)CH3", "category": "Branched Alkane", "difficulty": "Hard"},
    {"smiles": "CCC(CC)CCC", "name": "4-ethylheptane", "condensed": "CH3CH2CH2CH(CH2CH3)CH2CH2CH3", "category": "Branched Alkane", "difficulty": "Hard"},
    {"smiles": "CC(C)(C)CC(C)C", "name": "2,2,4-trimethylpentane", "condensed": "(CH3)3CCH2CH(CH3)CH3", "category": "Branched Alkane", "difficulty": "Hard"},

    # === Alkene === (Includes straight and branched)
    {"smiles": "C=C", "name": "ethene", "condensed": "CH2=CH2", "category": "Alkene", "difficulty": "Easy"},
    {"smiles": "CC=C", "name": "propene", "condensed": "CH3CH=CH2", "category": "Alkene", "difficulty": "Easy"},
    {"smiles": "C=CCC", "name": "but-1-ene", "condensed": "CH2=CHCH2CH3", "category": "Alkene", "difficulty": "Medium"},
    {"smiles": "CC=CC", "name": "but-2-ene", "condensed": "CH3CH=CHCH3", "category": "Alkene", "difficulty": "Medium"},
    {"smiles": "C=CCCC", "name": "pent-1-ene", "condensed": "CH2=CHCH2CH2CH3", "category": "Alkene", "difficulty": "Medium"},
    {"smiles": "CC=CCC", "name": "pent-2-ene", "condensed": "CH3CH=CHCH2CH3", "category": "Alkene", "difficulty": "Medium"},
    {"smiles": "CC(C)C=C", "name": "3-methylbut-1-ene", "condensed": "CH3CH(CH3)CH=CH2", "category": "Alkene", "difficulty": "Medium"},
    {"smiles": "C=C(C)CC", "name": "2-methylbut-1-ene", "condensed": "CH2=C(CH3)CH2CH3", "category": "Alkene", "difficulty": "Hard"},
    {"smiles": "CC=C(C)C", "name": "2-methylbut-2-ene", "condensed": "CH3CH=C(CH3)CH3", "category": "Alkene", "difficulty": "Hard"},
    {"smiles": "CCC(C)=CCC", "name": "3-methylhex-3-ene", "condensed": "CH3CH2C(CH3)=CHCH2CH3", "category": "Alkene", "difficulty": "Hard"},

    # === Haloalkane ===
    {"smiles": "C(Cl)", "name": "chloromethane", "condensed": "CH3Cl", "category": "Haloalkane", "difficulty": "Easy"},
    {"smiles": "CCBr", "name": "bromoethane", "condensed": "CH3CH2Br", "category": "Haloalkane", "difficulty": "Easy"},
    {"smiles": "CI", "name": "iodomethane", "condensed": "CH3I", "category": "Haloalkane", "difficulty": "Easy"}, # Added Iodo
    {"smiles": "CF", "name": "fluoromethane", "condensed": "CH3F", "category": "Haloalkane", "difficulty": "Easy"},
    {"smiles": "CCCI", "name": "1-iodopropane", "condensed": "CH3CH2CH2I", "category": "Haloalkane", "difficulty": "Medium"}, # Added Iodo
    {"smiles": "CC(I)C", "name": "2-iodopropane", "condensed": "CH3CHICH3", "category": "Haloalkane", "difficulty": "Medium"}, # Added Iodo
    {"smiles": "CCCCl", "name": "1-chloropropane", "condensed": "CH3CH2CH2Cl", "category": "Haloalkane", "difficulty": "Medium"},
    {"smiles": "CC(Cl)C", "name": "2-chloropropane", "condensed": "CH3CHClCH3", "category": "Haloalkane", "difficulty": "Medium"},
    {"smiles": "C(F)(F)F", "name": "trifluoromethane", "condensed": "CHF3", "category": "Haloalkane", "difficulty": "Medium"},
    {"smiles": "CC(Br)CC", "name": "2-bromobutane", "condensed": "CH3CHBrCH2CH3", "category": "Haloalkane", "difficulty": "Medium"},
    {"smiles": "ClCCBr", "name": "1-bromo-2-chloroethane", "condensed": "ClCH2CH2Br", "category": "Haloalkane", "difficulty": "Hard"},
    {"smiles": "CC(Cl)(I)C", "name": "2-chloro-2-iodopropane", "condensed": "CH3C(Cl)(I)CH3", "category": "Haloalkane", "difficulty": "Hard"}, # Added Iodo
    {"smiles": "FC(Cl)I", "name": "chlorofluoroiodomethane", "condensed": "CHFClI", "category": "Haloalkane", "difficulty": "Hard"}, # Added Iodo

    # === Alkanol ===
    {"smiles": "CO", "name": "methanol", "condensed": "CH3OH", "category": "Alkanol", "difficulty": "Easy"},
    {"smiles": "CCO", "name": "ethanol", "condensed": "CH3CH2OH", "category": "Alkanol", "difficulty": "Easy"},
    {"smiles": "CCCO", "name": "propan-1-ol", "condensed": "CH3CH2CH2OH", "category": "Alkanol", "difficulty": "Medium"},
    {"smiles": "CC(O)C", "name": "propan-2-ol", "condensed": "CH3CH(OH)CH3", "category": "Alkanol", "difficulty": "Medium"},
    {"smiles": "CCCCO", "name": "butan-1-ol", "condensed": "CH3CH2CH2CH2OH", "category": "Alkanol", "difficulty": "Medium"},
    {"smiles": "CC(O)CC", "name": "butan-2-ol", "condensed": "CH3CH(OH)CH2CH3", "category": "Alkanol", "difficulty": "Medium"},
    {"smiles": "CC(C)(O)C", "name": "2-methylpropan-2-ol", "condensed": "(CH3)3COH", "category": "Alkanol", "difficulty": "Hard"},
    {"smiles": "CC(C)CO", "name": "2-methylpropan-1-ol", "condensed": "CH3CH(CH3)CH2OH", "category": "Alkanol", "difficulty": "Hard"},
    {"smiles": "CCC(O)CC", "name": "pentan-3-ol", "condensed": "CH3CH2CH(OH)CH2CH3", "category": "Alkanol", "difficulty": "Hard"},
    {"smiles": "CC(O)C(O)C", "name": "butane-2,3-diol", "condensed": "CH3CH(OH)CH(OH)CH3", "category": "Alkanol", "difficulty": "Hard"},

    # === Carboxylic Acid ===
    {"smiles": "C(=O)O", "name": "methanoic acid", "condensed": "HCOOH", "category": "Carboxylic Acid", "difficulty": "Easy"},
    {"smiles": "CC(=O)O", "name": "ethanoic acid", "condensed": "CH3COOH", "category": "Carboxylic Acid", "difficulty": "Easy"},
    {"smiles": "CCC(=O)O", "name": "propanoic acid", "condensed": "CH3CH2COOH", "category": "Carboxylic Acid", "difficulty": "Medium"},
    {"smiles": "CCCC(=O)O", "name": "butanoic acid", "condensed": "CH3CH2CH2COOH", "category": "Carboxylic Acid", "difficulty": "Medium"},
    {"smiles": "CC(C)C(=O)O", "name": "2-methylpropanoic acid", "condensed": "CH3CH(CH3)COOH", "category": "Carboxylic Acid", "difficulty": "Medium"},
    {"smiles": "CCCCC(=O)O", "name": "pentanoic acid", "condensed": "CH3CH2CH2CH2COOH", "category": "Carboxylic Acid", "difficulty": "Hard"},
    {"smiles": "CC(C)CC(=O)O", "name": "3-methylbutanoic acid", "condensed": "CH3CH(CH3)CH2COOH", "category": "Carboxylic Acid", "difficulty": "Hard"},
    {"smiles": "C(C(=O)O)C(=O)O", "name": "propanedioic acid", "condensed": "HOOCCH2COOH", "category": "Carboxylic Acid", "difficulty": "Hard"},
    {"smiles": "CC(Cl)C(=O)O", "name": "2-chloropropanoic acid", "condensed": "CH3CH(Cl)COOH", "category": "Carboxylic Acid", "difficulty": "Hard"}, # Also Mixed

    # === Mixed Functional Groups === (Focusing on combinations taught in S4, avoiding primary ketones)
    # Alkanol + Alkene
    {"smiles": "CC(O)C=C", "name": "but-3-en-2-ol", "condensed": "CH2=CHCH(OH)CH3", "category": "Mixed Functional Groups", "difficulty": "Medium"},
    {"smiles": "C=CCCO", "name": "but-3-en-1-ol", "condensed": "CH2=CHCH2CH2OH", "category": "Mixed Functional Groups", "difficulty": "Medium"},
    {"smiles": "CC=CC(O)C", "name": "pent-3-en-2-ol", "condensed": "CH3CH=CHCH(OH)CH3", "category": "Mixed Functional Groups", "difficulty": "Hard"},
    {"smiles": "C=C(C)CO", "name": "2-methylprop-2-en-1-ol", "condensed": "CH2=C(CH3)CH2OH", "category": "Mixed Functional Groups", "difficulty": "Hard"},

    # Alkanol + Haloalkane
    {"smiles": "OCCBr", "name": "2-bromoethanol", "condensed": "HOCH2CH2Br", "category": "Mixed Functional Groups", "difficulty": "Medium"},
    {"smiles": "ClCC(O)C", "name": "1-chloropropan-2-ol", "condensed": "ClCH2CH(OH)CH3", "category": "Mixed Functional Groups", "difficulty": "Medium"},
    {"smiles": "CC(O)CI", "name": "1-iodopropan-2-ol", "condensed": "ICH2CH(OH)CH3", "category": "Mixed Functional Groups", "difficulty": "Hard"}, # Added iodo
    {"smiles": "C=CC(Br)CO", "name": "2-bromobut-3-en-1-ol", "condensed": "CH2=CHCH(Br)CH2OH", "category": "Mixed Functional Groups", "difficulty": "Hard"},

    # Alkene + Haloalkane
    {"smiles": "C=CCl", "name": "chloroethene", "condensed": "CH2=CHCl", "category": "Mixed Functional Groups", "difficulty": "Easy"},
    {"smiles": "BrC=C", "name": "bromoethene", "condensed": "CHBr=CH2", "category": "Mixed Functional Groups", "difficulty": "Easy"},
    {"smiles": "C=CI", "name": "iodoethene", "condensed": "CH2=CHI", "category": "Mixed Functional Groups", "difficulty": "Easy"}, # Added iodo
    {"smiles": "ClC=CCl", "name": "1,2-dichloroethene", "condensed": "CHCl=CHCl", "category": "Mixed Functional Groups", "difficulty": "Medium"},
    {"smiles": "C=CCBr", "name": "3-bromoprop-1-ene", "condensed": "CH2=CHCH2Br", "category": "Mixed Functional Groups", "difficulty": "Medium"},

    # Carboxylic Acid + Alkene (Unsaturated Acids)
    {"smiles": "C=CC(=O)O", "name": "propenoic acid", "condensed": "CH2=CHCOOH", "category": "Mixed Functional Groups", "difficulty": "Medium"},
    {"smiles": "CC=CC(=O)O", "name": "but-2-enoic acid", "condensed": "CH3CH=CHCOOH", "category": "Mixed Functional Groups", "difficulty": "Medium"},
    {"smiles": "C=C(C)C(=O)O", "name": "2-methylpropenoic acid", "condensed": "CH2=C(CH3)COOH", "category": "Mixed Functional Groups", "difficulty": "Hard"},

    # Carboxylic Acid + Haloalkane (Halo Acids)
    {"smiles": "ClCC(=O)O", "name": "chloroethanoic acid", "condensed": "ClCH2COOH", "category": "Mixed Functional Groups", "difficulty": "Medium"},
    {"smiles": "BrCCC(=O)O", "name": "3-bromopropanoic acid", "condensed": "BrCH2CH2COOH", "category": "Mixed Functional Groups", "difficulty": "Medium"},
    {"smiles": "CC(I)C(=O)O", "name": "2-iodopropanoic acid", "condensed": "CH3CH(I)COOH", "category": "Mixed Functional Groups", "difficulty": "Hard"}, # Added iodo
    {"smiles": "ClC(Cl)C(=O)O", "name": "2,2-dichloroethanoic acid", "condensed": "Cl2CHCOOH", "category": "Mixed Functional Groups", "difficulty": "Hard"},

    # More challenging combinations without primary ketones
    {"smiles": "ClC=CC(O)C", "name": "1-chlorobut-1-en-3-ol", "condensed": "ClCH=CHCH(OH)CH3", "category": "Mixed Functional Groups", "difficulty": "Hard"},
    {"smiles": "CC(Br)=CC(=O)O", "name": "3-bromobut-2-enoic acid", "condensed": "CH3C(Br)=CHCOOH", "category": "Mixed Functional Groups", "difficulty": "Hard"},
    {"smiles": "OCC(Cl)C=C", "name": "3-chlorobut-3-en-1-ol", "condensed": "HOCH2CH(Cl)C=CH2", "category": "Mixed Functional Groups", "difficulty": "Hard"},
    {"smiles": "CC(O)C(C)C(=O)O", "name": "2-hydroxy-3-methylbutanoic acid", "condensed": "CH3CH(OH)CH(CH3)COOH", "category": "Mixed Functional Groups", "difficulty": "Hard"},
    {"smiles": "C=C(Cl)C(C)(O)C", "name": "3-chloro-2-methylbut-3-en-2-ol", "condensed": "CH2=C(Cl)C(CH3)(OH)CH3", "category": "Mixed Functional Groups", "difficulty": "Hard"}, # Corrected from before
    {"smiles": "BrC(C)=CC(O)C", "name": "4-bromopent-3-en-2-ol", "condensed": "BrCH(CH3)C=CHCH(OH)CH3", "category": "Mixed Functional Groups", "difficulty": "Hard"},
    {"smiles": "CC(O)C=C(Br)C", "name": "4-bromopent-3-en-2-ol", "condensed": "CH3CH(OH)CH=C(Br)CH3", "category": "Mixed Functional Groups", "difficulty": "Hard"},

    # Additional Mixed Examples
    {"smiles": "CCC(O)C=C", "name": "pent-1-en-3-ol", "condensed": "CH3CH2CH(OH)CH=CH2", "category": "Mixed Functional Groups", "difficulty": "Medium"},
    {"smiles": "CC(Cl)C(O)CC", "name": "2-chloropentan-3-ol", "condensed": "CH3CH(Cl)CH(OH)CH2CH3", "category": "Mixed Functional Groups", "difficulty": "Hard"},
    {"smiles": "C=C(Br)CCC(=O)O", "name": "4-bromopent-4-enoic acid", "condensed": "CH2=C(Br)CH2CH2COOH", "category": "Mixed Functional Groups", "difficulty": "Hard"},
    {"smiles": "OCC=CCO", "name": "but-2-ene-1,4-diol", "condensed": "HOCH2CH=CHCH2OH", "category": "Mixed Functional Groups", "difficulty": "Hard"},
    {"smiles": "ClCC(Cl)CO", "name": "2,3-dichloropropan-1-ol", "condensed": "ClCH2CH(Cl)CH2OH", "category": "Mixed Functional Groups", "difficulty": "Hard"},
    {"smiles": "C=CC(Br)CO", "name": "2-bromobut-3-en-1-ol", "condensed": "CH2=CHCH(Br)CH2OH", "category": "Mixed Functional Groups", "difficulty": "Hard"},
    {"smiles": "CC(Cl)=CCC(=O)O", "name": "4-chloropent-3-enoic acid", "condensed": "CH3C(Cl)=CHCH2COOH", "category": "Mixed Functional Groups", "difficulty": "Hard"},
    {"smiles": "CC(I)C=C", "name": "3-iodobut-1-ene", "condensed": "CH3CH(I)CH=CH2", "category": "Mixed Functional Groups", "difficulty": "Hard"}, # Alkene double bond gets lower number if choice
    {"smiles": "O=C(O)C=CC(=O)O", "name": "butenedioic acid", "condensed": "HOOCCH=CHCOOH", "category": "Mixed Functional Groups", "difficulty": "Hard"},
]


# @title Validate structures (Adapted for Streamlit - console/optional UI output)
def validate_smiles_in_practice_problems(problems_list):
    invalid_smiles_entries = []
    validation_messages = ["--- Validating SMILES Strings ---"]

    if not problems_list:
        validation_messages.append("Practice problems list is empty.")
        return invalid_smiles_entries, validation_messages

    for i, problem in enumerate(problems_list):
        smiles = problem.get('smiles')
        name = problem.get('name', 'N/A')

        if not smiles:
            msg = f"Error: Entry {i+1} (Name: '{name}') has no SMILES string."
            validation_messages.append(msg)
            invalid_smiles_entries.append({**problem, "index": i+1, "error_type": "Missing SMILES"})
            continue

        mol = Chem.MolFromSmiles(smiles, sanitize=True)

        if mol is None:
            mol_no_sanitize = Chem.MolFromSmiles(smiles, sanitize=False)
            error_detail = "General parsing error."
            if mol_no_sanitize is None:
                error_detail = "SMILES syntax error (failed even without sanitization)."
            else:
                try:
                    Chem.SanitizeMol(mol_no_sanitize)
                except Exception as e:
                    error_detail = f"Sanitization error: {e}"
            
            msg = (f"Error: Invalid SMILES at Entry {i+1} (Name: '{name}')\n"
                   f"  SMILES: '{smiles}'\n"
                   f"  Detail: {error_detail}\n" + "-" * 20)
            validation_messages.append(msg)
            invalid_smiles_entries.append({**problem, "index": i+1, "error_type": error_detail, "original_smiles": smiles})
        elif mol.GetNumAtoms() == 0 and smiles.strip() != "":
            msg = (f"Warning: SMILES at Entry {i+1} (Name: '{name}') resulted in a molecule with 0 atoms.\n"
                   f"  SMILES: '{smiles}'\n" + "-" * 20)
            validation_messages.append(msg)

    if not invalid_smiles_entries:
        validation_messages.append("\nAll SMILES strings are valid!")
    else:
        validation_messages.append(f"\nFound {len(invalid_smiles_entries)} entries with SMILES errors.")

    validation_messages.append("--- Validation Complete ---")
    return invalid_smiles_entries, validation_messages

# --- Structure Generation Functions ---
@st.cache_data
def get_full_structure_image(mol_smiles):
    mol = Chem.MolFromSmiles(mol_smiles)
    if not mol: return None
    mol_with_hs = Chem.AddHs(mol)
    Compute2DCoords(mol_with_hs)
    for atom in mol_with_hs.GetAtoms():
        if atom.GetAtomicNum() == 6:
            atom.SetProp('atomLabel', 'C')
    draw_options = rdMolDraw2D.MolDrawOptions()
    draw_options.atomLabelFontSize = 15 
    draw_options.padding = 0.1
    draw_options.explicitCarbonLabels = True
    draw_options.addStereoAnnotation = True
    # Original size: (550, 450). st.image will scale this down if use_column_width is set.
    img = Draw.MolToImage(mol_with_hs, size=(550, 450), kekulize=True, options=draw_options)
    return img

@st.cache_data
def get_skeletal_structure_image(mol_smiles):
    mol = Chem.MolFromSmiles(mol_smiles)
    if not mol: return None
    Compute2DCoords(mol)
    img = Draw.MolToImage(mol, size=(350, 250))
    return img

def format_condensed_formula_html(condensed_str):
    processed_str = condensed_str.replace('#', '≡')
    formatted_with_subscripts = re.sub(r'([A-Za-z)])(\d+)', r'\1<sub>\2</sub>', processed_str)
    return f"<div style='font-size: 1.8em; font-weight: bold; margin-top: 10px; margin-bottom: 10px; font-family: Arial, sans-serif; text-align: center;'>{formatted_with_subscripts}</div>"

@st.cache_data
def generate_condensed_formula(mol_smiles):
    for p in practice_problems:
        if p['smiles'] == mol_smiles and 'condensed' in p and p['condensed']:
            return p['condensed']
    return f"Condensed formula not found for SMILES: {mol_smiles}"

# --- Session State Initialization ---
def initialize_session_state():
    defaults = {
        'app_stage': 'setup',
        'selected_categories': [], # CHANGED: Now a list for multiselect
        'selected_difficulties': [], # CHANGED: Now a list for multiselect
        'num_problems_requested': 5,
        'quiz_problems_list': [],
        'problem_index': 0,
        'total_problems_in_quiz': 0,
        'current_score': 0,
        'current_mol_smiles': None,
        'current_correct_name': "",
        'current_alternative_names': [],
        'student_answer': "",
        'is_current_problem_answered': False,
        'is_current_problem_correct': False,
        'feedback_message': "",
        'ai_explanation': "",
        'last_selected_formula_type': 'Skeletal',
        'disable_answer_input': False,
        'disable_formula_dropdown': False
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

initialize_session_state()

# --- AI Explanation Function ---
@st.cache_data(show_spinner="🤖 Asking AI for explanation...")
def get_ai_nomenclature_explanation_st(student_answer, correct_iupac_name, smiles_string):
    global genai_model, genai_service_available # Access the globally configured model
    if not genai_service_available or not genai_model:
        return "AI explanation service is not available."

    prompt = f"""
    You are an expert chemistry tutor evaluating the student's IUPAC nomenclature attempt for an organic compound.
    The student's answer is: "{student_answer}"
    The correct preferred IUPAC name is: "{correct_iupac_name}"

    Provide a step-by-step breakdown of how to name this compound correctly, and for each step, evaluate if the student's answer reflects understanding of that step.
    Give the general comment in the first sentence, then use the following format for each step:
    - "Step X: [Description of the nomenclature step, e.g., Identify the principal functional group and parent chain.] [If correct, (✅). If incorrect (❌)]"
    - "Comment: [If incorrect (❌), provide a concise, one-sentence explanation of what the student likely did wrong for THIS SPECIFIC STEP, relating it to their answer and the correct name. If correct (✅) , leave the comment blank"]"

    Consider these common nomenclature steps (adapt them as needed based on the complexity of the molecule from the SMILES string):
    1.  Identify the principal functional group.
    2.  Identify the longest continuous carbon chain.
    3.  Number the parent chain to give the principal functional group the lowest possible number.
    4.  Identify all substituents (alkyl groups, halogens, etc.) attached to the parent chain.
    5.  Name and number each substituent.
    6.  Assemble the name in the correct order:
    7.  Check for special cases like redundant number.

    Be very specific in your comments, referring to parts of the student's answer and the correct name.
    For example, if student said "2-methylpentan-4-ol" and correct is "4-methylpentan-2-ol", for Step 3 (Numbering) you would say:
    "Step 3: Number the parent chain to give the hydroxyl group (-OH) the lowest number. ❌"
    "Comment: It seems you numbered from the end that gave the methyl group a lower number, but the -OH group should have priority for the lowest number (position 2, not 4)."

    Address the student as "you"

    If the student's answer is "{student_answer}" and the correct answer is "{correct_iupac_name}":
    """
    try:
        response = genai_model.models.generate_content(contents=prompt,model=gemini_model_name)
        explanation = response.text
        return extract_error_steps_and_comments(explanation)
    except Exception as e:
        st.error(f"Error calling Gemini API: {e}")
        return f"Error calling Gemini API: {e}"

def extract_error_steps_and_comments(text_block):
    lines = text_block.strip().split('\n')
    result_lines = []
    last_step_was_error = False

    for line in lines:
        cleaned_line_for_processing = line.strip()
        processed_line_content = re.sub(r'^[*-]\s*', '', cleaned_line_for_processing)

        if processed_line_content.startswith("Step ") and processed_line_content.endswith("❌"):
            result_lines.append(processed_line_content)
            last_step_was_error = True
        elif processed_line_content.startswith("Step "): # Reset if it's a step but not an error
            last_step_was_error = False
        elif processed_line_content.startswith("Comment:") and last_step_was_error:
            result_lines.append(processed_line_content)
            # Optional: Reset last_step_was_error here if a comment should only follow one error step
            # last_step_was_error = False 

    if not result_lines:
        return "" 
    
    html_list_items = [f"<li>{res_line.replace('❌', '❌ (Incorrect)').replace('✅', '✅ (Correct)')}</li>" for res_line in result_lines]
    return f"<ul>{''.join(html_list_items)}</ul>"

# --- Streamlit UI Functions ---

def display_structure_st(view_type_str, smiles_str, structure_placeholder):
    with structure_placeholder:
        if not smiles_str:
            # structure_placeholder.warning("No molecule SMILES string available to display.") # Removed to avoid clearing useful warnings
            st.warning("No molecule SMILES string available to display in placeholder.")
            return

        if view_type_str == "Skeletal":
            pil_image = get_skeletal_structure_image(smiles_str)
            if pil_image:
                st.image(pil_image, caption="Skeletal Structure", use_column_width='auto')
            else:
                st.error("Could not generate skeletal structure.")
        elif view_type_str == "Full":
            pil_image = get_full_structure_image(smiles_str)
            if pil_image:
                st.image(pil_image, caption="Full Structure", use_column_width='auto')
            else:
                st.error("Could not generate full structure.")
        elif view_type_str == "Condensed":
            condensed_formula_raw = generate_condensed_formula(smiles_str)
            if "not found" in condensed_formula_raw.lower(): # Make check case-insensitive
                 st.warning(condensed_formula_raw)
            else:
                formatted_html_string = format_condensed_formula_html(condensed_formula_raw)
                # Responsive div for condensed formula
                st.markdown(
                    f"""
                    <div style="
                        width: 100%; 
                        max-width: 350px; /* Max desirable width */
                        min-height: 200px; /* Minimum height to ensure visibility */
                        height: auto;    /* Let content define height */
                        display: flex; 
                        justify-content: center; 
                        align-items: center; 
                        border: 1px solid #eee; 
                        margin-left: auto; /* Center the box if col is wider than max-width */
                        margin-right: auto;
                        background-color: #fff;
                        padding: 10px; /* Add some padding inside the box */
                        box-sizing: border-box; /* Ensure padding is included in width/height */
                    ">
                        {formatted_html_string}
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
        else:
            st.error("Unknown view type selected.")

def handle_answer_submission_st():
    if st.session_state.is_current_problem_answered:
        return

    student_answer = st.session_state.student_answer
    correct_name = st.session_state.current_correct_name
    alternative_names = st.session_state.current_alternative_names

    processed_student_answer = student_answer.lower().strip().replace(" ", "").replace("-", "")
    processed_correct_name = correct_name.lower().strip().replace(" ", "").replace("-", "")
    processed_alt_names = [alt.lower().strip().replace(" ", "").replace("-", "") for alt in alternative_names]

    is_correct = (processed_student_answer == processed_correct_name or
                  processed_student_answer in processed_alt_names)
    
    st.session_state.is_current_problem_answered = True
    st.session_state.disable_answer_input = True
    st.session_state.disable_formula_dropdown = True

    if is_correct:
        st.session_state.is_current_problem_correct = True
        st.session_state.current_score += 1
        st.session_state.feedback_message = f"<p style='color:green; font-weight:bold; font-size:1.1em;'>Correct! The name is {correct_name}.</p>"
        st.balloons()
    else:
        st.session_state.is_current_problem_correct = False
        feedback_parts = [
            f"<p style='color:red; font-weight:bold; font-size:1.1em;'>Incorrect.</p>",
            f"Your answer: <code>{student_answer}</code>",
            f"Correct answer(s): <strong><code>{correct_name}</code></strong>" +
            (f" or <strong><code>{', '.join(alternative_names)}</code></strong>" if alternative_names else "")
        ]
        
        custom_explanation_found = False
        problem_spec = st.session_state.quiz_problems_list[st.session_state.problem_index]
        if 'common_errors' in problem_spec:
            for error_entry in problem_spec['common_errors']:
                processed_incorrect_name = error_entry['incorrect_name'].lower().strip().replace(" ", "").replace("-", "")
                if processed_student_answer == processed_incorrect_name:
                    feedback_parts.append(f"<hr><b>Explanation for your answer:</b><br>{error_entry['explanation']}")
                    custom_explanation_found = True
                    break
        
        st.session_state.feedback_message = "<br>".join(feedback_parts)
        
        if not custom_explanation_found and genai_service_available:
            st.session_state.ai_explanation = get_ai_nomenclature_explanation_st(
                student_answer, correct_name, st.session_state.current_mol_smiles
            )
        else:
            st.session_state.ai_explanation = ""

def go_to_next_problem_callback(): # Changed name for clarity
    st.session_state.problem_index += 1
    
    # Reset states for the new problem
    st.session_state.student_answer = ""  # THIS IS THE KEY CHANGE for the error
    st.session_state.is_current_problem_answered = False
    st.session_state.is_current_problem_correct = False
    st.session_state.feedback_message = ""
    st.session_state.ai_explanation = ""
    st.session_state.disable_answer_input = False
    st.session_state.disable_formula_dropdown = False

    if st.session_state.problem_index >= st.session_state.total_problems_in_quiz:
        st.session_state.app_stage = 'results'
    else:
        # If still in quiz, load the next problem's details.
        # This prepares the state for the upcoming re-render.
        load_current_problem_details()

def setup_new_quiz_st():
    filtered_problems = list(practice_problems) # Start with a copy
    
    # --- UPDATED FILTERING LOGIC ---
    selected_cats = st.session_state.get('selected_categories', [])
    selected_diffs = st.session_state.get('selected_difficulties', [])

    if selected_cats: # If the list is not empty, apply category filter
        filtered_problems = [p for p in filtered_problems if p.get('category') in selected_cats]
    
    if selected_diffs: # If the list is not empty, apply difficulty filter
        filtered_problems = [p for p in filtered_problems if p.get('difficulty') in selected_diffs]

    if not filtered_problems:
        st.warning(f"No problems found for the selected criteria. Trying to use problems from all available.")
        # If no problems match the multi-selection, you could either:
        # 1. Fallback to all problems (current behavior if initial lists were empty)
        # 2. Or, more strictly, show an error that no problems match.
        # For now, let's be explicit: if filtering results in empty, and original selections were made, it's a "no match"
        if selected_cats or selected_diffs: # If any specific filter was actually applied
            st.error("No problems match your specific combination of categories and difficulties. Please broaden your selection.")
            # st.session_state.app_stage = 'setup' # Keep on setup page
            return # Stop quiz setup
        else: # This case means both selected_cats and selected_diffs were empty (i.e., "Any")
            filtered_problems = list(practice_problems) # Fallback to all problems if initial selections were empty
    
    if not filtered_problems: # Should be caught above, but as a safeguard
        st.error("No practice problems available at all. Cannot start quiz.")
        # st.session_state.app_stage = 'setup' # Keep on setup page
        return

    num_req = st.session_state.num_problems_requested
    actual_num_problems = min(num_req, len(filtered_problems))
    
    if actual_num_problems == 0:
        st.error("Not enough problems available to run the quiz with the selected criteria after filtering.")
        # st.session_state.app_stage = 'setup' # Keep on setup page
        return

    st.session_state.quiz_problems_list = random.sample(filtered_problems, k=actual_num_problems)
    st.session_state.total_problems_in_quiz = actual_num_problems
    st.session_state.problem_index = 0
    st.session_state.current_score = 0
    st.session_state.app_stage = 'quiz' # Move to quiz stage
    
    # Reset other per-problem states explicitly for the first problem
    st.session_state.student_answer = ""
    st.session_state.is_current_problem_answered = False
    st.session_state.is_current_problem_correct = False
    st.session_state.feedback_message = ""
    st.session_state.ai_explanation = ""
    st.session_state.disable_answer_input = False
    st.session_state.disable_formula_dropdown = False
    
    load_current_problem_details() # Load first problem details

def load_current_problem_details():
    if 'problem_index' not in st.session_state or 'quiz_problems_list' not in st.session_state:
        st.error("Quiz state not properly initialized. Cannot load problem details.")
        st.session_state.app_stage = 'setup' # Force back to setup
        return

    if st.session_state.problem_index < st.session_state.total_problems_in_quiz:
        problem_spec = st.session_state.quiz_problems_list[st.session_state.problem_index]
        st.session_state.current_mol_smiles = problem_spec['smiles']
        st.session_state.current_correct_name = problem_spec['name']
        
        alt_names = problem_spec.get('alternative_names', [])
        st.session_state.current_alternative_names = [alt_names] if isinstance(alt_names, str) else alt_names
        
        mol = Chem.MolFromSmiles(st.session_state.current_mol_smiles)
        if not mol:
            st.error(f"Error loading SMILES: {st.session_state.current_mol_smiles} for problem {st.session_state.problem_index + 1}. This problem will be skipped.")
            # Mark problem as "answered" to enable Next button and prevent interaction
            st.session_state.is_current_problem_answered = True
            st.session_state.disable_answer_input = True
            st.session_state.disable_formula_dropdown = True
            st.session_state.feedback_message = "<p style='color:orange; font-weight:bold;'>Problem Loading Error: This problem could not be loaded and will be skipped. Please click 'Next Problem'.</p>"
            st.session_state.current_mol_smiles = None # Ensure it's None so display_structure shows nothing or error
            return # Exit, the UI will reflect this error state
    else:
        st.session_state.current_mol_smiles = None # No current problem if index is out of bounds

# --- Main App Display Logic ---

def display_setup_page_st():
    st.header("🧪 Organic Chemistry Nomenclature Practice Setup")
    st.markdown("---")

    # Get unique categories and difficulties, maintaining original order of appearance
    seen_categories_set = set()
    # REMOVED "Any Category" from options, as empty multiselect implies "Any"
    ordered_categories_options = [
        p['category'] for p in practice_problems 
        if p.get('category') and p['category'] not in seen_categories_set 
        and not seen_categories_set.add(p['category'])
    ]
    
    seen_difficulties_set = set()
    # REMOVED "Any Difficulty" from options
    ordered_difficulties_options = [
        p['difficulty'] for p in practice_problems 
        if p.get('difficulty') and p['difficulty'] not in seen_difficulties_set 
        and not seen_difficulties_set.add(p['difficulty'])
    ]
    
    max_possible_problems = len(practice_problems)

    cols_setup = st.columns([2,2,1])
    with cols_setup[0]:
      st.multiselect( # CHANGED to st.multiselect
          "Select Categories (leave blank for Any):", 
          options=ordered_categories_options, 
          key="selected_categories" # Key matches session state
      )
    with cols_setup[1]:
      st.multiselect( # CHANGED to st.multiselect
          "Select Difficulties (leave blank for Any):", 
          options=ordered_difficulties_options, 
          key="selected_difficulties" # Key matches session state
      )
    with cols_setup[2]:
      st.number_input(
          "Number of Problems:", 
          min_value=1, 
          max_value=max_possible_problems, 
          key="num_problems_requested", 
          step=1
      )

    if st.button("🚀 Start Practice", type="primary", use_container_width=True):
        setup_new_quiz_st()
        # Only rerun if app_stage actually changed to 'quiz'.
        # If setup_new_quiz_st returned early due to errors, we don't want to rerun into quiz.
        if st.session_state.app_stage == 'quiz':
            st.rerun()
        # If setup_new_quiz_st encounters an error, it will display st.error()
        # and the user will remain on the setup page to adjust their selections.

    # ... (rest of the setup page, like expander, remains the same) ...
    st.markdown("---")
    with st.expander("ℹ️ About this App & SMILES Validation"):
        st.markdown("""
        This app helps you practice IUPAC nomenclature for organic compounds.
        - Select categories, difficulties (or leave blank for all), and number of problems.
        - View structures as Skeletal, Full, or Condensed formulas.
        - Submit your answer and get feedback.
        - AI-powered explanations (using Google's Gemini) are provided for incorrect answers if available.
        """)
        if st.checkbox("Run SMILES Validation on Question Bank (for developers/debugging)"):
            invalid_entries, validation_log_messages = validate_smiles_in_practice_problems(practice_problems)
            st.text_area("SMILES Validation Log:", "\n".join(validation_log_messages), height=200, key="smiles_val_log")
            if invalid_entries:
                st.error(f"{len(invalid_entries)} invalid SMILES entries found. Details in log above.")
                
def display_quiz_page_st():
    st.header("🧠 IUPAC Nomenclature Practice")
    
    # Ensure problem details are loaded if somehow missed (e.g., after a direct URL visit to quiz page)
    if not st.session_state.current_mol_smiles and \
       st.session_state.problem_index < st.session_state.total_problems_in_quiz and \
       st.session_state.quiz_problems_list: # Check if list exists
        load_current_problem_details()

    progress_val = (st.session_state.problem_index) / st.session_state.total_problems_in_quiz if st.session_state.total_problems_in_quiz > 0 else 0
    st.progress(progress_val, text=f"Problem {st.session_state.problem_index + 1} of {st.session_state.total_problems_in_quiz} (Score: {st.session_state.current_score})")
    st.markdown("---")

    # Graceful handling if problem loading failed
    if not st.session_state.current_mol_smiles and \
       st.session_state.problem_index < st.session_state.total_problems_in_quiz:
        # Feedback message should already be set by load_current_problem_details if it failed
        if st.session_state.feedback_message:
             st.markdown(st.session_state.feedback_message, unsafe_allow_html=True)
        else: # Generic message if feedback was not set
             st.error("The current problem could not be loaded. Please click 'Next Problem'.")
        # Still need to show the "Next Problem" button
        st.session_state.is_current_problem_answered = True # Enable next button

    col1, col2 = st.columns([2, 3])

    with col1:
        st.markdown("#### Structure to Name:")
        st.selectbox(
            "Select Formula View:",
            options=['Skeletal', 'Full', 'Condensed'],
            key='last_selected_formula_type',
            disabled=st.session_state.disable_formula_dropdown or not st.session_state.current_mol_smiles
        )
        
        structure_placeholder_col1 = st.empty()
        if st.session_state.current_mol_smiles:
             display_structure_st(st.session_state.last_selected_formula_type, st.session_state.current_mol_smiles, structure_placeholder_col1)
        elif st.session_state.problem_index < st.session_state.total_problems_in_quiz: # If problem should exist but SMILES is None
             structure_placeholder_col1.warning("Structure cannot be displayed for this problem.")
        # else: quiz is over or not started

    with col2:
        st.markdown("#### Your Answer:")
        
        with st.form(key="answer_form"):
            st.text_input(
                "Enter IUPAC Name:", 
                key='student_answer', # Widget linked to st.session_state.student_answer
                disabled=st.session_state.disable_answer_input or not st.session_state.current_mol_smiles
            )
            
            form_submitted = st.form_submit_button(
                label="✔️ Submit Answer", 
                disabled=st.session_state.is_current_problem_answered or not st.session_state.current_mol_smiles,
                use_container_width=True
            )

            if form_submitted:
                handle_answer_submission_st() # This function modifies session state for feedback
                st.rerun() # Rerun to show feedback and updated button states

        next_button_text = "➡️ Next Problem"
        if st.session_state.problem_index + 1 >= st.session_state.total_problems_in_quiz:
            next_button_text = "🏁 Finish Practice"
        
        # --- THIS IS THE CRITICAL CHANGE ---
        st.button(
            next_button_text, 
            key="next_problem_btn", 
            disabled=not st.session_state.is_current_problem_answered, 
            use_container_width=True, 
            type="primary",
            on_click=go_to_next_problem_callback # Use the on_click callback here
        )
        # The st.rerun() after this button is now implicit after the on_click callback executes.
        # No need to call load_current_problem_details() or st.rerun() explicitly after this button.

        st.markdown("---")
        if st.session_state.feedback_message:
            st.markdown("#### Feedback:")
            st.markdown(st.session_state.feedback_message, unsafe_allow_html=True)
            if st.session_state.ai_explanation:
                with st.expander("💡 AI Explanation (Beta)", expanded=not st.session_state.is_current_problem_correct):
                    st.markdown(st.session_state.ai_explanation, unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("New Practice Setup / Quit Current Practice", key="quit_quiz_btn"):
        # Reset relevant session state for a clean start
        keys_to_clear_for_new_quiz = [
            
            'quiz_problems_list', 'problem_index', 'total_problems_in_quiz', 
            'current_score', 'current_mol_smiles', 'current_correct_name', 
            'current_alternative_names', 'student_answer', 'is_current_problem_answered',
            'is_current_problem_correct', 'feedback_message', 'ai_explanation',
            'disable_answer_input', 'disable_formula_dropdown'
        ]
        for key in keys_to_clear_for_new_quiz:
            if key in st.session_state:
                # Use pop for safer removal, providing a default if key somehow missing
                st.session_state.pop(key, None) 
        
        st.session_state.app_stage = 'setup'
        initialize_session_state() # Re-apply defaults for cleared items
        st.rerun()

def display_results_page_st():
    st.header("🏆 Quiz Over!")
    st.balloons()
    st.markdown("---")
    st.subheader(f"Your final score is: {st.session_state.current_score} out of {st.session_state.total_problems_in_quiz}")
    
    percentage = (st.session_state.current_score / st.session_state.total_problems_in_quiz) * 100 if st.session_state.total_problems_in_quiz > 0 else 0
    st.metric(label="Percentage", value=f"{percentage:.2f}%")

    if percentage == 100:
        st.success("🎉 Excellent! Perfect Score! 🎉")
    elif percentage >= 75:
        st.info("👍 Great job!")
    elif percentage >= 50:
        st.warning("🙂 Good effort, keep practicing!")
    else:
        st.error("😓 Needs more practice. Don't give up!")

    st.markdown("---")
    if st.button("🔄 Start a New Quiz", type="primary", use_container_width=True):
        # Similar reset as "Quit Quiz" to ensure clean state for new setup
        keys_to_clear_for_restart = [
            'quiz_problems_list', 'problem_index', 'total_problems_in_quiz', 
            'current_score', 'current_mol_smiles', 'current_correct_name', 
            'current_alternative_names', 'student_answer', 'is_current_problem_answered',
            'is_current_problem_correct', 'feedback_message', 'ai_explanation',
            'disable_answer_input', 'disable_formula_dropdown'
        ]
        for key in keys_to_clear_for_restart:
            if key in st.session_state:
                del st.session_state[key]
        
        st.session_state.app_stage = 'setup'
        initialize_session_state() # Re-initialize
        st.rerun()

# --- App Router ---
if __name__ == "__main__":
    
    if 'app_stage' not in st.session_state:
        initialize_session_state()

    if st.session_state.app_stage == 'setup':
        display_setup_page_st()
    elif st.session_state.app_stage == 'quiz':
        if not st.session_state.get('quiz_problems_list') or st.session_state.get('total_problems_in_quiz', 0) == 0:
            st.warning("Quiz not properly initialized. Returning to setup.")
            st.session_state.app_stage = 'setup' 
            initialize_session_state() 
            st.rerun()
        else:
            display_quiz_page_st()
    elif st.session_state.app_stage == 'results':
        display_results_page_st()
    else: 
        st.error("Invalid application stage. Resetting to setup.")
        st.session_state.app_stage = 'setup'
        initialize_session_state()
        st.rerun()