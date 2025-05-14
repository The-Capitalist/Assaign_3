import flet as ft  # type: ignore
import requests  # type: ignore

API_URL = "http://192.168.101.164:5000"  # Change to your server IP if needed

def main(page: ft.Page):
    page.title = "Smart Room Controller"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 30
    page.scroll = ft.ScrollMode.AUTO
    page.vertical_alignment = ft.MainAxisAlignment.START

    # Controls
    led_checkbox = ft.Switch(label="LED Auto Mode", value=False)
    led_override_checkbox = ft.Switch(label="Manual LED Override", value=False)
    fan_slider = ft.Slider(
        min=0, max=255, value=0, divisions=51,
        label="{value}", tooltip="Adjust fan speed"
    )

    # Status Texts
    flet_status_text = ft.Text(value="Flet control not synced yet.", size=13, color=ft.Colors.BLUE_GREY_200)
    esp_status_text = ft.Text(value="ESP data not received.", size=13, color=ft.Colors.BLUE_GREY_200)

    # Update Flet Control Data
    def update_flet_data(e=None):
        data = {
            "led": led_checkbox.value,
            "fan_speed": int(fan_slider.value),
            "led_override": led_override_checkbox.value
        }
        try:
            response = requests.post(f"{API_URL}/flet/update", json=data)
            flet_status_text.value = "✅ Control data sent" if response.status_code == 200 else f"❌ Error {response.status_code}"
        except Exception as ex:
            flet_status_text.value = f"⚠️ {str(ex)}"
        page.update()

    # Refresh all data from backend
    def refresh_status(e=None):
        try:
            response = requests.get(f"{API_URL}/dashboard")
            if response.status_code == 200:
                dashboard = response.json()
                flet_d = dashboard.get("flet", {})
                esp_d = dashboard.get("esp", {})

                # Update UI
                led_checkbox.value = flet_d.get("led", False)
                led_override_checkbox.value = flet_d.get("led_override", False)
                fan_slider.value = flet_d.get("fan_speed", 0)

                flet_status_text.value = (
                    f"LED: {'🟢 ON' if flet_d.get('led') else '🔴 OFF'}, "
                    f"Fan: {flet_d.get('fan_speed', 0)}, "
                    f"Override: {'✅ Enabled' if flet_d.get('led_override') else '❌ Disabled'}"
                )

                esp_status_text.value = (
                    f"Light Level: {esp_d.get('light', 'N/A')}, "
                    f"Motion: {'🟠 Detected' if esp_d.get('motion') else '⚫ None'}"
                )
            else:
                esp_status_text.value = f"❌ Dashboard Error: {response.status_code}"
        except Exception as ex:
            esp_status_text.value = f"⚠️ {str(ex)}"
        page.update()

    # Bind changes
    led_checkbox.on_change = update_flet_data
    led_override_checkbox.on_change = update_flet_data
    fan_slider.on_change = update_flet_data

    refresh_button = ft.ElevatedButton(text="🔄 Refresh Status", on_click=refresh_status)

    # Initial load
    refresh_status()

    # Final Layout
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("🧠 Smart Room Controller", size=26, weight="bold", text_align="center"),
                    ft.Divider(color=ft.Colors.BLUE_GREY_600),

                    ft.Text("Control Panel", size=18, weight="bold"),
                    led_checkbox,
                    led_override_checkbox,
                    fan_slider,

                    ft.Divider(height=20, color=ft.Colors.BLUE_GREY_800),
                    refresh_button,

                    ft.Divider(color=ft.Colors.BLUE_GREY_600),
                    ft.Text("Status Panel", size=18, weight="bold"),
                    flet_status_text,
                    esp_status_text
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.START
            ),
            padding=20,
            border_radius=12,
            bgcolor=ft.Colors.BLUE_GREY_900,
            width=500,
            alignment=ft.alignment.center
        )
    )

ft.app(target=main)
