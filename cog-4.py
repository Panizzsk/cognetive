from psychopy import visual, event, core, data, gui
import random
import pandas as pd

# settings
win = visual.Window([800,600])
instructions = visual.TextStim(win, text="Welcome to the experiment.\nPress any key to start.")
instructions.draw()
win.flip()
event.waitKeys()

n_trial_1=20
n_trial_2=100
n_trial_3=24
n_trial_4=16

trials = [n_trial_1,n_trial_2,n_trial_3,n_trial_4]
trial_names = ["Training phase","Learning phase","Post learning","estimation"]

reward_distributions = {
    'あ': (64, 13),
    'ビ': (64, 13),
    'だ': (54, 13),
    'エ': (44, 13)
}
options = ['あ', 'ビ', 'だ', 'エ']
feedback_type = "Complete"  #'Partial'  # یا 'Complete'

# calculating rewards
def get_reward(option):
    mean, std = reward_distributions[option]
    return random.gauss(mean, std)

# run tasks
results = []
for i,n_trial in enumerate(trials):
    phase_beginning_text = visual.TextStim(win, text=f"beginning phase:\n{trial_names[i]}")
    phase_beginning_text.draw()
    win.flip()
    event.waitKeys()
    for trial in range(n_trial):
        random.shuffle(options)
        choice_pair = options[:2]

        choice_text = f"Choose between {choice_pair[0]} and {choice_pair[1]}"
        choice_stim = visual.TextStim(win, text=choice_text)
        choice_stim.draw()
        win.flip()

        keys = event.waitKeys(keyList=['left', 'right'])
        choice = choice_pair[0] if keys[0] == 'left' else choice_pair[1]
        reward = get_reward(choice)

        if feedback_type == 'Complete':
            counterfactual_choice = choice_pair[1] if choice == choice_pair[0] else choice_pair[0]
            counterfactual_reward = get_reward(counterfactual_choice)
            feedback_text = f"You chose {choice} and got {reward:.2f}.\n{counterfactual_choice} would have given {counterfactual_reward:.2f}."
        else:
            feedback_text = f"You chose {choice} and got {reward:.2f}."

        feedback_stim = visual.TextStim(win, text=feedback_text)
        feedback_stim.draw()
        win.flip()
        core.wait(2)

        results.append({'trial phase':trial_names[i],'trial': trial, 'choice_pair': choice_pair, 'choice': choice, 'reward': reward})
    
    
# transform data to DataFrame
df = pd.DataFrame(results)

# save data on CSV
df.to_csv('experiment_results.csv', index=False)

# end task
end_text = visual.TextStim(win, text="Thank you for participating.\nPress any key to exit.")
end_text.draw()
win.flip()
event.waitKeys()
win.close()
core.quit()
