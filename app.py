import streamlit as st
import pint 

# Pint library for unit conversion
ureg = pint.UnitRegistry()
ureg.define('square_meter = meter ** 2')
ureg.define('square_kilometer = kilometer ** 2')
ureg.define('square_centimeter = centimeter ** 2')
ureg.define('square_millimeter = millimeter ** 2')
ureg.define('square_mile = mile ** 2')
ureg.define('square_yard = yard ** 2')
ureg.define('square_foot = foot ** 2')
ureg.define('square_inch = inch ** 2')

# Session state to store conversion history
if 'history' not in st.session_state:
    st.session_state.history = []

# Custom CSS for professional styling
st.markdown("""
    <style>
    /* Main container styling */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
        padding: 20px;
    }
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        color: white;
        padding: 20px;
        border-radius: 10px;
    }
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
        transition: background 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #45a049, #4CAF50);
    }
    /* Input fields styling */
    {
        background: white;
        border-radius: 5px;
        border: 1px solid #ddd;
        padding: 10px;
    }
    /* Header styling */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #4CAF50;
        margin-bottom: 10px;
    }
    /* History card styling */
    .history-card {
        background: white;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar for additional options
with st.sidebar:
    st.markdown("## 🛠️ Settings")
    st.markdown("Customize your experience here.")
    if st.button("Clear History ❌"):
        st.session_state.history = []
        st.success("History cleared successfully!")

# Main content
st.title("🔄 Unit Converter")

# Unit categories
unit_categories = {
    "📏 Length": ["meter", "kilometer", "centimeter", "millimeter", "micrometer", "nanometer", "mile", "yard", "foot", "inch", "light_year"],
    "🌡️ Temperature": ["celsius", "fahrenheit", "kelvin"],
    "📐 Area": ["square_meter", "square_kilometer", "square_centimeter", "square_millimeter", "square_mile", "square_yard", "square_foot", "square_inch"],
    "🧊 Volume": ["liter", "milliliter", "cubic_meter", "cubic_centimeter", "cubic_millimeter", "gallon", "quart", "pint", "cup", "fluid_ounce"],
    "⚖️ Weight": ["gram", "kilogram", "milligram", "microgram", "ton", "pound", "ounce"],
    "⏳ Time": ["second", "minute", "hour", "day", "week", "month", "year"]
}

# Select conversion type
st.subheader("Select Conversion Type")
category = st.selectbox("Category", list(unit_categories.keys()))

# Layout for conversion input
st.markdown("### Conversion Details")
col1, col2, col3 = st.columns([3, 1, 3])

with col1:
    from_unit = st.selectbox("From Unit", unit_categories[category])
    value = st.number_input("Enter Value:")

with col2:
    st.markdown("<h3 style='text-align: center; color: #4CAF50;'>=</h3>", unsafe_allow_html=True)

with col3:
    converted_value = ""
    to_unit = st.selectbox("To Unit", unit_categories[category])

def convert_temperature(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value
    elif from_unit == "celsius" and to_unit == "fahrenheit":
        return (value * 9/5) + 32
    elif from_unit == "fahrenheit" and to_unit == "celsius":
        return (value - 32) * 5/9
    elif from_unit == "celsius" and to_unit == "kelvin":
        return value + 273.15
    elif from_unit == "kelvin" and to_unit == "celsius":
        return value - 273.15
    elif from_unit == "fahrenheit" and to_unit == "kelvin":
        return (value - 32) * 5/9 + 273.15
    elif to_unit == "fahrenheit" and from_unit == "kelvin":
        return (value - 273.15) * 9/5 + 32
    return None

# Convert button
if st.button("Convert 🔄"):
    try:
        if category == "🌡️ Temperature":
            result = convert_temperature(value, from_unit, to_unit)
        else:
            result = (value * ureg(from_unit)).to(to_unit)
        
        converted_value = f"{result:.6f}"
        st.success(f"✅ {value} {from_unit} = {converted_value} {to_unit}")
        
        # Store result in history
        st.session_state.history.append(f"{value} {from_unit} → {converted_value} {to_unit}")
    except Exception as e:
        st.error(f"⚠️ Conversion error: {e}")

# History section
st.markdown("---")
st.subheader("📜 Conversion History")
if st.session_state.history:
    for entry in st.session_state.history[::-1]:
        st.markdown(f"""
        <div class="history-card">
            <p style="font-size: 16px; color: #333;">{entry}</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No conversion history yet. Start converting units to see your history here!")
