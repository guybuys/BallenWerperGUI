import pygame
from graphic_interface import Slider, PushButtonPic, TextField, TerminalWindow, Label, SerialPlotter
from serial_manager import SerialManager
from parameter_manager import ParameterManager
from colors import BLACK, RED, GRAY, BACKGROUNDCOLOR, DARKGREEN, SCREENGREEN
import os

# Get the current directory of the Python file
current_dir = os.path.dirname(__file__)

# Specify the name of the folder containing images
image_folder = 'images'

# Construct the path to the image files
on_image_path = os.path.join(current_dir, image_folder, 'SSL_Button_ON.png')
off_image_path = os.path.join(current_dir, image_folder, 'SSL_Button_OFF.png')

# Set the path to your font file
lcd_font_path = "C:/Users/guy.buys/PycharmProjects/SerialCommunicationDisplay/fonts/LCD-Solid/LCD_Solid.ttf"
led_font_path = "C:/Users/guy.buys/PycharmProjects/SerialCommunicationDisplay/fonts/ds_digital/DS-DIGII.TTF"
# ls7_font_path = "C:/Users/guy.buys/PycharmProjects/SerialCommunicationDisplay/fonts/Segment7/Segment7Standard.otf"
# dymo_font_path = ("C:/Users/guy.buys/PycharmProjects/SerialCommunicationDisplay/fonts/dymo_grunge_bubble"
#                  "/Dymo Grunge Bubble.ttf")
sharpie_font_path = ("C:/Users/guy.buys/PycharmProjects/SerialCommunicationDisplay/fonts/permanent-marker-font"
                     "/PermanentMarker-x99j.ttf")
serial_connected = False

# Define constants for window dimensions
# WINDOW_WIDTH = 1120
# WINDOW_HEIGHT = 800

# Define constants for interface
PID_TARGET_OFFSET = 1
TOLERANCE_RANGE = 1


def get_param_value(name, pm, ttx, trx):
    parameter_name, parameter_value = pm.get_parameter(name)
    ttx.add_message(name, color=DARKGREEN)
    trx.add_message(parameter_name + " " + parameter_value, color=DARKGREEN)
    try:
        return float(parameter_value)
    except ValueError:
        return float('nan')


