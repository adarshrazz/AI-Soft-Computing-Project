🌱 Smart Irrigation System Using Sugeno Fuzzy Logic
A Python-based smart irrigation simulation that estimates an irrigation duration from soil moisture and temperature using a Zero-Order Sugeno Fuzzy Inference System (FIS). The project demonstrates how fuzzy sets, membership functions, fuzzy IF–THEN rules, rule firing strengths, and a weighted-average output can be combined into an explainable decision-support system.
Project type: Academic mini-project / software simulation
Inference method: Zero-Order Sugeno Fuzzy Inference System
Interface: Streamlit
Language: Python
Hardware: Not required

🎥 Project Demonstration
Watch the recorded demonstration:

▶️ Watch the Smart Irrigation System Demo on Google Drive

If the video does not open, the owner may need to set Google Drive sharing to Anyone with the link — Viewer.
📌 Project Overview
Traditional irrigation schedules may use fixed watering durations even when environmental conditions change. This project demonstrates a fuzzy-logic approach that considers two inputs:
- Soil moisture (%) — lower moisture generally increases the simulated need for irrigation.
- Temperature (°C) — higher temperature can increase the simulated duration when the soil is not already sufficiently moist.
The application fuzzifies the numerical inputs, evaluates the rules, and calculates a recommended irrigation duration between 0 and 10 minutes. The Streamlit dashboard displays the output, membership degrees, fired rules, membership-function plots, and a response-surface visualization.

This is an educational simulation. It does not read physical sensors or operate a real pump.
🎯 Objectives
- Apply fuzzy logic to a simple irrigation decision problem.
- Model soil moisture and temperature with linguistic fuzzy sets.
- Implement a Zero-Order Sugeno inference engine in Python.
- Explain how rule firing strengths affect the final output.
- Visualize membership functions and model behavior.
- Test the system with different simulated environmental conditions.
🧠 Fuzzy Logic Concepts Used
1. Fuzzy sets
A fuzzy set allows an input to belong to a category to a degree between 0 and 1, rather than requiring a strict yes/no classification. For example, soil moisture may be partly Low and partly Medium.
2. Linguistic variables
The model uses human-readable labels to describe input conditions:
Variable	Range	Linguistic sets
Soil moisture	0–100%	Low, Medium, High
Temperature	0–50°C	Low, Medium, High


3. Membership functions
Triangular membership functions map each crisp input value to a membership degree. The model uses shoulder-shaped triangles at the edges of the supported ranges.

For a triangular membership function with parameters \(a,b,c\), the membership degree rises from 0 to 1 and then falls to 0. A value can have non-zero membership in more than one fuzzy set.

The current membership-function parameters are:

Soil moisture
Fuzzy set	Parameters \((a,b,c)\)
Low	(0, 0, 40)
Medium	(20, 50, 80)
High	(60, 100, 100)


Temperature
Fuzzy set	Parameters \((a,b,c)\)
Low	(0, 0, 20)
Medium	(10, 25, 40)
High	(30, 50, 50)


These parameters are project design choices for demonstration, not universal agricultural thresholds.
4. Fuzzification
Fuzzification converts the crisp numerical inputs into membership degrees. For example, a soil moisture input can produce a degree for Low, Medium, and High.
5. Fuzzy IF–THEN rules
The rule base contains nine rules, formed from the three soil-moisture sets and three temperature sets.

Examples:
- IF soil moisture is Low AND temperature is High, THEN irrigation duration is 10 minutes.
- IF soil moisture is Medium AND temperature is Medium, THEN irrigation duration is 4 minutes.
- IF soil moisture is High, THEN the rules recommend 0 minutes in this model.
The rules encode the intended behavior: dry soil generally receives more irrigation, while already moist soil should not receive additional watering merely because the temperature is high.
6. Fuzzy AND operator and rule firing strength
The system uses the minimum operator to combine the membership degrees of the two antecedents:
\[
w_i = \min(\mu_{\text{soil},i},\mu_{\text{temperature},i})
\]
Here, \(w_i\) is the firing strength of rule \(i\). A rule with a firing strength of 0 does not contribute to the final result.
7. Zero-Order Sugeno inference
In a Zero-Order Sugeno system, every rule has a constant numerical consequent \(z_i\). The rule outputs are combined with a weighted average instead of creating an output fuzzy set and applying centroid defuzzification.
Soil moisture	Low temperature	Medium temperature	High temperature
Low	7 min	8 min	10 min
Medium	3 min	4 min	6 min
High	0 min	0 min	0 min


These constants are illustrative values chosen for the mini-project, not agronomically validated watering recommendations.
8. Weighted-average output
The final irrigation duration is calculated as:
\[
z^* = \frac{\sum_{i=1}^{n} w_i z_i}{\sum_{i=1}^{n} w_i}
\]
where:
- \(w_i\) is the firing strength of rule \(i\);
- \(z_i\) is the constant output assigned to rule \(i\);
- \(n\) is the number of rules contributing to the output;
- \(z^*\) is the calculated irrigation duration in minutes.
The output is constrained to the project's configured range of 0–10 minutes.
9. Output interpretation
The dashboard displays the calculated duration and a simple category:
Output duration	Display category
Below 0.5 minutes	No irrigation
0.5 to below 3.5 minutes	Low
3.5 to below 7 minutes	Moderate
7 to 10 minutes	High


