import json
import random
import glob
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

# White background to match the application pegs
Window.clearcolor = (1, 1, 1, 1)
Window.size = (360, 640)

def load_all_json_data():
    """
    Dynamically loads and merges all .json files in the directory.
    Groups them by their filename prefix (e.g., PIPE_1.json -> PIPE).
    """
    combined_data = {}
    json_files = glob.glob("*.json")
    
    for filename in json_files:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Extract main category (e.g., "PIPE_2.json" becomes "PIPE")
                raw_name = filename.replace('.json', '').upper()
                main_category = raw_name.split('_')[0] 
                
                # Ensure the master dictionary has this category
                if main_category not in combined_data:
                    combined_data[main_category] = {}
                    
                # Identify if the parsed JSON is wrapped in a top-level key
                if raw_name in data and isinstance(data[raw_name], dict):
                    source_data = data[raw_name]
                elif main_category in data and isinstance(data[main_category], dict):
                    source_data = data[main_category]
                else:
                    source_data = data
                    
                # Merge the sub-topics and their questions
                for sub_topic, questions in source_data.items():
                    if sub_topic in combined_data[main_category]:
                        combined_data[main_category][sub_topic].extend(questions)
                    else:
                        combined_data[main_category][sub_topic] = questions
                        
        except Exception:
            continue
            
    # Fallback if no valid JSON files are found
    if not combined_data:
        return {"ERROR": {"No Data Found": [{"question": "Database missing or empty.", "choices": ["A", "B", "C", "D"], "answer": "A"}]}}
        
    return combined_data

class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MainMenuScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Header matching the reference pegs
        header_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.2))
        header_layout.add_widget(Label(text="WELCOME!!", color=(0,0,0,1), font_size='32sp', bold=True))
        header_layout.add_widget(Label(text="MSU GENSAN REVIEWER", color=(0,0,0.8,1), font_size='18sp', bold=True))
        layout.add_widget(header_layout)
        
        # Fixed subject buttons
        btn_layout = BoxLayout(orientation='vertical', spacing=10, size_hint=(1, 0.6))
        categories = ["MESL", "PIPE", "MD"]
        
        for cat in categories:
            btn = Button(text=cat, color=(0.8, 0, 0, 1), background_normal='', background_color=(0.9, 0.9, 0.9, 1), 
                         size_hint=(None, None), size=(250, 40), pos_hint={'center_x': 0.5}, bold=True)
            btn.bind(on_press=lambda instance, c=cat: App.get_running_app().open_submenu(c))
            btn_layout.add_widget(btn)
            
        layout.add_widget(btn_layout)
        layout.add_widget(Label(text="Credits: Christian Lloyd Reandino", color=(0,0,0,1), font_size='12sp', size_hint=(1, 0.2), bold=True))
        self.add_widget(layout)

class SubMenuScreen(Screen):
    def __init__(self, **kwargs):
        super(SubMenuScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Top Nav for backing out of the submenu
        nav_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        back_btn = Button(text="< Back", size_hint=(None, None), size=(80, 40), background_normal='', background_color=(0.8, 0.2, 0.2, 1))
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'menu'))
        nav_layout.add_widget(back_btn)
        nav_layout.add_widget(Label(text="")) # spacer
        self.layout.add_widget(nav_layout)
        
        # Scrollable area for dynamically loaded subcategories
        scroll = ScrollView(size_hint=(1, 0.9))
        self.grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        
        scroll.add_widget(self.grid)
        self.layout.add_widget(scroll)
        self.add_widget(self.layout)

    def populate(self, main_category, subcategories):
        self.grid.clear_widgets()
        for sub in subcategories:
            btn = Button(text=sub, color=(0, 0, 0, 1), background_normal='', background_color=(0.92, 0.92, 0.92, 1), 
                         size_hint_y=None, height=50)
            btn.bind(on_press=lambda instance, s=sub: App.get_running_app().setup_prequiz(main_category, s))
            self.grid.add_widget(btn)

class PreQuizScreen(Screen):
    def __init__(self, **kwargs):
        super(PreQuizScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Circular-style nav buttons matching the pegs
        nav_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        restart_btn = Button(text="restart", size_hint=(None, None), size=(60, 50), background_normal='', background_color=(0.2, 0.6, 0.6, 1), color=(1,1,1,1))
        restart_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'menu'))
        next_btn = Button(text="next", size_hint=(None, None), size=(60, 50), background_normal='', background_color=(0.2, 0.6, 0.6, 1), color=(1,1,1,1))
        next_btn.bind(on_press=lambda x: App.get_running_app().start_quiz())
        
        nav_layout.add_widget(restart_btn)
        nav_layout.add_widget(Label(text="")) 
        nav_layout.add_widget(next_btn)
        layout.add_widget(nav_layout)
        
        self.title_lbl = Label(text="COACHING NOTES", color=(0.2, 0.6, 0.6, 1), font_size='18sp', bold=True, size_hint=(1, 0.1), text_size=(320, None), halign='left')
        layout.add_widget(self.title_lbl)
        
        layout.add_widget(Label(text="When you click the next button the quiz will begin. Do your best to answer each question correctly. Good Luck!", 
                                color=(0,0,0,1), text_size=(320, None), halign='left', size_hint=(1, 0.2)))
        
        layout.add_widget(Label(text="Name or User ID:", color=(0,0,0,1), text_size=(320, None), halign='left', size_hint=(1, 0.05)))
        self.name_input = TextInput(multiline=False, size_hint=(1, None), height=40)
        layout.add_widget(self.name_input)
        
        layout.add_widget(Label(text="", size_hint=(1, 0.55))) 
        self.add_widget(layout)

