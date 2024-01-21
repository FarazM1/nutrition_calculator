import math
import pandas as pd
from matplotlib import pyplot as plt
import streamlit as st 


# Defining Variables

male =  False
female = False
lose_weight = False
maintain_weight = False
gain_weight = False
build_muscle = False
heathy_diet = False 
bmr = 0
intake = 0
mod_intake = 0 
food = []
calories = []
protein = []
fat = []
carbs = []

# User Input


st.header('Nutrition Calculator', divider= 'grey')
st.markdown(''' :blue[This Nutrition Calculator is meant to facilitate your fitness and health goals. By providing information about your body, eating habits, and goals, a nutrition plan will be created for you].''' )
st.subheader("General Information", divider = "grey")

weight = st.number_input('Please enter your current weight in pounds:', min_value = 1, value=1, step = 5)
height_ft = st.number_input('Please enter your height (feet):', min_value = 1, value = 1, step = 5)
height_in = st.number_input('Please enter your height (inches):', min_value = 1, value = 1, step = 5)
height = height_ft*12 + height_in
age = st.number_input('Age', min_value = 0, value=0, step=5)

sex = st.selectbox(label = 'Please select your sex:', options = ['Male', 'Female'])
if sex.lower() == 'male':
    male = True
else:
    female = True

activity_level = st.selectbox(label = 'Please choose an activity level from the following:', options = ['Little Exercise', 'Moderate Exercise', 'Heavy Exercise'])
little_exercise = (activity_level == "Little Exercise")
moderate_exercise = (activity_level == "Moderate Exercise")
heavy_exercise = (activity_level == "Heavy Exercise") 

user_goals = st.multiselect(label = 'Please choose your fitness and health goals:', options = ['Lose Weight', 'Maintain Weight', 'Gain Weight', 'Build Muscle', 'Overall Healthy Diet'])
user_goals = list(map(lambda x: x.lower(), user_goals))
user_goals = list(map(lambda x: x.strip(' '), user_goals))
for goal in user_goals:
    if 'lose' in goal:
        lose_weight = True
    if 'maintain' in goal:
        maintain_weight = True
    if 'build' in goal:
        build_muscle = True
    if 'healthy' in goal:
        healthy_diet = True 
    if 'gain' in goal:
        gain_weight = True 

st.subheader("Food Calculator", divider = "grey")
food_form = st.form("Food Tracker")
food_count = food_form.number_input('Please enter the number of foods you would like to track:', min_value = 1, value=1, step = 1)
food_form.form_submit_button("Continue") 


widget_id = (id for id in range(1, 10000))
for i in range(food_count):
    food.append(st.text_input('Please enter the name of the food:', key = next(widget_id)))
    calories.append(st.number_input('Please enter the number of calories in' + ' ' + food[i] + ":"+ "cals", min_value = 0, value=0, step = 1, key = next(widget_id)))
    fat.append(st.number_input('Please enter the amount of fat, in grams, in' + " " + food[i], min_value = 0, value=0, step = 1, key = next(widget_id)))
    carbs.append(st.number_input('Please enter the amount of carbohydrates, in grams, in' + ' ' + food[i], min_value = 0, value=0, step = 1, key = next(widget_id)))
    protein.append(st.number_input('Please enter the amount of protein, in grams in' + ' ' + food[i], min_value = 0, value=0, step = 1, key = next(widget_id)))
    st.subheader("", divider = "grey")

# Creating Food Data Frame

tracker = {'Foods': [] , 'Calories': [], "Protein": [], "Fat":[], "Carbohydrates":[]}

for i in range(len(food)):
    tracker['Foods'].append(food[i])
    tracker['Calories'].append(float(calories[i]))
    tracker['Protein'].append(float(protein[i]))
    tracker['Fat'].append(float(fat[i]))
    tracker['Carbohydrates'].append(float(carbs[i]))