The category is a presentation aid. The numerical duration is the model's main output, and category boundaries are design choices for this simulation.
⚙️ System Workflow
1. The user enters soil moisture and temperature in the Streamlit dashboard.
2. The application validates that both values are within the supported ranges.
3. Membership functions calculate the degrees for Low, Medium, and High.
4. The fuzzy rule base calculates rule firing strengths using the minimum operator.
5. The Zero-Order Sugeno engine combines the rule constants using the weighted-average formula.
6. The dashboard shows the recommended duration, category, membership degrees, active rules, and visualizations.
🏗️ Project Structure
smart_irrigation_sugeno/
├── app.py                 # Streamlit dashboard
├── membership.py          # Membership functions and fuzzy sets
├── sugeno.py              # Sugeno rules and inference calculation
├── visualizations.py      # Membership plots and response surface
├── test_cases.py          # Basic scenario and range checks
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
🛠️ Technologies Used
- Python — application logic and fuzzy inference
- Streamlit — interactive web interface
- NumPy — numerical calculations and plot data
- Matplotlib — membership-function and response-surface graphs
- Pandas — display rule and membership tables
The Sugeno inference calculation is implemented in the project source code so that the algorithm can be inspected and explained.
🚀 Installation and Setup
Prerequisites
- Python installed on Windows, macOS, or Linux
- Git (optional, for version control)
- The project files downloaded or cloned locally
1. Open the project folder
Open a terminal in the directory containing app.py and requirements.txt.
2. Create a virtual environment
Windows PowerShell:
py -m venv .venv
If the py command is unavailable but python works, use:
python -m venv .venv
3. Install dependencies
To avoid PowerShell activation-policy issues, use the virtual environment's Python directly:
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
4. Run the application
.\.venv\Scripts\python.exe -m streamlit run app.py
Streamlit will display a local URL, usually http://localhost:8501. Open that URL in your browser.

macOS/Linux: After creating the environment, use source .venv/bin/activate, then pip install -r requirements.txt and streamlit run app.py.
🧪 Run the Test Scenarios
Run the included basic checks from the project directory:
.\.venv\Scripts\python.exe test_cases.py
The script prints example scenarios and checks that the calculated output remains within the configured 0–10 minute range. These checks verify basic program behavior; they do not validate agricultural effectiveness.

Example scenarios include:
- Dry soil with hot weather
- Moderate soil moisture and temperature
- Moist soil with hot weather
- Wet soil with cool weather
☁️ Deployment
The app can be deployed using Streamlit Community Cloud:
1. Push the project files to a GitHub repository.
2. Visit Streamlit Community Cloud.
3. Connect your GitHub account and select the repository.
4. Select branch main and main file path app.py.
5. Deploy the application.
Ensure requirements.txt is committed to the repository so the deployment environment can install the dependencies.
📊 Expected Output
For the selected input values, the application displays:
- Recommended duration: a numerical value between 0 and 10 minutes.
- Model category: No irrigation, Low, Moderate, or High.
- Input membership degrees: membership values for each fuzzy set.
- Active rules: rules with non-zero firing strength, their strengths, constants, and weighted contributions.
- Membership-function plots: how soil moisture and temperature map to fuzzy sets.
- Response surface: how the output varies across the input ranges.
The output is deterministic: the same inputs and model configuration produce the same result.
⚠️ Limitations
- This is a software simulation; it does not connect to real sensors or operate a water pump.
- Membership-function parameters and rule constants are illustrative and have not been validated by agricultural experts.
- The model does not account for crop type, soil type, rainfall, root depth, irrigation flow rate, or evapotranspiration.
- The result should not be treated as a real-world watering prescription without agronomic calibration and safety testing.
- A higher temperature does not always mean more watering is appropriate; the soil-moisture rules intentionally prevent irrigation when the soil is already classified as High.
🔮 Future Improvements
- Calibrate the model using crop- and soil-specific data.
- Add rainfall and crop type as additional inputs.
- Connect actual sensors and a pump in a separate hardware extension.
- Record scenario history and compare model outputs.
- Evaluate the fuzzy model against a baseline irrigation strategy.
👨‍🎓 Academic Summary
This mini-project demonstrates the use of fuzzy sets, membership functions, fuzzification, linguistic variables, IF–THEN rules, the minimum AND operator, rule firing strength, Zero-Order Sugeno inference, and weighted-average output calculation in an irrigation-duration simulation.

The key learning outcome is understanding how uncertain or gradual input conditions can be represented with fuzzy membership degrees and converted into an interpretable numerical output.
Note: This repository presents an educational fuzzy-logic model. The output duration is a simulated recommendation, not a guarantee of crop water requirements.