class QuizScreen(Screen):
    def __init__(self, **kwargs):
        super(QuizScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Circular-style nav buttons
        nav_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        restart_btn = Button(text="restart", size_hint=(None, None), size=(60, 50), background_normal='', background_color=(0.2, 0.6, 0.6, 1), color=(1,1,1,1))
        restart_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'menu'))
        
        self.next_btn = Button(text="next", size_hint=(None, None), size=(60, 50), background_normal='', background_color=(0.2, 0.6, 0.6, 1), color=(1,1,1,1))
        self.next_btn.bind(on_press=self.submit_and_next)
        
        nav_layout.add_widget(restart_btn)
        nav_layout.add_widget(Label(text="")) 
        nav_layout.add_widget(self.next_btn)
        self.layout.add_widget(nav_layout)
        
        self.title_lbl = Label(text="COACHING NOTES", color=(0.2, 0.6, 0.6, 1), font_size='18sp', bold=True, size_hint=(1, 0.1), text_size=(320, None), halign='left')
        self.layout.add_widget(self.title_lbl)
        
        self.tracker_lbl = Label(text="Question 1 of X", color=(0,0,0,1), size_hint=(1, 0.05), text_size=(320, None), halign='left')
        self.layout.add_widget(self.tracker_lbl)
        
        self.q_label = Label(text="Question text here", color=(0,0,0,1), size_hint=(1, 0.25), text_size=(320, None), halign='left', valign='top')
        self.layout.add_widget(self.q_label)
        
        # Standard Radio Button layout matching the pegs
        self.choices_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.5), spacing=5)
        self.checkboxes = []
        self.choice_labels = []
        
        for i in range(4):
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            cb = CheckBox(group='answers', color=(0,0,0,1), size_hint_x=0.1)
            lbl = Label(text="", color=(0,0,0,1), text_size=(280, None), halign='left', size_hint_x=0.9)
            row.add_widget(cb)
            row.add_widget(lbl)
            self.choices_layout.add_widget(row)
            self.checkboxes.append(cb)
            self.choice_labels.append(lbl)
            
        self.layout.add_widget(self.choices_layout)
        self.add_widget(self.layout)

    def start_quiz(self, title, questions):
        self.title_lbl.text = f"COACHING NOTES ({title.upper()})"
        self.questions = questions
        random.shuffle(self.questions)
        self.current_idx = 0
        self.score = 0
        self.next_btn.disabled = False
        self.display_question()

    def display_question(self):
        if self.current_idx < len(self.questions):
            q_data = self.questions[self.current_idx]
            self.tracker_lbl.text = f"Question {self.current_idx + 1} of {len(self.questions)}"
            self.q_label.text = q_data['question']
            
            for i in range(4):
                self.checkboxes[i].active = False 
                if i < len(q_data['choices']):
                    self.choice_labels[i].text = q_data['choices'][i]
                    self.checkboxes[i].opacity = 1
                    self.checkboxes[i].disabled = False
                    self.choice_labels[i].opacity = 1
                else:
                    self.choice_labels[i].text = ""
                    self.checkboxes[i].opacity = 0
                    self.checkboxes[i].disabled = True
                    self.choice_labels[i].opacity = 0
        else:
            # End of Quiz Screen
            user_name = self.manager.get_screen('prequiz').name_input.text
            self.q_label.text = f"Quiz Complete!\nFinal Score: {self.score} / {len(self.questions)}\nUser: {user_name}"
            self.tracker_lbl.text = ""
            for i in range(4):
                self.checkboxes[i].opacity = 0
                self.choice_labels[i].opacity = 0
            self.next_btn.disabled = True

    def submit_and_next(self, instance):
        if self.current_idx >= len(self.questions):
            return
            
        selected_text = ""
        for i, cb in enumerate(self.checkboxes):
            if cb.active:
                selected_text = self.choice_labels[i].text
                break
                
        correct_ans_text = self.questions[self.current_idx]['answer']
        
        # Simple evaluation logic
        if selected_text and correct_ans_text.lower() in selected_text.lower():
            self.score += 1
            
        self.current_idx += 1
        self.display_question()

class MELEApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.quiz_data = load_all_json_data()
        
        self.sm.add_widget(MainMenuScreen(name='menu'))
        self.sm.add_widget(SubMenuScreen(name='submenu'))
        self.sm.add_widget(PreQuizScreen(name='prequiz'))
        self.sm.add_widget(QuizScreen(name='quiz'))
        
        # Track routing variables
        self.active_main_cat = ""
        self.active_sub_cat = ""
        
        return self.sm

    def open_submenu(self, main_category):
        self.active_main_cat = main_category
        if main_category in self.quiz_data:
            sub_cats = list(self.quiz_data[main_category].keys())
            self.sm.get_screen('submenu').populate(main_category, sub_cats)
            self.sm.current = 'submenu'

    def setup_prequiz(self, main_category, sub_category):
        self.active_sub_cat = sub_category
        prequiz = self.sm.get_screen('prequiz')
        prequiz.title_lbl.text = f"COACHING NOTES {main_category}"
        self.sm.current = 'prequiz'
        
    def start_quiz(self):
        quiz = self.sm.get_screen('quiz')
        questions = self.quiz_data[self.active_main_cat][self.active_sub_cat]
        quiz.start_quiz(self.active_main_cat, questions)
        self.sm.current = 'quiz'

if __name__ == "__main__":
    MELEApp().run()