from graphics import *
from graphics_extras import Button, Slider
from game import Game
import settings.edit_settings as edit_settings


# Class for Settings Screen which has the sliders and back button
class SettingsScreen:
    # Create the graphics objects, buttons and sliders
    title_text = Text(Point(600, 300), "Settings")
    title_text.setSize(36)

    music_slider_value = edit_settings.get_music_volume()
    music_volume_slider = Slider(Point(400, 600), length=200, thickness=10, starting_value=music_slider_value)
    music_volume_text = Text(Point(400, 550), f"Music Volume: {music_volume_slider.value * 100:.0f}%")

    music_volume_slider.set_top_track_color(color_rgb(0, 132, 255))
    music_volume_slider.set_track_color(color_rgb(203, 210, 214))
    music_volume_slider.set_knob_color(color_rgb(245, 249, 252))

    sfx_slider_value = edit_settings.get_sfx_volume()
    sfx_volume_slider = Slider(Point(800, 600), length=200, thickness=10, starting_value=sfx_slider_value)
    sfx_volume_text = Text(Point(800, 550), f"SFX Volume: {sfx_volume_slider.value * 100:.0f}%")

    sfx_volume_slider.set_top_track_color(color_rgb(0, 132, 255))
    sfx_volume_slider.set_track_color(color_rgb(203, 210, 214))
    sfx_volume_slider.set_knob_color(color_rgb(245, 249, 252))

    back_button = Button(Point(0, 600), Point(200, 700), "Back")
    back_button.body.setFill(color_rgb(255, 255, 255))
    back_button.label.setFill(color_rgb(0, 0, 0))

    # Draw everything on the screen and bind the clicks
    @staticmethod
    def draw_screen(event=None):
        Game.undraw_all()

        SettingsScreen.title_text.draw(Game.window)

        Game.window.setBackground(color_rgb(89, 191, 255))
        SettingsScreen.music_volume_slider.draw(Game.window)
        SettingsScreen.music_volume_text.draw(Game.window)
        SettingsScreen.music_volume_slider.bind_click(Game.window, SettingsScreen.update_music_volume)

        SettingsScreen.sfx_volume_slider.draw(Game.window)
        SettingsScreen.sfx_volume_text.draw(Game.window)
        SettingsScreen.sfx_volume_slider.bind_click(Game.window, SettingsScreen.update_sfx_volume)

        SettingsScreen.back_button.draw(Game.window)
        SettingsScreen.back_button.bind_click(Game.window, SettingsScreen.switch_to_main_menu)

    # Will update the volume when the slider is dragged
    @staticmethod
    def update_music_volume(event=None):
        edit_settings.change_music_volume(SettingsScreen.music_volume_slider.value)
        SettingsScreen.music_volume_text.setText(f"Volume: {SettingsScreen.music_volume_slider.value * 100:.0f}%")
        Game.bgm.volume = SettingsScreen.music_volume_slider.value * 100

    @staticmethod
    def update_sfx_volume(event=None):
        edit_settings.change_sfx_volume(SettingsScreen.sfx_volume_slider.value)
        SettingsScreen.sfx_volume_text.setText(f"Volume: {SettingsScreen.sfx_volume_slider.value * 100:.0f}%")
        Game.hit_sound.volume = SettingsScreen.sfx_volume_slider.value * 100
        Game.stand_sound.volume = SettingsScreen.sfx_volume_slider.value * 100
        Game.win_sfx.volume = SettingsScreen.sfx_volume_slider.value * 100
        Game.lose_sfx.volume = SettingsScreen.sfx_volume_slider.value * 100
        Game.new_game_sound.volume = SettingsScreen.sfx_volume_slider.value * 100
        Game.pop_sfx.volume = SettingsScreen.sfx_volume_slider.value * 100

    # Switch to start screen and play the pop sound
    @staticmethod
    def switch_to_main_menu(event=None):
        Game.pop_sfx.play(block=False, loop=False)
        from screens.start_screen import StartScreen
        StartScreen.start()
