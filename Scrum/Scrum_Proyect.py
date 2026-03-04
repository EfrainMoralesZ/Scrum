"""
Aplicación de Gestión de Proyectos Scrum - Multibrand.
Permite crear, gestionar y organizar múltiples proyectos con tableros Scrum.
"""

from Scrum import ScrumService
from ScrumUI import ScrumView
from ProjectUI import ProjectSelectionView
from ProjectManager import ProjectManager
import customtkinter as ctk
from pathlib import Path


class ScrumApp:
    """Aplicación principal de gestión de proyectos Scrum."""
    
    def __init__(self) -> None:
        """Inicializa la aplicación."""
        self.current_theme = "light"  # light o dark
        ctk.set_appearance_mode(self.current_theme)
        
        self.app = ctk.CTk()
        self.app.title("🎯 Board de Scrum - Multibrand")
        self.app.geometry("1000x500")
        self._configure_app_icon()
        
        # Definir estilos para ambos temas
        self.STYLES = {
            "light": {
                "primario": "#ECD925",
                "secundario": "#282828",
                "exito": "#008D53",
                "advertencia": "#ff1500",
                "peligro": "#d74a3d",
                "fondo": "#F8F9FA",
                "surface": "#FFFFFF",
                "texto_oscuro": "#282828",
                "texto_claro": "#ffffff",
                "borde": "#E0E0E0",
                # Colores de botones primarios (amarillos)
                "btn_primario_bg": "#ECD925",
                "btn_primario_fg": "#1F1F1F",
                "btn_primario_border": "#D4B81D",
                # Colores de botones (mantienen el mismo fondo)
                "btn_editar_bg": "#E8F4FD",
                "btn_editar_fg": "#1F3A56",
                "btn_editar_border": "#B8D4E8",
                "btn_borrar_bg": "#FFE5E5",
                "btn_borrar_fg": "#7A2F2F",
                "btn_borrar_border": "#F5B8B8",
                "btn_group_bg": "#E8F4FD",
                "btn_group_fg": "#1F3A56",
                "btn_group_border": "#B8D4E8",
                "btn_group_active_bg": "#FFF4E5",
                "btn_group_active_fg": "#7A4A12",
                "btn_group_active_border": "#FFBB7A",
                "btn_refresh_bg": "#F0F0F0",
                "btn_refresh_fg": "#2E2E2E",
                "btn_refresh_border": "#D0D0D0",
                # Botón de tema - minimalista claro
                "btn_theme_bg": "transparent",
                "btn_theme_fg": "#888888",
                "btn_theme_hover": "#DDDDDD",
                "btn_theme_border": "transparent",
            },
            "dark": {
                "primario": "#ECD925",
                "secundario": "#F0F0F0",
                "exito": "#00A86B",
                "advertencia": "#ff1500",
                "peligro": "#e8665a",
                "fondo": "#1E1E1E",
                "surface": "#2D2D2D",
                "texto_oscuro": "#F0F0F0",
                "texto_claro": "#1E1E1E",
                "borde": "#404040",
                # Colores de botones primarios (amarillos - mejorados para modo oscuro)
                "btn_primario_bg": "#D4AF37",
                "btn_primario_fg": "#1F1F1F",
                "btn_primario_border": "#8B7500",
                # Colores de botones (mismo fondo, texto diferente)
                "btn_editar_bg": "#E8F4FD",
                "btn_editar_fg": "#1F3A56",
                "btn_editar_border": "#B8D4E8",
                "btn_borrar_bg": "#FFE5E5",
                "btn_borrar_fg": "#7A2F2F",
                "btn_borrar_border": "#F5B8B8",
                "btn_group_bg": "#E8F4FD",
                "btn_group_fg": "#1F3A56",
                "btn_group_border": "#B8D4E8",
                "btn_group_active_bg": "#FFF4E5",
                "btn_group_active_fg": "#7A4A12",
                "btn_group_active_border": "#FFBB7A",
                "btn_refresh_bg": "#F0F0F0",
                "btn_refresh_fg": "#2E2E2E",
                "btn_refresh_border": "#D0D0D0",
                # Botón de tema - minimalista oscuro
                "btn_theme_bg": "transparent",
                "btn_theme_fg": "#B0B0B0",
                "btn_theme_hover": "#3A3A3A",
                "btn_theme_border": "transparent",
            }
        }
        
        self.STYLE = self.STYLES[self.current_theme]
        
        self.app.configure(fg_color=self.STYLE["fondo"])
        
        # Inicializar proyecto manager
        self.project_manager = ProjectManager(base_dir="projects")
        self.current_project = None
        self.scrum_service = None
        self.scrum_view = None
        
        # Mostrar pantalla de selección de proyectos
        self._show_project_selection()
    
    def _show_project_selection(self) -> None:
        """Muestra la pantalla de selección de proyectos."""
        # Limpiar contenido anterior
        for widget in self.app.winfo_children():
            widget.destroy()
        
        # Asegurar que el fondo de la app es correcto
        self.app.configure(fg_color=self.STYLE["fondo"])
        
        # Crear vista de selección de proyectos
        project_view = ProjectSelectionView(
            parent=self.app,
            style=self.STYLE,
            on_project_selected=self._on_project_selected,
            on_theme_change=self._toggle_theme,
        )

    def _configure_app_icon(self) -> None:
        """Configura el icono principal de la aplicación."""
        icon_path = Path(__file__).resolve().parent / "img" / "icono.ico"
        if not icon_path.exists():
            return

        try:
            self.app.iconbitmap(str(icon_path))
        except Exception:
            pass
    
    def _toggle_theme(self) -> None:
        """Alterna entre tema claro y oscuro."""
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        ctk.set_appearance_mode(self.current_theme)
        self.STYLE = self.STYLES[self.current_theme]
        
        # Actualizar el color de fondo de la aplicación
        self.app.configure(fg_color=self.STYLE["fondo"])
        
        # Recargar la vista actual
        if self.current_project:
            self._show_scrum_view()
        else:
            self._show_project_selection()
    
    def _on_project_selected(self, project_name: str) -> None:
        """Se ejecuta cuando se selecciona un proyecto."""
        self.current_project = project_name
        
        # Obtener ruta al archivo scrum_board.json del proyecto
        scrum_path = self.project_manager.get_project_scrum_path(project_name)
        
        if not scrum_path:
            # Crear estructura si no existe
            project_dir = Path("projects") / project_name
            scrum_path = project_dir / "scrum_board.json"
        
        # Inicializar servicio de Scrum
        self.scrum_service = ScrumService(data_dir=scrum_path.parent)
        
        # Mostrar vista de Scrum
        self._show_scrum_view()
    
    def _show_scrum_view(self) -> None:
        """Muestra la vista de Scrum del proyecto actual."""
        # Limpiar contenido anterior
        for widget in self.app.winfo_children():
            widget.destroy()
        
        # Asegurar que el fondo de la app es correcto
        self.app.configure(fg_color=self.STYLE["fondo"])
        
        # Marco principal con fondo visible
        main_frame = ctk.CTkFrame(self.app, fg_color=self.STYLE["fondo"])
        main_frame.pack(fill="both", expand=True)
        
        # Botón para volver a proyectos
        back_frame = ctk.CTkFrame(main_frame, fg_color=self.STYLE["fondo"])
        back_frame.pack(fill="x", padx=20, pady=(15, 0))
        
        back_btn = ctk.CTkButton(
            back_frame,
            text="← Volver a Proyectos",
            command=self._show_project_selection,
            fg_color="#666666",
            text_color="white",
            font=("Inter", 11),
            height=32,
            width=150,
        )
        back_btn.pack(side="left")
        
        project_label = ctk.CTkLabel(
            back_frame,
            text=f"📁 Proyecto: {self.current_project}",
            font=("Inter", 13, "bold"),
            text_color=self.STYLE["texto_oscuro"],
        )
        project_label.pack(side="left", padx=(20, 0))
        
        # Botón de cambio de tema
        theme_icon = "🌙" if self.current_theme == "light" else "☀️"
        theme_btn = ctk.CTkButton(
            back_frame,
            text=theme_icon,
            command=self._toggle_theme,
            fg_color=self.STYLE["btn_theme_bg"],
            text_color=self.STYLE["btn_theme_fg"],
            hover_color=self.STYLE["btn_theme_hover"],
            font=("Inter", 13),
            height=28,
            width=35,
            corner_radius=6,
            border_width=0,
            border_color=self.STYLE["btn_theme_border"],
        )
        theme_btn.pack(side="right", padx=(10, 0))
        
        # Crear vista de Scrum
        self.scrum_view = ScrumView(
            parent=main_frame,
            scrum_service=self.scrum_service,
            style=self.STYLE,
        )
    
    def run(self) -> None:
        """Inicia la aplicación."""
        self.app.mainloop()


def main() -> None:
    """Función principal."""
    app = ScrumApp()
    app.run()


if __name__ == "__main__":
    main()