def main():
    pygame.init()
    # -----
    # Get display information
    display_info = pygame.display.Info()

    # Get maximum resolution
    max_resolution = (display_info.current_w, display_info.current_h)

    # 150% => (1280, 720) event.w = 1280, event.h = 649
    # 125% => (1536, 864) event.w = 1536, event.h = 793
    # 100% => (1920, 1080) event.w = 1920, event.h = 1009

    print("Maximum resolution:", max_resolution)
    window_width, window_height = max_resolution

    window_height = round(window_height * .9)

    serial_manager = SerialManager()
    parameter_manager = ParameterManager(serial_manager)
    # Open serial connection
    parameter_manager.open_serial_connection()

    pygame.display.set_caption("Arduino Serial Interface " + parameter_manager.get_serial_connection_name())

    # Set screen to maximum resolution (90% in height)
    screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)

    # -----

    serial_manager = SerialManager()
    parameter_manager = ParameterManager(serial_manager)
    # Open serial connection
    parameter_manager.open_serial_connection()

    pygame.display.set_caption("Arduino Serial Interface " + parameter_manager.get_serial_connection_name())

    clock = pygame.time.Clock()
    running = True

    # callback functions
    def button_callback(state):
        if state:
            value = 1
        else:
            value = 0
        terminal_tx_window.add_message("motor " + str(value), color=DARKGREEN)
        parameter_manager.set_parameter("motor", value)

    def pid_callback(state):
        if state:
            value = 1
        else:
            value = 0
        terminal_tx_window.add_message("pid " + str(value), color=DARKGREEN)
        parameter_manager.set_parameter("pid", value)

    def kp_callback(value):
        terminal_tx_window.add_message("kp " + str(value), color=DARKGREEN)
        parameter_manager.set_parameter("kp", value)

    def ki_callback(value):
        terminal_tx_window.add_message("ki " + str(value), color=DARKGREEN)
        parameter_manager.set_parameter("ki", value)

    def kd_callback(value):
        terminal_tx_window.add_message("kd " + str(value), color=DARKGREEN)
        parameter_manager.set_parameter("kd", value)

    # Create UI elements
    switch_on = PushButtonPic(50, 25, on_image_path, off_image_path, "motor", callback=button_callback)

    switch_pid = PushButtonPic(150, 25, on_image_path, off_image_path, "PID", callback=pid_callback)

    slider_pwm1 = Slider(50, 175, 1024, 30, 0, 1023, 100,
                         slot_color=BLACK, slider_color=GRAY)
    slider_pwm2 = Slider(50, 275, 1024, 30, 0, 1023, 100,
                         slot_color=BLACK, slider_color=GRAY)
    slider_target = Slider(50, 375, 1024, 30, 0, 255, 100,
                           slot_color=BLACK, slider_color=(200, 200, 200))
    slider_angle = Slider(50, 475, 1024, 30, 0, 180, 90,
                          slot_color=BLACK, slider_color=(200, 200, 200))

    label_pwm1 = Label(60, 120, 'PWM1', font=sharpie_font_path, font_size=28, color=(0, 0, 0))
    label_pwm2 = Label(60, 220, 'PWM2', font=sharpie_font_path, font_size=28, color=(0, 0, 0))
    label_target = Label(50, 320, 'Target', font=sharpie_font_path, font_size=28, color=(0, 0, 0))
    label_speed1 = Label(410, 2, 'Speed1', font=sharpie_font_path, font_size=28, color=(0, 0, 0))
    label_speed2 = Label(610, 2, 'Speed2', font=sharpie_font_path, font_size=28, color=(0, 0, 0))
    label_kp = Label(840, 8, 'KP', font=sharpie_font_path, font_size=28, color=(0, 0, 0))
    label_ki = Label(840, 58, 'KI', font=sharpie_font_path, font_size=28, color=(0, 0, 0))
    label_kd = Label(840, 108, 'KD', font=sharpie_font_path, font_size=28, color=(0, 0, 0))
    label_angle = Label(50, 420, 'Angle', font=sharpie_font_path, font_size=28, color=(0, 0, 0))

    text_field_pwm1 = TextField(200, 125, 100, 40, rect_color=BLACK, background_color=BLACK,
                                passive_text_color=RED, font=led_font_path, font_size=40)
    text_field_pwm2 = TextField(200, 225, 100, 40, rect_color=BLACK, background_color=BLACK,
                                passive_text_color=RED, font=led_font_path, font_size=40)
    text_field_speed = TextField(200, 325, 100, 40, rect_color=BLACK, background_color=BLACK,
                                 passive_text_color=RED, font=led_font_path, font_size=40)
    text_field_rps1 = TextField(400, 40, 120, 45, rect_color=BLACK, background_color=BLACK,
                                passive_text_color=RED, font=led_font_path, font_size=40)
    text_field_rps2 = TextField(600, 40, 120, 45, rect_color=BLACK, background_color=BLACK,
                                passive_text_color=RED, font=led_font_path, font_size=40)
    text_field_angle = TextField(200, 425, 100, 45, rect_color=BLACK, background_color=BLACK,
                                 passive_text_color=RED, font=led_font_path, font_size=40)

    text_field_lcd = TextField(910, 8, 160, 151, rect_color=BLACK, font=lcd_font_path, font_size=30)
    text_field_kp = TextField(930, 10, 100, 45, rect_color=(100, 200, 0), font=lcd_font_path,
                              font_size=30, editable=True, callback=kp_callback)
    text_field_ki = TextField(930, 60, 100, 45, rect_color=(100, 200, 0), font=lcd_font_path,
                              font_size=30, editable=True, callback=ki_callback)
    text_field_kd = TextField(930, 110, 100, 45, rect_color=(100, 200, 0), font=lcd_font_path,
                              font_size=30, editable=True, callback=kd_callback)

    terminal_tx_window = TerminalWindow(50, 520, 500, 270, background_color=SCREENGREEN)
    terminal_rx_window = TerminalWindow(575, 520, 500, 270, background_color=SCREENGREEN)

    # Get values from device with parameter manager
    switch_on.set_state(get_param_value("motor", parameter_manager, terminal_tx_window, terminal_rx_window))
    switch_pid.set_state(get_param_value("pid", parameter_manager, terminal_tx_window, terminal_rx_window))
    text_field_kp.set_value(get_param_value("kp", parameter_manager, terminal_tx_window, terminal_rx_window))
    text_field_ki.set_value(get_param_value("ki", parameter_manager, terminal_tx_window, terminal_rx_window))
    text_field_kd.set_value(get_param_value("kd", parameter_manager, terminal_tx_window, terminal_rx_window))
    slider_pwm1.update_value(get_param_value("pwm1", parameter_manager, terminal_tx_window, terminal_rx_window))
    slider_pwm1.update_slider_position()
    slider_pwm2.update_value(get_param_value("pwm2", parameter_manager, terminal_tx_window, terminal_rx_window))
    slider_pwm2.update_slider_position()
    slider_target.update_value(get_param_value("speed", parameter_manager, terminal_tx_window, terminal_rx_window))
    slider_target.update_slider_position()
    slider_angle.update_value(get_param_value("servo", parameter_manager, terminal_tx_window, terminal_rx_window))
    slider_angle.update_slider_position()

    # Start program
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            switch_on.handle_event(event)
            switch_pid.handle_event(event)
            if not switch_pid.get_state():
                slider_pwm1.handle_event(event)
                slider_pwm2.handle_event(event)
            slider_target.handle_event(event)
            slider_angle.handle_event(event)
            text_field_kp.handle_event(event)
            text_field_ki.handle_event(event)
            text_field_kd.handle_event(event)

        text_field_pwm1.set_value(int(slider_pwm1.get_value()))
        text_field_pwm2.set_value(int(slider_pwm2.get_value()))
        text_field_speed.set_value(int(slider_target.get_value()))
        text_field_angle.set_value(int(slider_angle.get_value()))
        # Update UI elements
        # serial_plotter.update()

        # Draw everything
        screen.fill(BACKGROUNDCOLOR)
        slider_pwm1.draw(screen)
        slider_pwm2.draw(screen)
        slider_target.draw(screen)
        slider_angle.draw(screen)
        switch_on.draw(screen)
        switch_pid.draw(screen)
        label_pwm1.draw(screen)
        label_pwm2.draw(screen)
        label_target.draw(screen)
        label_speed1.draw(screen)
        label_speed2.draw(screen)
        label_kp.draw(screen)
        label_ki.draw(screen)
        label_kd.draw(screen)
        label_angle.draw(screen)

        text_field_pwm1.draw(screen)
        text_field_pwm2.draw(screen)
        text_field_speed.draw(screen)
        text_field_rps1.draw(screen)
        text_field_rps2.draw(screen)
        text_field_angle.draw(screen)
        text_field_lcd.draw(screen)
        text_field_kp.draw(screen)
        text_field_ki.draw(screen)
        text_field_kd.draw(screen)
        terminal_tx_window.draw(screen)
        terminal_rx_window.draw(screen)
        # serial_plotter.draw(screen)
        pygame.display.flip()

        # Catch if sliders are moved (switches and textbox handled via callback functions)

        if slider_pwm1.is_moved() and not switch_pid.get_state():
            slider_pwm1_val_str = str(int(slider_pwm1.get_value()))
            print("Current slider_pwm1 value: " + slider_pwm1_val_str)
            parameter_manager.set_parameter("pwm1", slider_pwm1_val_str)
            terminal_tx_window.add_message("pwm1 " + slider_pwm1_val_str, color=DARKGREEN)

        if slider_pwm2.is_moved() and not switch_pid.get_state():
            slider_pwm2_val_str = str(int(slider_pwm2.get_value()))
            print("Current slider_pwm2 value: " + slider_pwm2_val_str)
            parameter_manager.set_parameter("pwm2", slider_pwm2_val_str)
            terminal_tx_window.add_message("pwm2 " + slider_pwm2_val_str, color=DARKGREEN)

        if slider_target.is_moved():
            slider_target_val_str = str(int(slider_target.get_value()))
            print("Current slider_target value: " + slider_target_val_str)
            parameter_manager.set_parameter("speed", slider_target_val_str)
            terminal_tx_window.add_message("speed " + slider_target_val_str, color=DARKGREEN)

        if slider_angle.is_moved():
            slider_angle_val_str = str(int(slider_angle.get_value()))
            print("Current slider_angle value: " + slider_angle_val_str)
            parameter_manager.set_parameter("servo", slider_angle_val_str)
            terminal_tx_window.add_message("servo " + slider_angle_val_str, color=DARKGREEN)

        # Get parameters updates
        update_list = parameter_manager.check_parameter_updates()
        if update_list:
            for item in update_list:
                parameter_name, parameter_value = item
                terminal_rx_window.add_message(parameter_name + " " + parameter_value, color=DARKGREEN)
                if parameter_name == "motor":
                    if parameter_value != switch_on.get_state():
                        if parameter_value == "1":
                            switch_on.set_state(True)
                        else:
                            switch_on.set_state(False)
                elif parameter_name == "pid":
                    if parameter_value != switch_pid.get_state():
                        if parameter_value == "1":
                            switch_pid.set_state(True)
                        else:
                            switch_pid.set_state(False)
                elif parameter_name == "motorRps1":
                    text_field_rps1.set_value(parameter_value)
                    target = slider_target.get_value()
                    if switch_pid.get_state():
                        pid_offset = PID_TARGET_OFFSET
                    else:
                        pid_offset = 0
                    if ((float(parameter_value) + pid_offset - TOLERANCE_RANGE) < target <
                            (float(parameter_value) + pid_offset + TOLERANCE_RANGE)):
                        text_field_rps1.change_colors(passive_text_color=DARKGREEN)
                    else:
                        text_field_rps1.change_colors(passive_text_color=RED)
                elif parameter_name == "motorRps2":
                    text_field_rps2.set_value(parameter_value)
                    target = slider_target.get_value()
                    if switch_pid.get_state():
                        pid_offset = PID_TARGET_OFFSET
                    else:
                        pid_offset = 0
                    if ((float(parameter_value) + pid_offset - TOLERANCE_RANGE) < target <
                            (float(parameter_value) + pid_offset + TOLERANCE_RANGE)):
                        text_field_rps2.change_colors(passive_text_color=DARKGREEN)
                    else:
                        text_field_rps2.change_colors(passive_text_color=RED)
                elif parameter_name == "pwm1":
                    if switch_pid.get_state():
                        slider_pwm1.update_value(int(float(parameter_value)))
                        slider_pwm1.update_slider_position()
                elif parameter_name == "pwm2":
                    if switch_pid.get_state():
                        slider_pwm2.update_value(int(float(parameter_value)))
                        slider_pwm2.update_slider_position()

        clock.tick(60)

    pygame.quit()
    # Close the serial connection when done
    parameter_manager.close_serial_connection()


if __name__ == "__main__":
    main()
