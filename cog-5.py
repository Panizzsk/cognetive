# Import necessary libraries
from psychopy import visual, core, event,gui
import random
import pandas as pd
import numpy as np


# Create a PsychoPy window
win = visual.Window(size=(800, 600), fullscr=False)

# Experiment setup
participant_info = {'Participant': '', 'Session': '001'}
dialog = gui.DlgFromDict(dictionary=participant_info, title='Risk Preference Study')
if not dialog.OK:
    core.quit()
    
    
instructions = visual.TextStim(win, text="Observe the other agent's risk-related decisions.\nPress any key to continue.")
instructions.draw()
win.flip()
event.waitKeys()

# Define stimuli (e.g., risky and safe options)
risky_option = visual.TextStim(win, text="Risky Option", pos=(0, 0))
safe_option = visual.TextStim(win, text="Safe Option", pos=(0, -0.2))

# Simulate an agent's risk preference (0 to 1, where 0 is risk-averse and 1 is risk-seeking)
agent_risk_preference = 0.7


results = []

# Main experiment loop
for trial in range(10):  # Adjust the number of trials as needed
    # Present options
    risk = random.random()
    money = random.randint(20,100)
    risky_option.draw()
    safe_option.draw()
    risk_angle = risk *360
    pie_segment_g = visual.Pie(win=win, radius=0.5, start=0.0, end=risk_angle, edges=32, fillColor='green')
    pie_segment_r = visual.Pie(win=win, radius=0.5, start=risk_angle, end=360, edges=32, fillColor='red')
    pie_segment_r.draw()
    pie_segment_g.draw()
    money_gambel = f"Risk for {money:.2f}$."
    gambel_text = visual.TextStim(win, text=money_gambel)
    gambel_text.draw()
    win.flip()
    core.wait(2)
    
    # Simulate participant's choice (0 for safe, 1 for risky)
    
    participant_choice = event.waitKeys(keyList=['up', 'down'])


    if participant_choice[0] == 'down':
        choice = 0 
        choice_text = "safe_option"
        money_text = f"You got 10$."
        money_plot = visual.TextStim(win, text=money_text)
        money_plot.draw()
        win.flip()
        core.wait(2)
    elif participant_choice[0] == 'up':
        choice = 1
        choice_text = "risky_option"
        if random.random()<risk:
            money_collected = 0
        else:
            money_collected = money
                
        
        money_text = f"You got {money_collected:.2f}."
        money_plot = visual.TextStim(win, text=money_text)
        money_plot.draw()
        win.flip()
        core.wait(2)
        
    
    results.append({'participant_id':participant_info['Participant'],'participant_session':participant_info['Session'],'risk_prob': risk, 'Participant_choice': choice_text, 'Participant_choice_flag': choice, 'gamble_money': money,"reward":money_collected})
    
    

    # Update agent's risk preference based on participant's choice
    agent_risk_preference = (agent_risk_preference + int(choice)) / 2
    
    # Pause briefly between trials
    core.wait(1)
        
        
# Close the window and end the experiment if ESC key is pressed

feedback_text = f"You got {agent_risk_preference:.2f}."

feedback_stim = visual.TextStim(win, text=feedback_text)
feedback_stim.draw()
win.flip()
core.wait(2)

print(f"Participant's risk preference: {agent_risk_preference:.2f}")
win.close()
core.quit()

df = pd.DataFrame(results)

file_name = f"data/{participant_info['Participant']}_{participant_info['Session']}"
# save data on CSV
df.to_csv(file_name+'.csv', index=False)



# Print the final updated risk preference
