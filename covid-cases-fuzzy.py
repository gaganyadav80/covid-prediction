### BLOCK 1
# !pip install scikit-fuzzy
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


### BLOCK 2
x = np.arange(0,190,0.1)
y = fuzz.membership.gaussmf(x, 2.5, 19.11)
y1 = fuzz.membership.gaussmf(x, 75, 12.74)
y2 = fuzz.membership.gaussmf(x, 140, 16.99)

covidcases = ctrl.Antecedent(x, 'covidcases')

covidcases['low'] = y
covidcases['medium'] = y1
covidcases['high'] = y2
covidcases.view()


### BLOCK 3
x = np.arange(0,60,0.1)
y = fuzz.membership.gaussmf(x, -2.22e-16, 5.493)
y1 = fuzz.membership.gaussmf(x, 26.5, 3.61)
y2 = fuzz.membership.gaussmf(x, 40, 2.247)

climateTemp = ctrl.Antecedent(x, 'climateTemp')

climateTemp['low'] = y
climateTemp['medium'] = y1
climateTemp['high'] = y2

climateTemp.view()


### BLOCK 4
x = np.arange(95,105,0.1)
y = fuzz.membership.gaussmf(x, 96, 0.4247)
y1 = fuzz.membership.gaussmf(x, 98, 0.4247)
y2 = fuzz.membership.gaussmf(x, 101, 0.8)

bodyTemp = ctrl.Antecedent(x, 'bodyTemp')

bodyTemp['low'] = y
bodyTemp['medium'] = y1
bodyTemp['high'] = y2

bodyTemp.view()


### BLOCK 5
x = np.arange(0,10,0.1)
y = fuzz.membership.gaussmf(x, 0.5, 0.574)
y1 = fuzz.membership.gaussmf(x, 5.0, 0.574)
y2 = fuzz.membership.gaussmf(x, 7.5, 0.574)

shortBreath = ctrl.Antecedent(x, 'shortBreath')

shortBreath['low'] = y
shortBreath['medium'] = y1
shortBreath['high'] = y2

shortBreath.view()


### BLOCK 6
x = np.arange(0,1,0.001)
y = fuzz.membership.gaussmf(x, 0.1, 0.08)
y1 = fuzz.membership.gaussmf(x, 0.5, 0.08)
y2 = fuzz.membership.gaussmf(x, 1, 0.08)

severity = ctrl.Consequent(x, 'severity')

severity['lessSevere'] = y
severity['normal'] = y1
severity['severe'] = y2

severity.view()


### BLOCK 7
rule1 = ctrl.Rule(climateTemp['medium'] & bodyTemp['medium'] & covidcases['low'] & shortBreath['low'], severity['lessSevere'])
rule2 = ctrl.Rule(climateTemp['low'] & bodyTemp['low'] & covidcases['low'] & shortBreath['low'], severity['lessSevere'])
# rule3 = ctrl.Rule(climateTemp['high'] & bodyTemp['medium'] & covidcases['low'] & shortBreath['low'], severity['lessSevere'])

# rule7 = ctrl.Rule(climateTemp['medium'] & bodyTemp['high'] & covidcases['high'] & shortBreath['high'], severity['severe'])
# rule8 = ctrl.Rule(climateTemp['low'] & bodyTemp['high'] & covidcases['high'] & shortBreath['high'], severity['severe'])
rule9 = ctrl.Rule(climateTemp['high'] & bodyTemp['high'] & covidcases['high'] & shortBreath['high'], severity['severe'])

rule13 = ctrl.Rule(climateTemp['medium'] & bodyTemp['high'] & covidcases['medium'] & shortBreath['medium'], severity['normal'])
# rule14 = ctrl.Rule(climateTemp['low'] & bodyTemp['high'] & covidcases['medium'] & shortBreath['medium'], severity['normal'])
rule15 = ctrl.Rule(climateTemp['high'] & bodyTemp['high'] & covidcases['medium'] & shortBreath['medium'], severity['normal'])

# rule1.view()
covidPreditction = ctrl.ControlSystem([rule1, rule2, rule9, rule13, rule15])
predictor= ctrl.ControlSystemSimulation(covidPreditction)


### BLOCK 8
from IPython.display import display
import ipywidgets as widgets
button = widgets.Button(description="Run Cell to get output")
output = widgets.Output()

display(button, output)

#@title Covid Self Tester
global State, Climate_Temp_Celsius, Body_Temp_Fahrenheit, Shortness_Of_Breath
# State = "Odisha" #@param ['Andaman And Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 'Dadra And Nagar Haveli And Daman And Diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu And Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telengana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal']
Spread_in_your_locality = 0.4 #@param {type:"slider", min:0, max:1.9, step:0.1}
Climate_Temp_Celsius = 30#@param {type:"integer"}
Body_Temp_Fahrenheit = 98#@param {type:"number", max:105}
Shortness_Of_Breath = 2#@param {type:"slider", min:0, max:10, step:1}

State = Spread_in_your_locality*100
# Climate_Temp_Celsius = max(0, Climate_Temp_Celsius)
# Body_Temp_Fahrenheit = max(95, Body_Temp_Fahrenheit)
# Climate_Temp_Celsius = min(60, Climate_Temp_Celsius)
# Body_Temp_Fahrenheit = min(105, Body_Temp_Fahrenheit)

# location = df.loc[df['STATE/UTS']== State]
# StateVal = (location.values.tolist()[0][1])

predictor.input['shortBreath'] = Shortness_Of_Breath
predictor.input['bodyTemp'] = Body_Temp_Fahrenheit
predictor.input['covidcases'] = State

predictor.input['climateTemp'] = Climate_Temp_Celsius

predictor.compute() 
format_float = "{:.2f}".format(predictor.output['severity']*100)
print("Your chances of having covid is:",format_float,"%")
severity.view(sim=predictor)
