# Step 1: Import necessary libraries
import streamlit as st
import base64 
from io import BytesIO 
import random
import re
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem.AllChem import Compute2DCoords
from rdkit.Chem.Draw import rdMolDraw2D

# Import the practice problems from our new separate file
from problems import practice_problems

# For Google GenAI
from google import genai

# --- Configuration & Initialization ---
st.set_page_config(page_title="Chemistry Quiz", layout="wide", initial_sidebar_state="collapsed")

try:
    api_key_to_use = st.secrets.get("GENAI_API_KEY")
    gemini_model_name = st.secrets.get("GENAI_MODEL_NAME", "gemini-2.0-flash")

    if not api_key_to_use:
        api_key_to_use = "" # YOUR PROVIDED KEY
        st.warning(
            "⚠️ Using a hardcoded API key from the original script. "
            "For security and best practice, please set `GENAI_API_KEY` in Streamlit Secrets. "
            "The current key may be exposed or invalid."
        )
    
    genai_model = genai.Client(api_key=api_key_to_use)
    genai_service_available = True
except Exception as e:
    st.error(f"🚨 Failed to initialize Google GenAI service: {e}. \n"
             f"AI features may not work. Ensure API key is valid and model name ('{gemini_model_name}') is correct. \n"
             "You can set `GENAI_API_KEY` and optionally `GENAI_MODEL_NAME` in Streamlit Secrets.")
    genai_model = None
    genai_service_available = False


# --- Category Definitions & Format Function ---
S4_CATEGORIES = [
    "Straight-chain Alkane", "Branched Alkane", "Alkene", 
    "Haloalkane", "Alkanol", "Carboxylic Acid", "Mixed Functional Groups"
]

S5_CATEGORIES = ["Ketone", "Aldehyde", "Primary Amine", "Unsubstituted Amide", "Ester"]

ALL_CATEGORIES = S4_CATEGORIES + S5_CATEGORIES

def format_category_label(category):
    if category in S4_CATEGORIES:
        return f"🟢 {category} (S4)"
    elif category in S5_CATEGORIES:
        return f"🟣 {category} (S5)"
    return category

# Hardcode the options directly so Streamlit has to render the emojis
FORMATTED_ALL_CATEGORIES = [format_category_label(c) for c in ALL_CATEGORIES]
# Create a dictionary to map the formatted strings back to raw category names
REVERSE_CATEGORY_MAP = {format_category_label(c): c for c in ALL_CATEGORIES}

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

    try:
        draw_options = rdMolDraw2D.MolDrawOptions()
        draw_options.atomLabelFontSize = 15        
        draw_options.bondLineWidth = 1.5
        draw_options.padding = 0.1                 
        draw_options.explicitCarbonLabels = True   
        draw_options.addStereoAnnotation = True    
        draw_options.includeAtomNumbers = False    
        draw_options.fixedBondLength = 40          
        draw_options.legendFontSize = 15           
    except AttributeError as e:
        st.error(f"RDKit Draw Options Error: {e}. Check attribute names for your RDKit version.")
        draw_options = rdMolDraw2D.MolDrawOptions()

    for atom in mol_with_hs.GetAtoms():
        if atom.GetAtomicNum() == 6: 
            atom.SetProp('atomLabel', 'C') 

    img = Draw.MolToImage(
        mol_with_hs, 
        size=(550, 450), 
        kekulize=True, 
        options=draw_options 
    )
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
        'selected_categories_formatted': [], # Updated to match new explicit text options
        'selected_difficulties': [], 
        'num_problems_requested': 5,
        'quiz_problems_list': [],
        'problem_index': 0,
        'total_problems_in_quiz': 0,
        'current_score': 0,
        'current_mol_smiles': None,
        'current_correct_name': "",
        'current_alternative_names': [],
        'student_answer': "", 
        'submitted_student_answer_for_feedback': "", 
        'is_current_problem_answered': False, 
        'answer_submitted_and_locked': False, 
        'is_current_problem_correct': False,
        'feedback_message': "",
        'ai_explanation': "",
        'last_selected_formula_type': 'Skeletal',
        'disable_formula_dropdown': False
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

