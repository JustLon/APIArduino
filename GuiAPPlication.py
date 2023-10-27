import os

os.system('pip install --upgrade Kivy')


from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.togglebutton import ToggleButton
import requests
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget

class ResponsePopup(Popup):
    def __init__(self, response, **kwargs):
        super(ResponsePopup, self).__init__(**kwargs)
        self.title = 'Server Response'
        self.content = BoxLayout(orientation='vertical')

        # Label to display the response message
        response_label = Label(text=response, size_hint_y=None, height=dp(40))
        self.content.add_widget(response_label)

        # Button to close the popup
        close_button = Button(text='Close', size_hint_y=None, height=dp(40))
        close_button.bind(on_press=self.dismiss_popup)
        self.content.add_widget(close_button)

    def dismiss_popup(self, instance):
        self.dismiss()

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
        # Reload the data from the API endpoint

            # Switch to the 'view_alarms' screen
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
        ampmtext = add_ampmtoogle.text
        add_button = Button(text='Add Alarm', on_press=lambda x: self.add_alarm(date_input.text, hour_input.text, type_input.text,ampmtext))
        cerrar_Boton = Button(text='Cerrar', on_press=lambda x: self.cerrar_Boton(cerrar_Boton))
        layout.add_widget(date_input)
        layout.add_widget(hour_input)
        layout.add_widget(add_ampmtoogle)
        layout.add_widget(type_input)
        layout.add_widget(add_button)
        layout.add_widget(cerrar_Boton)

    def cerrar_Boton(self, instance):
        self.manager.current = 'main'

    def add_alarm(self, date, hour, alarm_type, ampmtext):
        # Handle adding the alarm logic here (not implemented in this example)
        Hora, minutos = hour.split(":")
        AMorPM = ampmtext

        if (int(Hora)<=12) and (int(minutos)<60): #Hora comprobador
            url = 'http://192.168.0.14:5000/Alarmas/agregar/'

            # Parameters to send in the request (you can customize these)
            params = {
                'hora': Hora,
                'minutos': minutos,
                'ampm': AMorPM,
                'fecha': date,
                'tipo': alarm_type
            }

            response = requests.get(url, params=params)

            response_message = "Agregada Exitosamente" if response.text != "Error" else "Error"
        else:
            response_message = "La hora no es valida"

            # Show the response message in a popup
        response_popup = ResponsePopup(response_message)
        response_popup.open()


    def add_toogleampm(self, buton):
        if(buton.text == 'AM'):
            buton.text = 'PM'
        else:
            buton.text = 'AM'


from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

class ViewAlarmsScreen(Screen):
    def __init__(self, **kwargs):
        super(ViewAlarmsScreen, self).__init__(**kwargs)

        # Create a ScrollView to make the content scrollable
        scroll_view = ScrollView()
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None, padding=10)
        layout.bind(minimum_height=layout.setter('height'))
        scroll_view.add_widget(layout)
        self.add_widget(scroll_view)

        response = requests.get("http://192.168.0.14:5000/Alarmas/listar")

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Extract JSON content from the response
            json_data = response.json()

            # Parse JSON response and create dynamic height widgets
            for entry in json_data:
                entry_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=dp(40))
                hora_label = Label(text=f'Hora: {entry["hora"]}', size_hint_x=None, width=dp(100))
                minutos_label = Label(text=f'Minutos: {entry["minutos"]}', size_hint_x=None, width=dp(100))
                ampm_label = Label(text=f'AM/PM: {entry["ampm"]}', size_hint_x=None, width=dp(100))
                fecha_label = Label(text=f'Fecha: {entry["fecha"]}', size_hint_x=None, width=dp(100))
                tipo_label = Label(text=f'Tipo: {entry["tipo"]}', size_hint_x=None, width=dp(100))
                creacionEpoch_label = Label(text=f'Epoch: {entry["creacionEpoch"]}', size_hint_x=None, width=dp(100))

                entry_layout.add_widget(hora_label)
                entry_layout.add_widget(minutos_label)
                entry_layout.add_widget(ampm_label)
                entry_layout.add_widget(fecha_label)
                entry_layout.add_widget(tipo_label)
                entry_layout.add_widget(creacionEpoch_label)

                layout.add_widget(entry_layout)

            # Add a close button
            close_button = Button(text='Cerrar', size_hint_y=None, height=dp(40))
            close_button.bind(on_press=self.go_to_main_screen)
            layout.add_widget(close_button)

    def go_to_main_screen(self, instance):
        self.manager.current = 'main'


class AlarmApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(AddAlarmScreen(name='add_alarm'))
        sm.add_widget(ViewAlarmsScreen(name='view_alarms'))
        return sm


if __name__ == '__main__':
    AlarmApp().run()