nutrition = pd.DataFrame(tracker)
sums = {'Foods': 'Totals', 'Calories': nutrition['Calories'].sum(), 'Protein': nutrition['Protein'].sum(), 'Fat': nutrition['Fat'].sum(), 'Carbohydrates': nutrition['Carbohydrates'].sum()}
nutrition = nutrition._append(sums, ignore_index = True)
nutrition.set_index('Foods', inplace = True)



# Calculating Information for Nutrition Summary

if male == True:
    bmr = 4.536 * weight + 15.88* height - 5 * age + 5
    if little_exercise == True: 
        bmr = 1.375* bmr
    elif moderate_exercise == True:
        bmr = 1.55* bmr
    elif heavy_exercise == True:
        bmr = 1.725 * bmr
else: 
    bmr = 4.536 * weight + 15.88* height - 5 * age - 161
    if little_exercise == True: 
        bmr = 1.375* bmr
    elif moderate_exercise == True:
        bmr = 1.55* bmr
    elif heavy_exercise == True:
        bmr = 1.725 * bmr

if lose_weight == True:
    intake = .80*bmr
elif maintain_weight == True:
    intake = bmr
elif gain_weight == True:
    intake = 1.20*bmr
else: 
    intake = bmr

mod_intake = intake

# Nutrition Summary For user

st.subheader('Nutrition Sumary', divider = "grey")
st.write("Based on the information provided, your Basal Metabolic Rate (BMR) is", math.trunc(bmr), "calories")
st.write("Currently, you have consumed", math.trunc(nutrition._get_value('Totals', 'Calories')), "calories")
st.write("Here is an overview of your food consumed:")
st.dataframe(nutrition, use_container_width = True)

if lose_weight == True:
    if bmr-200 < 0:
        st.error("Uh oh! Something went wrong. Please check your responses.")
    else:
        st.write("In order to lose weight, you should eat between", math.trunc(bmr-500), "to", math.trunc(bmr-200), "calories per day")
        st.write("Typically, a calorie deficit decreases your calories by 20%. Therefore, your calorie intake should be", math.trunc(intake))
elif maintain_weight == True:
    if bmr < 0:
        st.error("Uh oh! Something went wrong. Please check your responses.")
    else:
        st.write("In order to maintain weight, you should continue to eat at your BMR of", math.trunc(bmr))

elif gain_weight == True:
    if bmr +500 < 0:
        st.error("Uh oh! Something went wrong. Please check your responses.")
    else: 
        st.write("In order to gain weight, you should eat between", math.trunc(bmr+300), "to", math.trunc(bmr+500), "calories per day")
        st.write("Typically, a calorie surplus increases your calories by 20%. Therefore, your calorie intake should be", math.trunc(intake))
if build_muscle == True:
    st.write("In order to build muscle, you should eat about", math.trunc(weight*.8), "grams of protein each day")



# Nutrition Plan For user

st.subheader('Nutrition Plan', divider = "grey")
st.write("A nutrition plan will be developed for you based on your preferred macronutrient and caloric intake")
carb_preference = st.selectbox('Please select your preferred carbohydrate intake:', options = ['High', 'Moderate', 'Low'])
fat_preference = st.selectbox('Please select your preferred fat intake:', options = ['High', 'Moderate', 'Low'])

if build_muscle == False:   
    protein_preference = st.selectbox('Please select your preferred protein intake:', options = ['High', 'Moderate', 'Low'])

plan_start = st.button("Generate Nutrition Plan", use_container_width = True)

