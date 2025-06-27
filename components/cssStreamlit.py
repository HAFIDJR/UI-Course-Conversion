import streamlit as st
def css() :
    
    st.markdown(
    """
    <style>
        /* General styling */
        body {
            background-color: #f0f7f4;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .main-container {
            background-color: #ffffff;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 100, 0, 0.08);
            margin: 1rem;
            max-width: 1200px;
            margin-left: auto;
            margin-right: auto;
            min-height: 400px;
        }
        h1 {
            color: #2e7d32;
            font-size: 2.2rem;
            margin-bottom: 1rem;
            text-align: center;
        }
        h2, h3 {
            color: #2e7d32;
            font-size: 1.5rem;
        }
        p {
            color: #4a4a4a;
            font-size: 1.1rem;
        }

        /* Input section styling */
        .input-section {
            background-color: #f9fcf9;
            padding: 1.5rem;
            border-radius: 10px;
            border: 2px solid #c8e6c9;
            margin: 1.5rem 0;
        }

        /* Radio button styling */
        .stRadio > label {
            color: #2e7d32;
            font-weight: 500;
            font-size: 1.1rem;
            padding: 0.5rem;
            border-radius: 8px;
            transition: background-color 0.3s ease;
        }
        .stRadio > label:hover {
            background-color: #c8e6c9;
        }

        /* Text area and file uploader styling */
        .stTextArea textarea, .stFileUploader {
            border: 2px solid #c8e6c9;
            border-radius: 8px;
            background-color: #ffffff;
            transition: border-color 0.3s ease;
        }
        .stTextArea textarea:focus, .stFileUploader:hover {
            border-color: #2e7d32;
        }

        /* Button styling */
        .stButton>button {
            background-color: #2e7d32;
            color: white;
            border-radius: 10px;
            padding: 0.6rem 1.5rem;
            font-weight: 500;
            transition: all 0.3s ease;
            width: 100%;
        }
        .stButton>button:hover {
            background-color: #1b5e20;
            transform: translateY(-2px);
        }

        /* Success and warning messages */
        .stAlert {
            border-radius: 8px;
            padding: 1rem;
            font-size: 1rem;
        }

        /* TABLE STYLING - ENHANCED */
        .dataframe {
            border: none !important;
            border-radius: 12px !important;
            overflow: hidden !important;
            box-shadow: 0 4px 20px rgba(0, 100, 0, 0.15) !important;
            font-family: 'Segoe UI', sans-serif !important;
        }
        
        .dataframe thead tr {
            background: linear-gradient(135deg, #2e7d32 0%, #4caf50 100%) !important;
        }
        
        .dataframe thead th {
            color: white !important;
            font-weight: 600 !important;
            padding: 15px 20px !important;
            text-align: left !important;
            border: none !important;
            font-size: 1rem !important;
        }
        
        .dataframe tbody td {
            padding: 15px 20px !important;
            border-bottom: 1px solid #e8f5e9 !important;
            color: #424242 !important;
            font-size: 0.95rem !important;
            line-height: 1.5 !important;
        }
        
        .dataframe tbody tr:nth-child(even) {
            background-color: #f9fcf9 !important;
        }
        
        .dataframe tbody tr:hover {
            background-color: #e8f5e9 !important;
            transform: scale(1.01) !important;
            transition: all 0.2s ease !important;
        }

        .result-header {
            background: linear-gradient(135deg, #2e7d32 0%, #4caf50 100%);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 10px;
            margin-bottom: 1.5rem;
            text-align: center;
            font-size: 1.3rem;
            font-weight: 600;
        }

        /* Metric Cards */
        .metric-row {
            display: flex;
            gap: 20px;
            margin: 20px 0;
            flex-wrap: wrap;
        }

        .metric-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0, 100, 0, 0.1);
            border-top: 4px solid #4caf50;
            width: 100%;
            transition: all 0.3s ease;
        }

        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0, 100, 0, 0.2);
        }

        .metric-number {
            font-size: 2rem;
            font-weight: bold;
            color: #2e7d32;
            margin-bottom: 0.5rem;
        }

        .metric-label {
            color: #666;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .main-container, .result-section {
            animation: fadeIn 0.6s ease-in;
        }

        /* Hide sidebar completely */
        .css-1lcbmhc.e1fqkh3o0 {
            display: none;
        }
        .css-1d391kg.e1fqkh3o1 {
            padding-left: 1rem;
        }

        /* Status Badge */
        .status-badge {
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .status-wajib {
            background: #ffebee;
            color: #c62828;
            border: 1px solid #ef5350;
        }
        .status-pilihan {
            background: #e3f2fd;
            color: #1565c0;
            border: 1px solid #42a5f5;
        }
        .status-praktek {
            background: #f3e5f5;
            color: #7b1fa2;
            border: 1px solid #ab47bc;
        }

        /* Checkbox styling */
        .stCheckbox {
            margin: 0.5rem 0;
        }
        
        .stCheckbox > label {
            display: flex;
            align-items: center;
            padding: 0.5rem;
            border-radius: 8px;
            transition: background-color 0.3s ease;
        }
        
        .stCheckbox > label:hover {
            background-color: #e8f5e9;
        }

        /* Selection mode styling */
        .selection-mode {
            background: #f3e5f5;
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid #9c27b0;
            margin: 1rem 0;
        }

        /* Course selection row */
        .course-row {
            padding: 0.8rem;
            margin: 0.5rem 0;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        
        .course-row:hover {
            background-color: #f9fcf9;
            border-color: #4caf50;
            transform: translateX(5px);
        }
        
        .course-row.selected {
            background-color: #e8f5e9;
            border-color: #4caf50;
            border-width: 2px;
        }

        /* Selected summary */
        .selected-summary {
            background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
            border: 2px solid #4caf50;
        }

        .student-info-card {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
            box-shadow: 0 2px 10px rgba(0, 100, 0, 0.1);
            border-left: 4px solid #4caf50;
        }

        .delete-button {
            background-color: #d32f2f !important;
        }
        .delete-button:hover {
            background-color: #b71c1c !important;
        }

        .edit-button {
            background-color: #f57c00 !important;
        }
        .edit-button:hover {
            background-color: #e65100 !important;
        }
    </style>
""",
    unsafe_allow_html=True,
)
