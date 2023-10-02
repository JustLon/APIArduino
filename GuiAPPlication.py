import os

os.system('pip install --upgrade Kivy')


from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.togglebutton import ToggleButton

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        self.add_widget(layout)

        agregar_alarma_button = Button(text='Agregar Alarma', on_press=self.go_to_add_alarm, size_hint=(None, None), size=(200, 50), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        ver_alarmas_button = Button(text='Ver Alarmas', on_press=self.go_to_view_alarms, size_hint=(None, None), size=(200, 50), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout.add_widget(agregar_alarma_button)
        layout.add_widget(ver_alarmas_button)

    def go_to_add_alarm(self, instance):
        self.manager.current = 'add_alarm'

    def go_to_view_alarms(self, instance):
        self.manager.current = 'view_alarms'

class AddAlarmScreen(Screen):
    def __init__(self, **kwargs):
        super(AddAlarmScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.add_widget(layout)

        date_input = TextInput(hint_text='Ingrese la Fecha (YYYY-MM-DD)')
        hour_input = TextInput(hint_text='Ingrese la hora (hh:mm)')
        add_ampmtoogle = Button(text='AM', on_press=lambda x: self.add_toogleampm(add_ampmtoogle))
        type_input = TextInput(hint_text='Enter Alarm Type (Numeric)')

        add_button = Button(text='Add Alarm', on_press=lambda x: self.add_alarm(date_input.text, hour_input.text, type_input.text))
        layout.add_widget(date_input)
        layout.add_widget(hour_input)
        layout.add_widget(add_ampmtoogle)
        layout.add_widget(type_input)
        layout.add_widget(add_button)

    def add_alarm(self, date, hour, alarm_type):
        # Handle adding the alarm logic here (not implemented in this example)
        print(f'Alarm added: Date - {date}, Hour - {hour}, Type - {alarm_type}')

    def add_toogleampm(self, buton):
        if(buton.text == 'AM'):
            buton.text = 'PM'
        else:
            buton.text = 'AM'


class ViewAlarmsScreen(Screen):
    def __init__(self, **kwargs):
        super(ViewAlarmsScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.add_widget(layout)

        # Display alarms here (not implemented in this example)

class AlarmApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(AddAlarmScreen(name='add_alarm'))
        sm.add_widget(ViewAlarmsScreen(name='view_alarms'))
        return sm

if __name__ == '__main__':
    AlarmApp().run()