if build_muscle == True:
    protein_intake = .8*weight
    intake = (intake- protein_intake*4)
    if carb_preference == "High":
        if fat_preference == "Low":
            carb_intake = (.45*intake)/4
            intake = (intake- carb_intake*4)
            fat_intake = intake/9
        if fat_preference == "Moderate":
            carb_intake = (.35*intake)/4
            intake = (intake- carb_intake*4)
            fat_intake = intake/9
        if fat_preference == "High":
            carb_intake = (.25*intake)/4
            intake = (intake- carb_intake*4)
            fat_intake = intake/9
    elif carb_preference == "Moderate":
        if fat_preference == "Low":
            carb_intake = (.35*intake)/4
            intake = (intake- carb_intake*4)
            fat_intake = intake/9
        if fat_preference == "Moderate":
            carb_intake = (.25*intake)/4
            intake = (intake- carb_intake*4)
            fat_intake = intake/9
        if fat_preference == "High":
            carb_intake = (.15*intake)/4
            intake = (intake- carb_intake*4)
            fat_intake = intake/9
    elif carb_preference == "Low":
        if fat_preference == "Low":
            carb_intake = (.30*intake)/4
            intake = (intake- carb_intake*4)
            fat_intake = intake/9
        if fat_preference == "Moderate":
            carb_intake = (.20*intake)/4
            intake = (intake- carb_intake*4)
            fat_intake = intake/9
        if fat_preference == "High":
            carb_intake = (.10*intake)/4
            intake = (intake- carb_intake*4)
            fat_intake = intake/9
elif build_muscle == False:
    if protein_preference == "Low":
        protein_intake = (.15*intake)/4
        intake = (intake- protein_intake*4)
    if protein_preference == "Moderate":
        protein_intake = (.25*intake)/4
        intake = (intake- protein_intake*4)
    if protein_preference == "High":
        protein_intake = (.35*intake)/4
        intake = (intake- protein_intake*4)    
    if carb_preference == "High":
        if fat_preference == "Low":
            carb_intake = (.45*intake)/4
            intake = (intake- carb_intake*4)
            fat_intake = intake/9
        if fat_preference == "Moderate":
            carb_intake = (.35*intake)/4
            intake = (intake- carb_intake*4)
            fat_intake = intake/9
        if fat_preference == "High":
            carb_intake = (.25*intake)/4
            intake = (intake- carb_intake*4)
            fat_intake = intake/9
    elif carb_preference == "Moderate":
        if fat_preference == "Low":
            carb_intake = (.35*intake)/4
            intake = (intake- carb_intake*4)
            fat_intake = intake/9
        if fat_preference == "Moderate":
            carb_intake = (.25*intake)/4
            intake = (intake- carb_intake*4)
            fat_intake = intake/9
        if fat_preference == "High":
            carb_intake = (.15*intake)/4
            intake = (intake- carb_intake*4)
            fat_intake = intake/9
    elif carb_preference == "Low":
        if fat_preference == "Low":
            carb_intake = (.30*intake)/4
            intake = (intake- carb_intake*4)
            fat_intake = intake/9
        if fat_preference == "Moderate":
            carb_intake = (.20*intake)/4
            intake = (intake- carb_intake*4)
            fat_intake = intake/9
        if fat_preference == "High":
            carb_intake = (.10*intake)/4
            intake = (intake- carb_intake*4)
            fat_intake = intake/9
    


if plan_start == True:
    if (type(carb_intake) != float or type(fat_intake) != float or type(protein_intake) != float) or (carb_intake < 0 or fat_intake < 0 or protein_intake<0):
        st.error("Please fill in the missing information to generate your plan")
        if (carb_intake < 0 or fat_intake < 0 or protein_intake<0):
            st.error("Please check your responses for invalid entries")
    else:
        total_intakes = {"Total Calories": [math.trunc(mod_intake)], "Grams of Protein": [math.trunc(protein_intake)], "Grams of Fats": [math.trunc(fat_intake)], "Grams of Carbohydrates": [math.trunc(carb_intake)]}
        plan = pd.DataFrame(total_intakes)
        st.write("Here is an advised nutrition plan based on your goals and preferences:")
        st.dataframe(plan, hide_index=True, use_container_width = True)
        labels = ['Protein', 'Fats', 'Carbohydrates']
        sizes = plan.loc[0, 'Grams of Protein':'Grams of Carbohydrates'].tolist()
        fig, ax = plt.subplots()
        plt.style.use('classic')
        ax.pie(sizes, labels=labels, autopct='%1.1f%%')
        st.pyplot(fig, use_container_width=True)