initialize_session_state()

# --- AI Explanation Function ---
@st.cache_data(show_spinner="🤖 Asking AI for explanation...")
def get_ai_nomenclature_explanation_st(student_answer, correct_iupac_name, smiles_string):
    global genai_model, genai_service_available 
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
        elif processed_line_content.startswith("Step "): 
            last_step_was_error = False
        elif processed_line_content.startswith("Comment:") and last_step_was_error:
            result_lines.append(processed_line_content)

    if not result_lines:
        return "" 
    
    html_list_items = [f"<li>{res_line.replace('❌', '❌').replace('✅', '✅')}</li>" for res_line in result_lines]
    return f"<ul>{''.join(html_list_items)}</ul>"

# --- Streamlit UI Functions ---
def display_structure_st(view_type_str, smiles_str, structure_placeholder):
    with structure_placeholder:
        if not smiles_str:
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
            if "not found" in condensed_formula_raw.lower(): 
                 st.warning(condensed_formula_raw)
            else:
                formatted_html_string = format_condensed_formula_html(condensed_formula_raw)
                st.markdown(
                    f"""
                    <div style="
                        width: 100%; 
                        max-width: 350px; 
                        min-height: 200px; 
                        height: auto;    
                        display: flex; 
                        justify-content: center; 
                        align-items: center; 
                        border: 1px solid #eee; 
                        margin-left: auto; 
                        margin-right: auto;
                        background-color: #fff;
                        padding: 10px; 
                        box-sizing: border-box; 
                    ">
                        {formatted_html_string}
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
        else:
            st.error("Unknown view type selected.")

def handle_answer_submission_callback():
    if st.session_state.answer_submitted_and_locked:
        go_to_next_problem_callback()
    else:
        st.session_state.is_current_problem_answered = True
        st.session_state.submitted_student_answer_for_feedback = st.session_state.student_answer
        current_submission = st.session_state.student_answer 

        correct_name = st.session_state.current_correct_name
        alternative_names = st.session_state.get('current_alternative_names', [])

        processed_student_answer = current_submission.lower().strip().replace(" ", "").replace("-", "")
        processed_correct_name = correct_name.lower().strip().replace(" ", "").replace("-", "")
        processed_alt_names = [
            alt.lower().strip().replace(" ", "").replace("-", "")
            for alt in alternative_names if isinstance(alt, str)
        ]

        is_correct = (processed_student_answer == processed_correct_name or
                      processed_student_answer in processed_alt_names)

        st.session_state.answer_submitted_and_locked = True 
        st.session_state.disable_formula_dropdown = True

        if is_correct:
            st.session_state.is_current_problem_correct = True
            st.session_state.current_score += 1
            st.session_state.feedback_message = f"<p style='color:green; font-weight:bold; font-size:1.1em;'>Correct! The preferred name is {correct_name}.</p>"
            if processed_student_answer != processed_correct_name and alternative_names:
                st.session_state.feedback_message += f"<p style='font-size:0.9em;'>Your answer, '{current_submission}', is also an accepted name.</p>"
        else:
            st.session_state.is_current_problem_correct = False
            feedback_parts = [
                f"<p style='color:red; font-weight:bold; font-size:1.1em;'>Incorrect.</p>",
                f"Your answer: <code>{current_submission}</code>", 
                f"The preferred IUPAC name is: <code>{correct_name}</code>"
            ]
            if alternative_names:
                 feedback_parts.append(f"Other accepted name(s) include: <code>{', '.join(alternative_names)}</code>")
            feedback_parts.append(f"<p></p>")
            
            custom_explanation_found = False
            if 'quiz_problems_list' in st.session_state and \
               st.session_state.problem_index < len(st.session_state.quiz_problems_list):
                problem_spec = st.session_state.quiz_problems_list[st.session_state.problem_index]
                if 'common_errors' in problem_spec:
                    for error_entry in problem_spec['common_errors']:
                        if isinstance(error_entry.get('incorrect_name'), str):
                            processed_incorrect_name = error_entry['incorrect_name'].lower().strip().replace(" ", "").replace("-", "")
                            if processed_student_answer == processed_incorrect_name: 
                                feedback_parts.append(f"<hr><b>Explanation for your answer:</b><br>{error_entry['explanation']}")
                                custom_explanation_found = True
                                break
            st.session_state.feedback_message = "<br>".join(feedback_parts)
            
            if not custom_explanation_found and genai_service_available:
                st.session_state.ai_explanation = get_ai_nomenclature_explanation_st(
                    current_submission, correct_name, st.session_state.current_mol_smiles
                )
            else:
                st.session_state.ai_explanation = ""
    
def go_to_next_problem_callback():
    st.session_state.problem_index += 1
    
    st.session_state.student_answer = "" 
    st.session_state.submitted_student_answer_for_feedback = "" 
    st.session_state.is_current_problem_answered = False
    st.session_state.answer_submitted_and_locked = False 
    st.session_state.is_current_problem_correct = False
    st.session_state.feedback_message = ""
    st.session_state.ai_explanation = ""
    st.session_state.disable_formula_dropdown = False

    if st.session_state.problem_index >= st.session_state.total_problems_in_quiz:
        st.session_state.app_stage = 'results'
    else:
        load_current_problem_details()

def setup_new_quiz_st():
    filtered_problems = list(practice_problems) 
    
    selected_cats_formatted = st.session_state.get('selected_categories_formatted', [])
    # Map the formatted names back to their original names for filtering
    selected_cats = [REVERSE_CATEGORY_MAP[c] for c in selected_cats_formatted]
    selected_diffs = st.session_state.get('selected_difficulties', [])

    if selected_cats: 
        filtered_problems = [p for p in filtered_problems if p.get('category') in selected_cats]
    
    if selected_diffs: 
        filtered_problems = [p for p in filtered_problems if p.get('difficulty') in selected_diffs]

    if not filtered_problems:
        st.warning(f"No problems found for the selected criteria. Trying to use problems from all available.")
        if selected_cats or selected_diffs: 
            st.error("No problems match your specific combination of categories and difficulties. Please broaden your selection.")
            return 
        else: 
            filtered_problems = list(practice_problems) 
    
    if not filtered_problems: 
        st.error("No practice problems available at all. Cannot start quiz.")
        return

    num_req = st.session_state.num_problems_requested
    actual_num_problems = min(num_req, len(filtered_problems))
    
    if actual_num_problems == 0:
        st.error("Not enough problems available to run the quiz with the selected criteria after filtering.")
        return

    st.session_state.quiz_problems_list = random.sample(filtered_problems, k=actual_num_problems)
    st.session_state.total_problems_in_quiz = actual_num_problems
    st.session_state.problem_index = 0
    st.session_state.current_score = 0
    st.session_state.app_stage = 'quiz' 
    
    st.session_state.student_answer = ""
    st.session_state.is_current_problem_answered = False
    st.session_state.is_current_problem_correct = False
    st.session_state.feedback_message = ""
    st.session_state.ai_explanation = ""
    st.session_state.disable_answer_input = False
    st.session_state.disable_formula_dropdown = False
    
    load_current_problem_details() 

def load_current_problem_details():
    if 'problem_index' not in st.session_state or 'quiz_problems_list' not in st.session_state:
        st.error("Quiz state not properly initialized. Cannot load problem details.")
        st.session_state.app_stage = 'setup' 
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
            st.session_state.is_current_problem_answered = True
            st.session_state.disable_answer_input = True
            st.session_state.disable_formula_dropdown = True
            st.session_state.feedback_message = "<p style='color:orange; font-weight:bold;'>Problem Loading Error: This problem could not be loaded and will be skipped. Please click 'Next Problem'.</p>"
            st.session_state.current_mol_smiles = None 
            return 
    else:
        st.session_state.current_mol_smiles = None 

# --- Main App Display Logic ---
def display_setup_page_st():
    st.header("🧪 Organic Chemistry Nomenclature Practice Setup")
    st.markdown("---")

    max_possible_problems = max(len(practice_problems), 1)

    cols_setup = st.columns([2,2,1])
    with cols_setup[0]:
      st.multiselect( 
          "Select Categories (leave blank for Any):", 
          options=FORMATTED_ALL_CATEGORIES, # Directly use formatted labels
          key="selected_categories_formatted" 
      )
    with cols_setup[1]:
      st.multiselect( 
          "Select Difficulties (leave blank for Any):", 
          options=["Easy", "Medium", "Hard"], 
          key="selected_difficulties" 
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
        if st.session_state.app_stage == 'quiz':
            st.rerun()

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
    st.header("🧠 IUPAC Nomenclature Quiz")

    with st.expander("📝 Nomenclature Steps (Click to view)", expanded=False):
        st.markdown("""
        1. Identify the principal functional group.
        2. Identify the longest continuous carbon chain.
        3. Number the parent chain to give the principal functional group the lowest possible number.
        4. Identify all substituents (alkyl groups, halogens, etc.) attached to the parent chain.
        5. Name and number each substituent.
        6. Assemble the name in the correct order.
        7. Check for special cases like redundant number.
        """)

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
        elif st.session_state.problem_index < st.session_state.total_problems_in_quiz:
             structure_placeholder_col1.warning("Structure cannot be displayed for this problem.")


    with col2: 
        st.markdown("#### Your Answer:")
                
        with st.form(key="answer_form"):
            st.text_input(
                "Enter IUPAC Name:", 
                key='student_answer', 
                disabled=not st.session_state.current_mol_smiles,
            )
            
            submit_button_label = "✔️ Submit Answer"
            if st.session_state.answer_submitted_and_locked:
                if st.session_state.problem_index + 1 >= st.session_state.total_problems_in_quiz:
                    submit_button_label = "🏁 Finish Quiz (Press Enter or Click)"
                else:
                    submit_button_label = "➡️ Next Problem (Press Enter or Click)"

            st.form_submit_button(
                label=submit_button_label, 
                use_container_width=True,
                on_click=handle_answer_submission_callback
            )
            
        if st.session_state.feedback_message:
            st.markdown("#### Feedback:")
            st.markdown(st.session_state.feedback_message, unsafe_allow_html=True)
            if st.session_state.ai_explanation:
                with st.expander("💡 AI Explanation (Beta)", expanded=not st.session_state.is_current_problem_correct):
                    st.markdown(st.session_state.ai_explanation, unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("New Quiz Setup / Quit Current Quiz", key="quit_quiz_btn_main"): 
        keys_to_clear_for_new_quiz = [
            'quiz_problems_list', 'problem_index', 'total_problems_in_quiz', 
            'current_score', 'current_mol_smiles', 'current_correct_name', 
            'current_alternative_names', 'student_answer', 'is_current_problem_answered',
            'answer_submitted_and_locked', 
            'is_current_problem_correct', 'feedback_message', 'ai_explanation',
            'disable_formula_dropdown', 'selected_categories_formatted'
        ]
        for key in keys_to_clear_for_new_quiz:
            st.session_state.pop(key, None) 
        
        st.session_state.app_stage = 'setup'
        initialize_session_state()
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
        keys_to_clear_for_restart = [
            'quiz_problems_list', 'problem_index', 'total_problems_in_quiz', 
            'current_score', 'current_mol_smiles', 'current_correct_name', 
            'current_alternative_names', 'student_answer', 'is_current_problem_answered',
            'is_current_problem_correct', 'feedback_message', 'ai_explanation',
            'disable_answer_input', 'disable_formula_dropdown', 'selected_categories_formatted'
        ]
        for key in keys_to_clear_for_restart:
            if key in st.session_state:
                del st.session_state[key]
        
        st.session_state.app_stage = 'setup'
        initialize_session_state() 
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